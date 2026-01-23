from typing import Dict
from .interface import AnalyticsCalculator
from .tragedy import TragedyAnalyticsCalculator
from .comedy import ComedyAnalyticsCalculator


class CalculatorFactory:
    _calculators: Dict[str, AnalyticsCalculator] = {
        "tragedy": TragedyAnalyticsCalculator(),
        "comedy": ComedyAnalyticsCalculator(),
    }

    @classmethod
    def get_calculator(cls, play_type: str) -> AnalyticsCalculator:
        return cls._calculators.get(play_type)
        
    @classmethod
    def get_all(cls) -> Dict[str, AnalyticsCalculator]:
        return cls._calculators
