import sys
import argparse
from pathlib import Path
from typing import Optional

from domains.sales.application.statement_service import StatementService
from domains.sales.domain.statements_generator_service import StatementsGeneratorService
from domains.sales.infrastructure.repositories import RepositoryFactory, RepositoryInterface
from domains.sales.infrastructure.text_renderer import TextRenderer
from shared.infrastructure.database import Database

def generate_statements(repository: RepositoryInterface, generator: StatementsGeneratorService, renderer: TextRenderer, output_file: Path = None):
    try:
        statements = StatementService(repository, generator, renderer).generate_statements(output_file)
        print(statements)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run(repo_type: str, database: Optional[Database], data_dir: Path):    
    try:
        repository = RepositoryFactory.create(repo_type, data_dir, database)
    except Exception as e:
        print(f"Repository Initialization Error: {e}", file=sys.stderr)
        sys.exit(1)

    generator = StatementsGeneratorService()
    renderer = TextRenderer()

    parser = argparse.ArgumentParser(description='Theater client')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    stmt_parser = subparsers.add_parser('generate-statements', help='Generate statements')
    stmt_parser.add_argument('--output', '-o', type=Path, help='Output file')
    stmt_parser.set_defaults(func=lambda args: generate_statements(repository, generator, renderer, args.output))

    args = parser.parse_args()
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
