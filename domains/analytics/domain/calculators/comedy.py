import polars as pl
from .interface import AnalyticsCalculator


class ComedyAnalyticsCalculator(AnalyticsCalculator):

    BASE_AMOUNT = 30000
    BASE_PER_PERSON = 300
    AUDIENCE_THRESHOLD = 20
    THRESHOLD_BONUS = 10000
    EXTRA_PER_PERSON = 500
    CREDITS_THRESHOLD = 30
    CREDITS_DIVISOR = 5

    def calculate_amount(self, audience: pl.Expr) -> pl.Expr:
        base = self.BASE_AMOUNT + (audience * self.BASE_PER_PERSON)
        extra = pl.when(audience > self.AUDIENCE_THRESHOLD).then(self.THRESHOLD_BONUS + (audience - self.AUDIENCE_THRESHOLD) * self.EXTRA_PER_PERSON).otherwise(0)
        return base + extra

    def calculate_credits(self, audience: pl.Expr) -> pl.Expr:
        return pl.max_horizontal(audience - self.CREDITS_THRESHOLD, 0) + (audience // self.CREDITS_DIVISOR)
