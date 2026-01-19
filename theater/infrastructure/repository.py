import json
import logging
from pathlib import Path
from typing import Dict, List
from theater.models.invoice import Invoice, Performance
from theater.models.play import Play
from theater.models.rules import PricingRules

class Repository:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

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

    def _load_json(self, filename: str):
        file_path = self.data_dir / filename
        try:
            with file_path.open(encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON format in file: {file_path}")
            raise
        except OSError as e:
            logging.error(f"OS error reading file {file_path}: {e}")
            raise
