import json
import logging
from pathlib import Path
from typing import Dict, List

from domains.sales.infrastructure.repositories.repository_interface import RepositoryInterface
from domains.sales.models.invoice import Invoice, Performance
from domains.sales.models.play import Play

class JSONRepository(RepositoryInterface):
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

    def save_report(self, report: str, output_file: Path):
        try:
            file_path = self.data_dir / output_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(report, encoding='utf-8')
            logging.info(f"Saved to {file_path}")
        except OSError as e:
            logging.error(f"OS error writing file {file_path}: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error writing file {file_path}: {e}")
            raise

    def _load_json(self, filename: str):
        file_path = self.data_dir / filename
        try:
            with file_path.open(encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            raise
