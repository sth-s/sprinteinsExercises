import polars as pl
from pathlib import Path


class DataLoader:
    def __init__(self, db_path: Path):
        self.db_uri = f"sqlite:///{db_path.resolve()}"
    
    def load_performances_with_details(self) -> pl.DataFrame:
        query = """
            SELECT 
                c.name as customer,
                p.name as play_name,
                pt.name as play_type,
                perf.audience
            FROM performances perf
            JOIN invoices i ON perf.invoice_id = i.id
            JOIN customers c ON i.customer_id = c.id
            JOIN plays p ON perf.play_id = p.id
            JOIN play_types pt ON p.type_id = pt.id
        """
        return pl.read_database_uri(query, self.db_uri)
    
    def load_all_plays(self) -> pl.DataFrame:
        query = "SELECT name as play_name FROM plays ORDER BY name"
        return pl.read_database_uri(query, self.db_uri)
