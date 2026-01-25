# Theater Billing System

Theater statement generator with clean architecture.

**Features:**
- Two domains: **Sales** (transactional) and **Analytics** (Polars columnar)
- SQLite database with SQLModel ORM
- Abstract interfaces for repositories and calculators
- Factory pattern for dependency injection

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
```

## Quick Start

```bash
# Initialize database
python3 -m scripts.init_db
python3 -m scripts.seed_data  # optional: add test data

# Sales: generate billing statements 
# Not recommended to run this command, as it have to be too slow
# Use analytics domain instead
python3 main.py sales generate-statements
python3 main.py sales generate-statements -o output.txt

# Sales: add new invoice (transactional)
python3 main.py sales add-invoice \
  -c "TestCustomer" \
  -p '[{"play_id": "hamlet", "audience": 55}]'

# Analytics: calculate and save customer reports
python3 main.py analytics generate-report --name customer_reports
# Saves to data/customer_reports.parquet, prints top 5

# Analytics: print text report from parquet
python3 main.py analytics print-text-report --name customer_reports [--save-as result]
# Loads data/customer_reports.parquet, prints formatted statement
```

## Configuration

Settings in `.env`:

| Variable | Description | Values |
|----------|-------------|--------|
| `REPOSITORY_TYPE` | Data source | `json` or `sql` |
| `DB_PATH` | SQLite path | `data/theater.db` |
| `DATA_DIR` | Data folder | `data` |

## Tests

```bash
pytest tests/unit/ -v
```

## Architecture

```
domains/
├── sales/              # Transactional billing
│   ├── models/         # Domain models (Pydantic)
│   ├── domain/         # Business logic + calculators
│   ├── application/    # Services
│   ├── infrastructure/ # Repositories (JSON/SQL)
│   └── interfaces/     # CLI client
│
└── analytics/          # Read-only Polars analytics
    ├── domain/         # Calculator strategies (Polars Expr)
    ├── services/       # RevenueService (DataFrame in/out)
    ├── infrastructure/ # AnalyticsRepository (DataLoader/ReportWriter combined)
    └── interfaces/     # CLI (top 5 + save)

shared/
└── infrastructure/     # Database connection

scripts/
├── init_db.py          # Create DB from JSON
└── seed_data.py        # Additional test data
```
