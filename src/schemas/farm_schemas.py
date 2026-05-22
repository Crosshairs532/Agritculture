from pydantic import BaseModel
from typing import Optional

class FarmQuery(BaseModel):
    region: Optional[str] = None
    farm_type: Optional[str] = None
    year: Optional[int] = None
    season: Optional[str] = None
    market_type:Optional[str] = None
    crop_category:Optional[str] = None
