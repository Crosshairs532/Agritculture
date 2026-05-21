from fastapi import APIRouter
from dotenv import load_dotenv
load_dotenv(override=True)

router = APIRouter(prefix="/crops", tags=["crops"])

@router.get("/yield-efficiency")
async def get_crop_yield_efficiency():
    return {"message": "Crop yield efficiency data will be here."}