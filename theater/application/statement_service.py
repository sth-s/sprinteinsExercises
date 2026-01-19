from typing import List
from theater.infrastructure.repository import Repository
from theater.domain.statement_calculator import StatementCalculator
from theater.models.statement import Statement

class StatementService:
    def __init__(self, repository: Repository, calculator: StatementCalculator):
        self.repository = repository
        self.calculator = calculator

    def generate_statements(self) -> List[Statement]:
        invoices = self.repository.get_invoices()
        plays = self.repository.get_plays_dict()
        pricing_rules = self.repository.get_pricing_rules_dict()
        
        statements = []
        for invoice in invoices:
            total_amount = 0
            total_credits = 0
            performance_results = []
            
            for perf in invoice.performances:
                play = plays[perf.play_id]
                rules = pricing_rules.get(play.type)
                
                if not rules:
                    raise ValueError(f"unknown type: {play.type}")
                    
                result = self.calculator.calculate(perf, play, rules)
                performance_results.append(result)
                
                total_amount += result.amount
                total_credits += result.credits
                
            statements.append(
                Statement(
                    customer=invoice.customer,
                    total_amount=total_amount,
                    total_credits=total_credits,
                    performance_details=performance_results
                )
            )
        return statements
