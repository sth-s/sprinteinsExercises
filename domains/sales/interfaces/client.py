import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List

from domains.sales.application.statement_service import StatementService
from domains.sales.application.invoice_service import InvoiceService
from domains.sales.domain.statements_generator_service import StatementsGeneratorService
from domains.sales.infrastructure.repositories import RepositoryFactory, RepositoryInterface
from domains.sales.infrastructure.text_renderer import TextRenderer
from shared.infrastructure.database import Database


def generate_statements(
    repository: RepositoryInterface, 
    generator: StatementsGeneratorService, 
    renderer: TextRenderer, 
    output_file: Optional[Path] = None
):
    try:
        statements = StatementService(repository, generator, renderer).generate_statements(output_file)
        print(statements)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def add_invoice(service: InvoiceService, customer: str, performances_json: str):
    try:
        performances = json.loads(performances_json)
        statement = service.add_invoice(customer, performances)
        print(statement)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def run(repo_type: str, database: Optional[Database], data_dir: Path, args: List[str]):
    try:
        repository = RepositoryFactory.create(repo_type, data_dir, database)
    except Exception as e:
        print(f"Repository Initialization Error: {e}", file=sys.stderr)
        sys.exit(1)

    generator = StatementsGeneratorService()
    renderer = TextRenderer()
    invoice_service = InvoiceService(repository, generator, renderer)

    parser = argparse.ArgumentParser(prog="main.py sales", description="Sales domain")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    stmt_parser = subparsers.add_parser("generate-statements", help="Generate statements")
    stmt_parser.add_argument("--output", "-o", type=Path, help="Output file")
    stmt_parser.set_defaults(func=lambda args: generate_statements(repository, generator, renderer, args.output))

    invoice_parser = subparsers.add_parser("add-invoice", help="Add new invoice")
    invoice_parser.add_argument("--customer", "-c", required=True, help="Customer name")
    invoice_parser.add_argument("--performances", "-p", required=True, help='Performances JSON, e.g. \'[{"play_id": "hamlet", "audience": 55}]\'')
    invoice_parser.set_defaults(func=lambda args: add_invoice(invoice_service, args.customer, args.performances))

    parsed_args = parser.parse_args(args)
    
    try:
        parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
