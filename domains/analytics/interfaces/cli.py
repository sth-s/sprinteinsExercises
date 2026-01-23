import sys
import argparse
from pathlib import Path
from typing import List
from domains.analytics.infrastructure.data_loader import DataLoader
from domains.analytics.infrastructure.report_writer import ReportWriter
from domains.analytics.domain.revenue_calculator import RevenueCalculator
from domains.analytics.services.analytics_service import AnalyticsService


def generate_report(service: AnalyticsService):
    result = service.generate_customer_report()
    
    top5 = result.sort("total_amount", descending=True).head(5)
    print("\nTop 5 customers by revenue:")
    print(top5)


def run(db_path: Path, data_dir: Path, args: List[str]):
    loader = DataLoader(db_path)
    writer = ReportWriter(data_dir)
    calculator = RevenueCalculator()
    service = AnalyticsService(loader, writer, calculator)
    
    parser = argparse.ArgumentParser(prog="main.py analytics", description="Analytics domain")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    report_parser = subparsers.add_parser("generate-report", help="Calculate and save customer reports")
    report_parser.set_defaults(func=lambda _: generate_report(service))
    
    parsed_args = parser.parse_args(args)
    
    try:
        parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
