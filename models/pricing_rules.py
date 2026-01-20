from pydantic import BaseModel
from typing import Optional


class AmountRules(BaseModel):
    base_amount: int
    base_coefficient: int
    audience_threshold_amount: int
    threshold_amount: int
    threshold_coefficient: int


class CreditsRules(BaseModel):
    audience_threshold_credits: int
    credits_divisor: Optional[int]


class PricingRules(BaseModel):
    amount: AmountRules
    credits: CreditsRules