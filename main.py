import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from shared.infrastructure.database import Database
from domains.sales.interfaces import client as sales_client
from domains.analytics.interfaces import cli as analytics_cli


load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH", "data/theater.db"))
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
REPO_TYPE = os.getenv("REPOSITORY_TYPE", "json")


def run_sales(args):
    database = Database(DB_PATH) if REPO_TYPE == "sql" else None
    sales_client.run(REPO_TYPE, database, DATA_DIR, args)


def run_analytics(args):
    analytics_cli.run(DB_PATH, args)


DOMAINS = {
    "sales": run_sales,
    "analytics": run_analytics,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in DOMAINS:
        print(f"Usage: python3 main.py <domain> [command]")
        print(f"Domains: {', '.join(DOMAINS.keys())}")
        sys.exit(1)
    
    domain = sys.argv[1]
    DOMAINS[domain](sys.argv[2:])


if __name__ == "__main__":
    main()
