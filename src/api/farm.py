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

@router.get('/{farm_id}/performance')
async def get_single_farm_performance(farm_id: str, query_params: FarmQuery = Depends()):
    return farm_service.get_Single_Farm_Performance(farm_id=farm_id, **query_params.dict())