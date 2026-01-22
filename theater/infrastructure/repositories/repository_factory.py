from pathlib import Path
from typing import Optional, Dict, Callable
from theater.infrastructure.repositories.repository_interface import RepositoryInterface
from theater.infrastructure.repositories.json_repository import JSONRepository
from theater.infrastructure.repositories.sql_repository import SQLRepository
from shared.infrastructure.database import Database


def _create_json(data_dir: Path, **kwargs) -> RepositoryInterface:
    return JSONRepository(data_dir)


def _create_sql(data_dir: Path, database: Optional[Database] = None, **kwargs) -> RepositoryInterface:
    if database is None:
        raise ValueError("Database instance is required for SQL repository")
    return SQLRepository(database.get_engine(), data_dir)


_REPOSITORY_CREATORS: Dict[str, Callable[..., RepositoryInterface]] = {
    'json': _create_json,
    'sql': _create_sql,
}


class RepositoryFactory:
    
    @staticmethod
    def create(repo_type: str, data_dir: Path, database: Optional[Database] = None) -> RepositoryInterface:
        creator = _REPOSITORY_CREATORS.get(repo_type)
        if not creator:
            raise ValueError(f"Unknown repository type: {repo_type}")
        return creator(data_dir=data_dir, database=database)
