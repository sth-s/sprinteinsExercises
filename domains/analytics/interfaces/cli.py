import sys
import argparse
from pathlib import Path
from typing import List
from domains.analytics.infrastructure.analytics_repository import AnalyticsRepository
from domains.analytics.domain.revenue_calculator import RevenueCalculator
from domains.analytics.services.analytics_service import AnalyticsService
from domains.analytics.infrastructure.text_render import TextRender
from domains.analytics.services.print_text_statement_service import PrintTextStatementService


def generate_report(service: AnalyticsService, name: str = None):
    result = service.generate_customer_report(name)
    
    top5 = result.sort("total_amount", descending=True).head(5)
    print("\nTop 5 customers by revenue:")
    print(top5)


def print_text_report(service: PrintTextStatementService, name: str, save_as: str = None):
    result = service.print_text_report(name, save_as)
    print(result)


def run(db_path: Path, data_dir: Path, args: List[str]):
    repository = AnalyticsRepository(db_path, data_dir)
    calculator = RevenueCalculator()
    service = AnalyticsService(repository, calculator)
    renderer = TextRender()
    print_service = PrintTextStatementService(repository, renderer)
    
    parser = argparse.ArgumentParser(prog="main.py analytics", description="Analytics domain")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    report_parser = subparsers.add_parser("generate-report", help="Calculate and save customer reports")
    report_parser.add_argument("--name", "-n", type=str, default=None, help="Name of the report")
    report_parser.set_defaults(func=lambda args: generate_report(service, args.name))
    
    print_parser = subparsers.add_parser("print-text-report", help="Render report as text")
    print_parser.add_argument("--name", "-n", type=str, help="Name of the report to load")
    print_parser.add_argument("--save-as", "-s", type=str, help="Save the text report to file")
    print_parser.set_defaults(func=lambda args: print_text_report(print_service, args.name, args.save_as))
    
    parsed_args = parser.parse_args(args)
    
    try:
        parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
