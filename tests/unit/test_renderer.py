import pytest
from domains.sales.infrastructure.text_renderer import TextRenderer
from domains.sales.models.statement import Statement, PerformanceResult
from domains.sales.models.play import Play


def test_render_single_statement():
    renderer = TextRenderer()
    
    play = Play(play_id="hamlet", name="Hamlet", type="tragedy")
    perf_result = PerformanceResult(amount=65000, credits=25, play=play, audience=55)
    statement = Statement(
        customer="BigCo",
        total_amount=65000,
        total_credits=25,
        performance_details=[perf_result]
    )
    
    result = renderer.text_statements_render([statement])
    
    assert "Statement for BigCo" in result
    assert "Hamlet: $650.00 (55 seats)" in result
    assert "Amount owed is $650.00" in result
    assert "You earned 25 credits" in result


def test_format_currency():
    renderer = TextRenderer()
    
    assert renderer._format_currency(65000) == "$650.00"
    assert renderer._format_currency(100) == "$1.00"
    assert renderer._format_currency(123456) == "$1,234.56"
