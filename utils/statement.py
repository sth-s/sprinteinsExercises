from models.invoice import Invoice, Performance 
from models.play import Play
from models.pricing_rules import AmountRules, CreditsRules, PricingRules
from models.statement import PerformanceResult, Statement
from typing import Dict, List

class StatementGenerator:
    
    def generate_statement(self, invoices: List[Invoice], plays: Dict[str, Play], pricing_rules: Dict[str, PricingRules]) -> List[Statement]:
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
                    
                result = self._calculate(perf, play, rules)
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

    def _calculate(self, performance: Performance, play: Play, rules: PricingRules) -> PerformanceResult:
        amount = self._calculate_amount(performance.audience, rules.amount)
        credits = self._calculate_credits(performance.audience, rules.credits)
        return PerformanceResult(amount=amount, credits=credits, play=play, audience=performance.audience)

    def _calculate_amount(self, audience: int, rules: AmountRules) -> int:
        amount = rules.base_amount
        amount += rules.base_coefficient * audience
        
        if audience > rules.audience_threshold_amount:
            amount += rules.threshold_amount
            amount += rules.threshold_coefficient * (audience - rules.audience_threshold_amount)
            
        return amount

    def _calculate_credits(self, audience: int, rules: CreditsRules) -> int:
        credits = max(audience - rules.audience_threshold_credits, 0)
        
        if rules.credits_divisor:
            credits += audience // rules.credits_divisor
        
        return credits