import logging
from pathlib import Path
from typing import List
from domains.sales.infrastructure.repositories.repository_interface import RepositoryInterface
from domains.sales.domain.statements_generator_service import StatementsGeneratorService
from domains.sales.infrastructure.text_renderer import TextRenderer

class StatementService:

    def __init__(self, repository: RepositoryInterface, generator: StatementsGeneratorService, renderer: TextRenderer):
        self.repository = repository
        self.generator = generator
        self.renderer = renderer

    def generate_statements(self, output_file: Path = None) -> str:
        try:
            invoices = self.repository.get_invoices()
            plays = self.repository.get_plays_dict()

            statements = self.generator.generate_statements(invoices, plays)

            result = self.renderer.text_statements_render(statements)

            if output_file:
                self.repository.save_report(result, output_file)

            return result

        except Exception as e:
            logging.error(f"Error: {e}")
            raise
            
