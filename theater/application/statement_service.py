import logging
from pathlib import Path
from typing import List
from theater.infrastructure.repository import Repository
from theater.domain.statements_generator_service import StatementsGeneratorService
from theater.infrastructure.text_renderer import TextRenderer
from theater.models.statement import Statement

class StatementService:
    def generate_statements(self, data_dir: Path, output_file: Path = None) -> List[Statement]:
        try:
            repository = Repository(data_dir)

            invoices = repository.get_invoices()
            plays = repository.get_plays_dict()
            pricing_rules = repository.get_pricing_rules_dict()

            statements = StatementsGeneratorService().generate_statements(invoices, plays, pricing_rules)
            
            result = TextRenderer().text_statements_render(statements)

            if output_file:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(result, encoding='utf-8')
                logging.info(f"Saved to {output_file}")
                return statements
            else:
                print(result, end='')
                return statements

        except Exception as e:
            logging.error(f"Error: {e}")
            raise
            
