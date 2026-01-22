import pytest
from pathlib import Path
from unittest.mock import Mock
from theater.application.statement_service import StatementService
from theater.infrastructure.repository import Repository
from theater.infrastructure.text_renderer import TextRenderer
from theater.domain.statements_generator_service import StatementsGeneratorService
from theater.models.invoice import Invoice, Performance
from theater.models.play import Play
from theater.models.rules import PricingRules, AmountRules, CreditsRules


@pytest.fixture
def mock_repository():
    repo = Mock(spec=Repository)
    
    invoices = [
        Invoice(
            customer="TestCo",
            performances=[
                Performance(play_id="hamlet", audience=55),
                Performance(play_id="as-like", audience=35)
            ]
        )
    ]
    
    plays = {
        "hamlet": Play(play_id="hamlet", name="Hamlet", type="tragedy"),
        "as-like": Play(play_id="as-like", name="As You Like It", type="comedy")
    }
    
    rules = {
        "tragedy": PricingRules(
            amount=AmountRules(
                base_amount=40000,
                base_coefficient=0,
                audience_threshold_amount=30,
                threshold_amount=0,
                threshold_coefficient=1000
            ),
            credits=CreditsRules(
                audience_threshold_credits=30,
                credits_divisor=None
            )
        ),
        "comedy": PricingRules(
            amount=AmountRules(
                base_amount=30000,
                base_coefficient=300,
                audience_threshold_amount=20,
                threshold_amount=10000,
                threshold_coefficient=500
            ),
            credits=CreditsRules(
                audience_threshold_credits=32,
                credits_divisor=5
            )
        )
    }
    
    repo.get_invoices.return_value = invoices
    repo.get_plays_dict.return_value = plays
    repo.get_pricing_rules_dict.return_value = rules
    
    return repo


def test_generate_statements_with_mock(mock_repository):
    generator = StatementsGeneratorService()
    renderer = TextRenderer()
    service = StatementService(mock_repository, generator, renderer)
    
    result = service.generate_statements()
    
    assert "Statement for TestCo" in result
    assert "Hamlet:" in result
    assert "As You Like It:" in result
    assert "$1,230.00" in result
    assert "35 credits" in result


def test_full_render_with_mock(mock_repository):
    generator = StatementsGeneratorService()
    renderer = TextRenderer()
    service = StatementService(mock_repository, generator, renderer)
    
    result = service.generate_statements()
    
    assert "Statement for TestCo" in result
    assert "Hamlet:" in result
    assert "As You Like It:" in result
