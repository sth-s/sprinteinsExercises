from theater.models.invoice import Performance
from theater.models.play import Play
from theater.models.rules import AmountRules, CreditsRules, PricingRules
from theater.models.statement import PerformanceResult

class StatementCalculator:
    def calculate(self, performance: Performance, play: Play, rules: PricingRules) -> PerformanceResult:
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
