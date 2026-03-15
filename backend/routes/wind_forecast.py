from fastapi import APIRouter, Query, HTTPException
from ..bmrs_client import fetch_paginated
from ..forecast_logic import select_forecasts
from ..config import ELEXON_BASE, validate_january2024
from datetime import datetime, timedelta
import httpx

router = APIRouter()

def expand_to_half_hour(data):
    expanded = []

    for r in data:
        t = datetime.fromisoformat(r["startTime"].replace("Z", "+00:00"))
        value = r["forecast"]

        # original hour
        expanded.append({
            "startTime": t.isoformat().replace("+00:00", "Z"),
            "forecast": value
        })

        # +30 minutes
        t30 = t + timedelta(minutes=30)

        expanded.append({
            "startTime": t30.isoformat().replace("+00:00", "Z"),
            "forecast": value
        })

    return expanded

@router.get("/forecasts")
async def fetch_wind_forecasts(start: str = Query(...), end: str = Query(...), horizon_hours: float = Query(4.0)):
    validate_january2024(start)
    validate_january2024(end)

    try:
        dt_start = datetime.fromisoformat(start.replace("Z", "+00:00"))
        dt_end = datetime.fromisoformat(end.replace("Z", "+00:00"))
        publish_start = dt_start - timedelta(hours=48)

        async with httpx.AsyncClient() as client:
            params = {"publishDateTimeFrom": publish_start.isoformat(), "publishDateTimeTo": dt_end.isoformat(), "format": "json"}
            raw = await fetch_paginated(client, f"{ELEXON_BASE}/WINDFOR/stream", params)

        selected = select_forecasts(raw, horizon_hours)
        expanded = expand_to_half_hour(selected)

        # keep only points within requested time range
        filtered = [
            r for r in expanded
            if start <= r["startTime"] <= end
        ]

        filtered.sort(key=lambda x: x["startTime"])

        return {"data": filtered, "count": len(filtered)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))