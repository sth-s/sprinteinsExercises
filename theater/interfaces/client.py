import sys
import argparse
from pathlib import Path
from theater.application.statement_service import StatementService

def generate_statements(data_dir: Path, output_file: Path = None):
    try:
        statements = StatementService().generate_statements(data_dir, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Theater client')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    stmt_parser = subparsers.add_parser('generate-statements', help='Generate statements')
    stmt_parser.add_argument('--output', '-o', type=Path, help='Output file')
    stmt_parser.set_defaults(func=lambda args: generate_statements(Path("data"), args.output))

    args = parser.parse_args()
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
