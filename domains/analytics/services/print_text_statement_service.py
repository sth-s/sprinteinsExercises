import polars as pl
from domains.analytics.infrastructure.text_render import TextRender
from domains.analytics.infrastructure.analytics_repository import AnalyticsRepository

class PrintTextStatementService:
    def __init__(self, repository: AnalyticsRepository, renderer: TextRender):
        self._repository = repository
        self._renderer = renderer

    def print_text_report(self, report_name: str, save_as: str = None) -> str:
        df = self._repository.load_report(report_name)
        text_report = self._renderer.text_report_as_statements_render(df)

        if save_as:
            self._repository.save_text_report(text_report, save_as)

        return text_report
