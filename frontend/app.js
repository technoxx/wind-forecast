const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:8000'
  : '';

let chart = null;

const $ = id => document.getElementById(id);

// --- Slider label sync ---
$('horizonSlider').addEventListener('input', () => {
  $('horizonDisplay').textContent = $('horizonSlider').value + 'h';
});

// --- Helpers ---
function toISO(localDT) {
  return localDT + ':00Z';
}

function showError(msg) {
  const el = $('errorMsg');
  el.textContent = msg;
  el.style.display = 'block';
}

function clearError() {
  $('errorMsg').style.display = 'none';
}

function setLoading(on) {
  $('loadBtn').disabled = on;
  $('loadBtn').textContent = on ? 'Loading…' : 'Load Data';
  $('loadingOverlay').style.display = on ? 'flex' : 'none';
  $('chartPlaceholder').style.display = 'none';
}


// --- Chart ---
function renderChart(actuals, forecasts) {
  const ctx = $('mainChart').getContext('2d');

  const datasets = [
    {
      label: 'Actual',
      data: actuals.map(d => ({ x: d.startTime, y: d.generation })),
      borderColor: '#4a90d9',
      backgroundColor: 'rgba(74,144,217,0.07)',
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 4,
      tension: 0.3,
      fill: false,
    },
    {
      label: 'Forecast',
      data: forecasts.map(d => ({ x: d.startTime, y: d.forecast })),
      borderColor: '#27ae60',
      backgroundColor: 'rgba(39,174,96,0.07)',
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 4,
      tension: 0.3,
      fill: false,
    },
  ];

  if (chart) {
    chart.data.datasets = datasets;
    chart.update();
    return;
  }

  chart = new Chart(ctx, {
    type: 'line',
    data: { datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: items => new Date(items[0].raw.x).toUTCString().replace(' GMT', ' UTC'),
            label: item => `  ${item.dataset.label}: ${Math.round(item.raw.y).toLocaleString()} MW`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          time: {
            displayFormats: { hour: 'dd/MM HH:mm', day: 'dd MMM' },
          },
          ticks: { maxRotation: 0, autoSkipPadding: 16, color: '#999' },
          grid: { color: '#f0f0f0' },
        },
        y: {
          title: { display: true, text: 'Power (MW)', color: '#999' },
          ticks: { color: '#999', callback: v => v.toLocaleString() },
          grid: { color: '#f0f0f0' },
        },
      },
    },
  });
}

// --- Load ---
async function loadData() {
  const start     = $('startTime').value;
  const end       = $('endTime').value;
  const horizonH  = parseInt($('horizonSlider').value);

  clearError();

  if (!start || !end) { showError('Please select both start and end times.'); return; }
  if (new Date(start) >= new Date(end)) { showError('End time must be after start time.'); return; }

  const rangeDays = (new Date(end) - new Date(start)) / 86400000;
  if (rangeDays > 7) { showError('Please select a range of 7 days or less.'); return; }

  setLoading(true);

  try {
    const s = encodeURIComponent(toISO(start));
    const e = encodeURIComponent(toISO(end));

    const [resA, resF] = await Promise.all([
      fetch(`${API_BASE}/api/actuals?start=${s}&end=${e}`),
      fetch(`${API_BASE}/api/forecasts?start=${s}&end=${e}&horizon_hours=${horizonH}`),
    ]);

    if (!resA.ok) throw new Error(`Actuals API error: ${await resA.text()}`);
    if (!resF.ok) throw new Error(`Forecasts API error: ${await resF.text()}`);

    const { data: actuals }   = await resA.json();
    const { data: forecasts } = await resF.json();

    if (!actuals.length && !forecasts.length) {
      throw new Error('No data returned. Make sure the selected range is within January 2024.');
    }

    renderChart(actuals, forecasts);

    const note = $('chartNote');
    note.style.display = 'block';
    note.textContent =
      `Showing latest forecast published ≥ ${horizonH}h before each target time. ` +
      `${actuals.length} actual points · ${forecasts.length} forecast points.`;

  } catch (err) {
    showError(err.message || 'Failed to load data.');
    if (!chart) $('chartPlaceholder').style.display = 'flex';
  } finally {
    setLoading(false);
  }
}

$('loadBtn').addEventListener('click', loadData);