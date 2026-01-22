from .calculator_interface import PerformanceCalculatorInterface
from domains.sales.models.invoice import Performance
from domains.sales.models.play import Play
from domains.sales.models.statement import PerformanceResult


class TragedyCalculator(PerformanceCalculatorInterface):
    
    BASE_AMOUNT = 40000
    AUDIENCE_THRESHOLD = 30
    EXTRA_PER_PERSON = 1000
    CREDITS_THRESHOLD = 30
    
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
        amount = self.BASE_AMOUNT
        if audience > self.AUDIENCE_THRESHOLD:
            amount += self.EXTRA_PER_PERSON * (audience - self.AUDIENCE_THRESHOLD)
        return amount
    
    def _calculate_credits(self, audience: int) -> int:
        return max(audience - self.CREDITS_THRESHOLD, 0)
