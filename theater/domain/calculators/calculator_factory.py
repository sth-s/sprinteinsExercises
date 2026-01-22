from .calculator_interface import IPerformanceCalculator
from .tragedy_calculator import TragedyCalculator
from .comedy_calculator import ComedyCalculator


class CalculatorFactory:
    
    _calculators: dict[str, type[IPerformanceCalculator]] = {
        "tragedy": TragedyCalculator,
        "comedy": ComedyCalculator,
    }
    
    @classmethod
    def get_calculator(cls, play_type: str) -> IPerformanceCalculator:
        calculator_class = cls._calculators.get(play_type)
        if not calculator_class:
            raise ValueError(f"unknown type: {play_type}")
        return calculator_class()