from typing import List, Dict
from theater.domain.calculators import CalculatorFactory
from theater.models.invoice import Invoice
from theater.models.play import Play
from theater.models.statement import Statement

class StatementsGeneratorService:
    
    def __init__(self, calculator_factory: CalculatorFactory = None):
        self.calculator_factory = calculator_factory or CalculatorFactory()

    def generate_statements(self, invoices: List[Invoice], plays: Dict[str, Play]) -> List[Statement]:
        statements = []
        for invoice in invoices:
            total_amount = 0
            total_credits = 0
            performance_results = []
            
            for perf in invoice.performances:
                play = plays[perf.play_id]
                calculator = self.calculator_factory.get_calculator(play.type)
                result = calculator.calculate(perf, play)
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