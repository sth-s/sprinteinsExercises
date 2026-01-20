from typing import List, Dict
from theater.domain.statement_calculator import StatementCalculator
from theater.models.invoice import Invoice
from theater.models.play import Play
from theater.models.rules import PricingRules
from theater.models.statement import Statement

class StatementsGeneratorService:
    def generate_statements(self, invoices: List[Invoice], plays: Dict[str, Play], pricing_rules: Dict[str, PricingRules]) -> List[Statement]:
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
                    
                result = StatementCalculator().calculate(perf, play, rules)
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