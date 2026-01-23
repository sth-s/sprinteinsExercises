from abc import ABC, abstractmethod
import polars as pl


class AnalyticsCalculator(ABC):
    @abstractmethod
    def calculate_amount(self, audience_col: pl.Expr) -> pl.Expr:
        pass

    @abstractmethod
    def calculate_credits(self, audience_col: pl.Expr) -> pl.Expr:
        pass
