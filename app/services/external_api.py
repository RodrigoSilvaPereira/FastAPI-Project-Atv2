import httpx

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_all_data():
    """Get all data from external API asynchronously."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(BASE_URL)
        resp.raise_for_status()
        return resp.json()


async def fetch_data_by_id(item_id: int):
    """Get a single item by ID asynchronously."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{BASE_URL}/{item_id}")
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()


async def create_data(payload: dict):
    """Create new data on external API asynchronously (simulated)."""
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(BASE_URL, json=payload)
        resp.raise_for_status()
        return resp.json()
