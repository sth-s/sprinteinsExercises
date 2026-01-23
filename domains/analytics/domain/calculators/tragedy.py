import polars as pl
from .interface import AnalyticsCalculator


class TragedyAnalyticsCalculator(AnalyticsCalculator):
    
    BASE_AMOUNT = 40000
    AUDIENCE_THRESHOLD = 30
    EXTRA_PER_PERSON = 1000
    CREDITS_THRESHOLD = 30

    def calculate_amount(self, audience: pl.Expr) -> pl.Expr:
        return self.BASE_AMOUNT + pl.when(audience > self.AUDIENCE_THRESHOLD).then((audience - self.AUDIENCE_THRESHOLD) * self.EXTRA_PER_PERSON).otherwise(0)

    def calculate_credits(self, audience: pl.Expr) -> pl.Expr:
        return pl.when(audience > self.CREDITS_THRESHOLD).then(audience - self.CREDITS_THRESHOLD).otherwise(0)
