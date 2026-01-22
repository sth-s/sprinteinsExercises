from pathlib import Path
from sqlmodel import create_engine, Session
from sqlalchemy.future import Engine

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        # sqlite:///absolute/path/to/file.db
        self.engine = create_engine(f"sqlite:///{self.db_path}")

    def get_session(self) -> Session:
        return Session(self.engine)
    
    def get_engine(self) -> Engine:
        return self.engine
