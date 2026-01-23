import polars as pl
from pathlib import Path


class ReportWriter:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
    
    def save(self, df: pl.DataFrame, name: str):
        path = self.data_dir / f"{name}.parquet"
        df.write_parquet(path)
        print(f"Saved to {path}")
