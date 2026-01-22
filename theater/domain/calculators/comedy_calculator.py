from .calculator_interface import PerformanceCalculatorInterface
from theater.models.invoice import Performance
from theater.models.play import Play
from theater.models.statement import PerformanceResult


class ComedyCalculator(PerformanceCalculatorInterface):
    
    BASE_AMOUNT = 30000
    BASE_PER_PERSON = 300
    AUDIENCE_THRESHOLD = 20
    THRESHOLD_BONUS = 10000
    EXTRA_PER_PERSON = 500
    CREDITS_THRESHOLD = 30
    CREDITS_DIVISOR = 5
    
    def calculate(self, performance: Performance, play: Play) -> PerformanceResult:
        amount = self._calculate_amount(performance.audience)
        credits = self._calculate_credits(performance.audience)
        return PerformanceResult(
            amount=amount,
            credits=credits,
            play=play,
            audience=performance.audience
        )
    
    def _calculate_amount(self, audience: int) -> int:
        amount = self.BASE_AMOUNT + (self.BASE_PER_PERSON * audience)
        if audience > self.AUDIENCE_THRESHOLD:
            amount += self.THRESHOLD_BONUS
            amount += self.EXTRA_PER_PERSON * (audience - self.AUDIENCE_THRESHOLD)
        return amount
    
    def _calculate_credits(self, audience: int) -> int:
        credits = max(audience - self.CREDITS_THRESHOLD, 0)
        credits += audience // self.CREDITS_DIVISOR
        return credits
