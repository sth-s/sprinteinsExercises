import os
from typing import List
from domains.sales.models.statement import Statement

class TextRenderer:
    def text_statements_render(self, statements: List[Statement]) -> str:
        return "".join(self._render_statement(s) for s in statements)

    def _render_statement(self, statement: Statement) -> str:
        lines = [f"Statement for {statement.customer}"]
        
        for result in statement.performance_details:
            lines.append(f"  {result.play.name}: {self._format_currency(result.amount)} ({result.audience} seats)")
            
        lines.append(f"Amount owed is {self._format_currency(statement.total_amount)}")
        lines.append(f"You earned {statement.total_credits} credits")
        return os.linesep.join(lines) + os.linesep

    def _format_currency(self, amount: int) -> str:
        return "${:,.2f}".format(amount / 100)