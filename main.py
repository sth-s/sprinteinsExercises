from pathlib import Path
from utils.io_helper import IOHelper
from utils.statement import StatementGenerator


def main():
    io_helper = IOHelper(Path("data"))
    statement_generator = StatementGenerator()

    plays = io_helper.get_plays_dict()
    pricing_rules = io_helper.get_pricing_rules_dict()

    invoices = io_helper.get_invoices()

    statements = statement_generator.generate_statement(invoices, plays, pricing_rules)

    print(io_helper.text_statements_render(statements))

if __name__ == "__main__":
    main()
