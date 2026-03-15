# Wind Forecast Monitoring & Analysis

A full-stack application to monitor and analyse wind power forecasts for the United Kingdom using BMRS datasets.

The system visualises the accuracy of wind generation forecasts and analyses historical wind power reliability to estimate dependable wind capacity for electricity demand planning.

---

# Live Demo

Application URL:
https://<your-deployment-link>

The app can be used to select a time range in January 2024 and compare actual vs forecast wind generation using different forecast horizons.

---

# Project Overview

This project consists of two components:

### 1. Forecast Monitoring Application

An interactive web application that visualises:

* Actual wind generation
* Forecasted wind generation

for a selected time range.

The application ensures that the **latest forecast published at least *H* hours before the target time** is used, where *H* is a configurable forecast horizon.

### 2. Forecast Error Analysis

A Jupyter notebook that analyses:

* Forecast error characteristics
* Error distribution
* Error behaviour across different times of day
* Reliability of historical wind generation

The goal is to understand how reliably wind power can meet electricity demand.

---

# Tech Stack

### Backend

* Python
* FastAPI
* HTTPX
* Pandas

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Data Analysis

* Python
* Pandas
* Matplotlib
* Jupyter Notebook

### Data Source

Data is obtained from the BMRS API:

Actual generation dataset
FUELHH – Wind power generation

Forecast dataset
WINDFOR – Wind generation forecasts

Both datasets were filtered to include **January 2024 data only**.

---

# System Architecture

User Interface (HTML/JS)

↓

Frontend fetches data from backend API

↓

FastAPI Backend

* Fetches BMRS data
* Filters forecast horizon
* Aligns forecast and actual values

↓

Visualization using Chart.js

---

# Forecast Selection Logic

For each target time **T**, the application selects the **latest forecast published before (T − H)** where:

* T = target generation time
* H = forecast horizon (user configurable)

Example:

Target time: 24/01/2024 18:00
Forecast horizon: 4 hours

The system selects the **latest forecast published before 14:00**.

This ensures forecasts represent information realistically available at prediction time.

---

# Application Features

* Interactive time range selection
* Configurable forecast horizon
* Real-time chart visualisation
* Actual vs Forecast comparison
* Responsive design (mobile + desktop)

---

# Running the Project

## Backend

Install dependencies

pip install -r requirements.txt

Run server

uvicorn backend.main:app --reload

Backend runs on:

http://localhost:8000

---

## Frontend

Simply open:

index.html

in a browser.

The frontend communicates with the backend API to retrieve wind data.

---

# Forecast Error Analysis

The notebook performs several analyses:

### Error Metrics

* Mean Absolute Error
* Median Error
* 99th Percentile Error

### Error Distribution

Understanding the variability and magnitude of forecast errors.

### Error vs Time of Day

Investigating whether forecasting accuracy varies across different periods.

### Wind Generation Reliability

Analysis of historical generation to estimate dependable wind capacity.

---

# Wind Reliability Recommendation

Wind generation is inherently variable due to weather conditions.

To estimate reliable wind capacity, the distribution of historical wind generation was analysed.

A conservative planning approach is to consider the **lower percentile of historical generation**.

For example:

* 10th percentile generation represents a level exceeded **90% of the time**
* This provides a conservative estimate of dependable wind capacity

Therefore, electricity planners should treat wind generation as **probabilistic rather than deterministic** when integrating it into supply planning.

---

# AI Tools Usage

AI tools were used only for:

* Debugging minor implementation issues
* Syntax assistance
* Library usage clarification

All system design, forecast filtering logic, and analysis were implemented and interpreted manually.


