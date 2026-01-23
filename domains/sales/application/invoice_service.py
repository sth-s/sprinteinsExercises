from typing import List, Dict
from domains.sales.infrastructure.repositories.repository_interface import RepositoryInterface
from domains.sales.domain.statements_generator_service import StatementsGeneratorService
from domains.sales.infrastructure.text_renderer import TextRenderer
from domains.sales.models.invoice import Invoice, Performance


class InvoiceService:
    def __init__(
        self, 
        repository: RepositoryInterface, 
        generator: StatementsGeneratorService, 
        renderer: TextRenderer
    ):
        self._repository = repository
        self._generator = generator
        self._renderer = renderer
    
    def add_invoice(self, customer: str, performances: List[dict]) -> str:
        invoice_id = self._repository.add_invoice(customer, performances)
        
        invoice = Invoice(
            customer=customer,
            performances=[
                Performance(play_id=p["play_id"], audience=p["audience"])
                for p in performances
            ]
        )
        plays = self._repository.get_plays_dict()
        
        statements = self._generator.generate_statements([invoice], plays)
        
        return self._renderer.text_statements_render(statements)
