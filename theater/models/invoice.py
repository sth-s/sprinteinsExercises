from pydantic import BaseModel
from typing import List

class Performance(BaseModel):
    play_id: str
    audience: int

class Invoice(BaseModel):
    customer: str
    performances: List[Performance]