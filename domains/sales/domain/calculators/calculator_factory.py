from .calculator_interface import PerformanceCalculatorInterface
from .tragedy_calculator import TragedyCalculator
from .comedy_calculator import ComedyCalculator


class CalculatorFactory:
    
    _calculators: dict[str, type[PerformanceCalculatorInterface]] = {
        "tragedy": TragedyCalculator,
        "comedy": ComedyCalculator,
    }
    
    @classmethod
    def get_calculator(cls, play_type: str) -> PerformanceCalculatorInterface:
        calculator_class = cls._calculators.get(play_type)
        if not calculator_class:
            raise ValueError(f"unknown type: {play_type}")
        return calculator_class()