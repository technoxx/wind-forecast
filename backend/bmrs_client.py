import httpx
from .config import TIMEOUT

async def fetch_paginated(client: httpx.AsyncClient, url: str, params: dict) -> list:
    results = []
    page = 1
    MAX_PAGES = 20  # safety limit

    while page <= MAX_PAGES:
        p = {**params, "page": page, "pageSize": 1000}

        resp = await client.get(url, params=p, timeout=TIMEOUT)
        resp.raise_for_status()

        data = resp.json()
        items = data if isinstance(data, list) else data.get("data", [])

        if not items:
            break

        results.extend(items)

        if len(items) < 1000:
            break

        page += 1

    return results