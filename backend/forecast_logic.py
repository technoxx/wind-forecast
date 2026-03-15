from datetime import datetime, timedelta
from collections import defaultdict

def select_forecasts(forecasts: list, horizon_hours: float) -> list:
    data = defaultdict(list)
    for f in forecasts:
        data[f["startTime"]].append(f)

    selected = []
    for start_time, items in data.items():
        target_time = datetime.fromisoformat(start_time.replace("Z", ""))
        cutoff_time = target_time - timedelta(hours=horizon_hours)

        valid = [item for item in items if datetime.fromisoformat(item["publishTime"].replace("Z", "")) <= cutoff_time]
        if not valid:
            continue

        latest = max(valid, key=lambda x: datetime.fromisoformat(x["publishTime"].replace("Z", "")))
        selected.append({
            "startTime": start_time,
            "forecast": latest["generation"]
        })
    return selected