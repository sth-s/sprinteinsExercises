import pytest
from theater.domain.statement_calculator import StatementCalculator
from theater.models.invoice import Performance
from theater.models.play import Play
from theater.models.rules import PricingRules, AmountRules, CreditsRules


def test_tragedy_calculation():
    calculator = StatementCalculator()
    performance = Performance(play_id="hamlet", audience=55)
    play = Play(play_id="hamlet", name="Hamlet", type="tragedy")
    rules = PricingRules(
        amount=AmountRules(
            base_amount=40000,
            base_coefficient=0,
            audience_threshold_amount=30,
            threshold_amount=0,
            threshold_coefficient=1000
        ),
        credits=CreditsRules(
            audience_threshold_credits=30,
            credits_divisor=1
        )
    )
    
    result = calculator.calculate(performance, play, rules)
    
    assert result.amount == 65000
    assert result.credits == 80


def test_comedy_calculation():
    calculator = StatementCalculator()
    performance = Performance(play_id="as-like", audience=35)
    play = Play(play_id="as-like", name="As You Like It", type="comedy")
    rules = PricingRules(
        amount=AmountRules(
            base_amount=30000,
            base_coefficient=300,
            audience_threshold_amount=20,
            threshold_amount=10000,
            threshold_coefficient=500
        ),
        credits=CreditsRules(
            audience_threshold_credits=20,
            credits_divisor=5
        )
    )
    
    result = calculator.calculate(performance, play, rules)
    
    assert result.amount == 58000
    assert result.credits == 22


def test_small_audience():
    calculator = StatementCalculator()
    performance = Performance(play_id="othello", audience=15)
    play = Play(play_id="othello", name="Othello", type="tragedy")
    rules = PricingRules(
        amount=AmountRules(
            base_amount=40000,
            base_coefficient=0,
            audience_threshold_amount=30,
            threshold_amount=0,
            threshold_coefficient=1000
        ),
        credits=CreditsRules(
            audience_threshold_credits=30,
            credits_divisor=1
        )
    )
    
    result = calculator.calculate(performance, play, rules)
    
    assert result.amount == 40000
    assert result.credits == 15
