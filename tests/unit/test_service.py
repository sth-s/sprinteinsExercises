import pytest
from pathlib import Path
from unittest.mock import Mock
from theater.application.statement_service import StatementService
from theater.infrastructure.repository import Repository
from theater.infrastructure.text_renderer import TextRenderer
from theater.domain.statement_calculator import StatementCalculator
from theater.models.invoice import Invoice, Performance
from theater.models.play import Play
from theater.models.rules import PricingRules, AmountRules, CreditsRules


@pytest.fixture
def mock_repository(monkeypatch):
    repo = Repository(Path("data"))
    
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
    
    monkeypatch.setattr(repo, "get_invoices", lambda: invoices)
    monkeypatch.setattr(repo, "get_plays_dict", lambda: plays)
    monkeypatch.setattr(repo, "get_pricing_rules_dict", lambda: rules)
    
    return repo


def test_generate_statements_with_mock(mock_repository, monkeypatch):
    service = StatementService()
    
    monkeypatch.setattr("theater.application.statement_service.Repository", lambda x: mock_repository)
    
    statements = service.generate_statements(Path("data"))
    
    assert len(statements) == 1
    assert statements[0].customer == "TestCo"
    assert statements[0].total_amount == 123000
    assert statements[0].total_credits == 35
    assert len(statements[0].performance_details) == 2


def test_full_render_with_mock(mock_repository, monkeypatch):
    renderer = TextRenderer()
    service = StatementService()
    
    monkeypatch.setattr("theater.application.statement_service.Repository", lambda x: mock_repository)
    
    statements = service.generate_statements(Path("data"))
    result = renderer.text_statements_render(statements)
    
    assert "Statement for TestCo" in result
    assert "Hamlet:" in result
    assert "As You Like It:" in result
