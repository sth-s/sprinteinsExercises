import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from shared.infrastructure.database import Database
from theater.interfaces import client

def main():
    load_dotenv()
    repo_type = os.getenv("REPOSITORY_TYPE", "json")
    db_path = os.getenv("DB_PATH", "data/theater.db")
    data_dir = os.getenv("DATA_DIR", "data")
    
    database = None
    if repo_type == 'sql':
        database = Database(Path(db_path))
    
    try:
        client.run(repo_type, database, Path(data_dir))
    except Exception as e:
        print(f"Application Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
