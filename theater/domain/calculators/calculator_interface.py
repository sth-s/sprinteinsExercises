from abc import ABC, abstractmethod
from theater.models.invoice import Performance
from theater.models.play import Play
from theater.models.statement import PerformanceResult


class IPerformanceCalculator(ABC):
    
    @abstractmethod
    def calculate(self, performance: Performance, play: Play) -> PerformanceResult:
        pass
