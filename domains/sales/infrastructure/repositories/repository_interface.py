from abc import ABC, abstractmethod
from typing import List, Dict
from pathlib import Path

from domains.sales.models.invoice import Invoice
from domains.sales.models.play import Play

class RepositoryInterface(ABC):
    
    @abstractmethod
    def get_invoices(self) -> List[Invoice]:
        pass

    @abstractmethod
    def get_plays_dict(self) -> Dict[str, Play]:
        pass

    @abstractmethod
    def save_report(self, report: str, output_file: Path):
        pass
