from pydantic import BaseModel
from typing import Optional
from enum import Enum

class FarmQuery(BaseModel):
    region: Optional[str] = None
    farm_type: Optional[str] = None
    year: Optional[int] = None
    season: Optional[str] = None
    market_type:Optional[str] = None
    crop_category:Optional[str] = None


class MetricEnum(str, Enum):
    PROFIT = "profit"
    REVENUE = "revenue"
    YIELD = "yield"
    
class FarmQueryMetric(FarmQuery):
    metric: Optional[MetricEnum] = None
    limit: Optional[int] = 10

class FarmLossQuery(FarmQuery):
    quality_grade: Optional[str] = None