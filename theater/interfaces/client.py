import sys
import argparse
from pathlib import Path
from theater.application.statement_service import StatementService
from theater.domain.statements_generator_service import StatementsGeneratorService
from theater.infrastructure.repository import Repository
from theater.infrastructure.text_renderer import TextRenderer

def generate_statements(repository: Repository, generator: StatementsGeneratorService, renderer: TextRenderer, output_file: Path = None):
    try:
        statements = StatementService(repository, generator, renderer).generate_statements(output_file)
        print(statements)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    repository = Repository(Path("data"))
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


if __name__ == "__main__":
    main()
