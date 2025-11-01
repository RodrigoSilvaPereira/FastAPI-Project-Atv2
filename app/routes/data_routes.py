from fastapi import APIRouter, HTTPException, Body
from app.services.external_api import fetch_all_data, fetch_data_by_id, create_data

router = APIRouter(prefix="/data", tags=["Data API"])


@router.get("/", summary="List all data from external API")
async def get_all_data():
    try:
        return await fetch_all_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", summary="Get data by ID from external API")
async def get_data_by_id(item_id: int):
    try:
        data = await fetch_data_by_id(item_id)
        if not data:
            raise HTTPException(status_code=404, detail="Item not found")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", summary="Create new data via external API")
async def post_new_data(payload: dict = Body(...)):
    try:
        return await create_data(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
