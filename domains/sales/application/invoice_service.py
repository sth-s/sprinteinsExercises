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
        self.repository = repository
        self.generator = generator
        self.renderer = renderer
    
    def add_invoice(self, customer: str, performances: List[dict]) -> str:
        plays = self.repository.get_plays_dict()
        
        invoice = Invoice(
            customer=customer,
            performances=[
                Performance(play_id=p["play_id"], audience=p["audience"])
                for p in performances
            ]
        )
        
        invoice_id = self.repository.add_invoice(invoice)
        
        statements = self.generator.generate_statements([invoice], plays)
        
        return self.renderer.text_statements_render(statements)
