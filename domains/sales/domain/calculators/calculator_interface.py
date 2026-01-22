from abc import ABC, abstractmethod
from domains.sales.models.invoice import Performance
from domains.sales.models.play import Play
from domains.sales.models.statement import PerformanceResult


class PerformanceCalculatorInterface(ABC):
    
    @abstractmethod
    def calculate(self, performance: Performance, play: Play) -> PerformanceResult:
        pass
