import sys
import argparse
from pathlib import Path
from theater.infrastructure.repository import Repository
from theater.infrastructure.text_renderer import TextRenderer
from theater.domain.statement_calculator import StatementCalculator
from theater.application.statement_service import StatementService


def generate_statements(data_dir: Path, output_file: Path = None):
    repository = Repository(data_dir)
    calculator = StatementCalculator()
    renderer = TextRenderer()
    service = StatementService(repository, calculator)
    
    statements = service.generate_statements()
    result = renderer.text_statements_render(statements)
    
    if output_file:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding='utf-8')
        print(f"Saved to {output_file}")
    else:
        print(result, end='')



def main():
    parser = argparse.ArgumentParser(description='Theater client')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    stmt_parser = subparsers.add_parser('generate-statements', help='Generate statements')
    stmt_parser.add_argument('--output', '-o', type=Path, help='Output file')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'generate-statements':
            generate_statements(Path("data"), args.output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
