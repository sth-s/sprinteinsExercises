import pytest
from pathlib import Path
from unittest.mock import Mock
from domains.sales.application.statement_service import StatementService
from domains.sales.infrastructure.repositories.repository_interface import RepositoryInterface
from domains.sales.infrastructure.text_renderer import TextRenderer
from domains.sales.domain.statements_generator_service import StatementsGeneratorService
from domains.sales.models.invoice import Invoice, Performance
from domains.sales.models.play import Play


@pytest.fixture
def mock_repository():
    repo = Mock(spec=RepositoryInterface)
    
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
    
    repo.get_invoices.return_value = invoices
    repo.get_plays_dict.return_value = plays
    
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
    assert "37 credits" in result


def test_full_render_with_mock(mock_repository):
    generator = StatementsGeneratorService()
    renderer = TextRenderer()
    service = StatementService(mock_repository, generator, renderer)
    
    result = service.generate_statements()
    
    assert "Statement for TestCo" in result
    assert "Hamlet:" in result
    assert "As You Like It:" in result
