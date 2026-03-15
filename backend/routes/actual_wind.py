from fastapi import APIRouter, Query, HTTPException
from ..bmrs_client import fetch_paginated
from ..config import ELEXON_BASE, validate_january2024
import httpx

router = APIRouter()

@router.get("/actuals")
async def fetch_actual_wind(start: str = Query(...), end: str = Query(...)):
    validate_january2024(start)
    validate_january2024(end)

    try:
        async with httpx.AsyncClient() as client:
            params = {"publishDateTimeFrom": start, "publishDateTimeTo": end, "fuelType": "WIND", "format": "json"}
            raw = await fetch_paginated(client, f"{ELEXON_BASE}/FUELHH/stream", params)

        result = sorted([{"startTime": r["startTime"], "generation": r["generation"]}
                for r in raw if r.get("fuelType", "").upper() == "WIND"],key=lambda x: x["startTime"])

        return {"data": result, "count": len(result)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))