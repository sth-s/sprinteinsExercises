import polars as pl
from domains.analytics.infrastructure.data_loader import DataLoader
from domains.analytics.infrastructure.report_writer import ReportWriter
from domains.analytics.domain.revenue_calculator import RevenueCalculator


class AnalyticsService:
    def __init__(self, loader: DataLoader, writer: ReportWriter, calculator: RevenueCalculator):
        self._loader = loader
        self._writer = writer
        self._calculator = calculator
    
    def generate_customer_report(self) -> pl.DataFrame:
        df = self._loader.load_performances_with_details()
        all_plays = self._loader.load_all_plays()
        
        result = self._calculator.calculate(df, all_plays)
        
        self._writer.save(result, "customer_reports")
        
        return result
