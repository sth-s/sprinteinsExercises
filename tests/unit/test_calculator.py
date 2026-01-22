import pytest
from domains.sales.domain.calculators.tragedy_calculator import TragedyCalculator
from domains.sales.domain.calculators.comedy_calculator import ComedyCalculator
from domains.sales.domain.calculators.calculator_factory import CalculatorFactory
from domains.sales.models.invoice import Performance
from domains.sales.models.play import Play


def test_tragedy_calculation():
    calculator = TragedyCalculator()
    performance = Performance(play_id="hamlet", audience=55)
    play = Play(play_id="hamlet", name="Hamlet", type="tragedy")
    
    result = calculator.calculate(performance, play)
    
    assert result.amount == 65000
    assert result.credits == 25


def test_comedy_calculation():
    calculator = ComedyCalculator()
    performance = Performance(play_id="as-like", audience=35)
    play = Play(play_id="as-like", name="As You Like It", type="comedy")
    
    result = calculator.calculate(performance, play)
    
    assert result.amount == 58000
    assert result.credits == 12


def test_tragedy_small_audience():
    calculator = TragedyCalculator()
    performance = Performance(play_id="othello", audience=15)
    play = Play(play_id="othello", name="Othello", type="tragedy")
    
    result = calculator.calculate(performance, play)
    
    assert result.amount == 40000
    assert result.credits == 0


def test_calculator_factory_tragedy():
    calculator = CalculatorFactory.get_calculator("tragedy")
    assert isinstance(calculator, TragedyCalculator)


def test_calculator_factory_comedy():
    calculator = CalculatorFactory.get_calculator("comedy")
    assert isinstance(calculator, ComedyCalculator)


def test_calculator_factory_unknown_type():
    with pytest.raises(ValueError, match="unknown type: musical"):
        CalculatorFactory.get_calculator("musical")
