from pydantic import BaseModel
from theater.models.play import Play
from typing import List

class PerformanceResult(BaseModel):
    amount: int
    credits: int
    play: Play
    audience: int

class Statement(BaseModel):
    customer: str
    total_amount: int
    total_credits: int
    performance_details: List[PerformanceResult]