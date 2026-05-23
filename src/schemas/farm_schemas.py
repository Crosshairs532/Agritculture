from pydantic import BaseModel
from typing import Optional
from enum import Enum
from fastapi import Query

class FarmQuery(BaseModel):
    region: Optional[str] =Query(
        None, 
        description="Filter by  region (e.g., Dhaka, Chittagong)",
        example="Dhaka"
    )
    farm_type: Optional[str] =Query(
        None,
        description="Filter by farm type (e.g., Small, Medium, Large, Commercial)",
        example="Small"
    )
    year: Optional[int] =Query(
        None,
        description="Filter by year",
        example=2023
    )
    season: Optional[str] =Query(
        None,
        description="Filter by season (e.g., Spring, Summer, Autumn, Winter)",
        example="Spring"
    )
    market_type:Optional[str] =Query(
        None,
        description="Filter by market type",
        example="Local"
    )
    crop_category:Optional[str] =Query(
        None,
        description="Filter by crop category",
        example="Rice"
    )


class MetricEnum(str, Enum):
    PROFIT = "profit"
    REVENUE = "revenue"
    YIELD = "yield"
    
class FarmQueryMetric(FarmQuery):
    metric: Optional[MetricEnum] = Query(
        None,
        description="Filter by metric",
        example="profit"
    )
    limit: Optional[int] = 10

class FarmLossQuery(FarmQuery):
    quality_grade: Optional[str] =Query(
        None,
        description="Filter by quality grade",
        example="Grade A"
    )