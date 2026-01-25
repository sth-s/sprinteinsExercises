import polars as pl
from domains.analytics.infrastructure.analytics_repository import AnalyticsRepository
from domains.analytics.domain.revenue_calculator import RevenueCalculator


class AnalyticsService:
    def __init__(self, repository: AnalyticsRepository, calculator: RevenueCalculator):
        self._repository = repository
        self._calculator = calculator
    
    def generate_customer_report(self, name: str = None) -> pl.DataFrame:
        df = self._repository.load_performances_with_details()
        all_plays = self._repository.load_all_plays()
        
        result = self._calculator.calculate(df, all_plays)
        
        if name:
            self._repository.save_report(result, name)
        
        return result
