import json
import os
from pathlib import Path
from models.invoice import Invoice, Performance
from models.play import Play
from models.pricing_rules import PricingRules
from models.statement import Statement
from typing import Dict, List

class IOHelper:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

# json reader

    def get_invoices(self) -> List[Invoice]:
        data = self._load_json("invoices.json")
        invoices = []
        for invoice_data in data:
            performances = [
                Performance(play_id=p["playID"], audience=p["audience"])
                for p in invoice_data["performances"]
            ]
            invoices.append(Invoice(customer=invoice_data["customer"], performances=performances))
        return invoices

    def get_plays_dict(self) -> Dict[str, Play]:
        data = self._load_json("plays.json")
        return {
            play_id: Play(play_id=play_id, **play_data)
            for play_id, play_data in data.items()
        }

    def get_pricing_rules_dict(self) -> Dict[str, PricingRules]:
        data = self._load_json("pricing_rules.json")
        return {
            play_type: PricingRules(**rules_data)
            for play_type, rules_data in data.items()
        }

    def _load_json(self, filename: str) -> dict:
        try:
            with (self.data_dir / filename).open(encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found in {self.data_dir}")
        except Exception as e:
            raise Exception(f"Failed to read file {filename}: {e}")

# text renderer

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