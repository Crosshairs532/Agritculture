from src.service.FarmService import FarmService
from fastapi import APIRouter, Depends
from src.schemas.farm_schemas import FarmQuery
from dotenv import load_dotenv
load_dotenv(override=True)

router = APIRouter(prefix="/farms", tags=["farms"])
farm_service = FarmService()

@router.get("/summary")
async def get_farm_summary(filters: FarmQuery = Depends()): 
    return farm_service.get_farm_summary(**filters.dict())