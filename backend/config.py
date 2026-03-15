ELEXON_BASE = "https://data.elexon.co.uk/bmrs/api/v1/datasets"
TIMEOUT = 30.0

from datetime import datetime, timezone
from fastapi import HTTPException

JAN_START = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
JAN_END   = datetime(2024, 1, 31, 23, 30, tzinfo=timezone.utc)

def validate_january2024(dt_str: str):
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if not (JAN_START <= dt <= JAN_END):
        raise HTTPException(
            status_code=400,
            detail=f"Date {dt_str} must be within January 2024"
        )