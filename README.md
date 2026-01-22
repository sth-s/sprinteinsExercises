# Theater Billing System

Theater statement generator with clean architecture.

**Features:**
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

For SQL mode, initialize the database first:
```bash
python3 -m scripts.init_db
python3 -m scripts.seed_data  # optional: add test data

python3 main.py generate-statements
python3 main.py generate-statements -o output.txt
```

## Configuration

Settings in `.env`:

| Variable | Description | Values |
|----------|-------------|--------|
| `REPOSITORY_TYPE` | Data source | `json` or `sql` |
| `DB_PATH` | SQLite path | `data/theater.db` |
| `DATA_DIR` | Data folder | `data` |

## Database

Initialize DB (from JSON):
```bash
python3 -m scripts.init_db
```

Add test data:
```bash
python3 -m scripts.seed_data
```

## Usage

```bash
python3 main.py generate-statements
python3 main.py generate-statements -o output.txt
```

## Tests

```bash
pytest tests/unit/ -v
```

## Architecture

```
theater/
├── models/           # Domain models (Pydantic)
├── domain/           # Business logic
│   └── calculators/  # PerformanceCalculatorInterface + implementations
├── application/      # Services
├── infrastructure/   
│   └── repositories/ # RepositoryInterface + JSON/SQL implementations
└── interfaces/       # CLI client

shared/
└── infrastructure/   # Database connection

scripts/
├── init_db.py        # Create DB from JSON
└── seed_data.py      # Additional test data
```

## Abstractions

- `RepositoryInterface` — data access abstraction (JSON/SQL)
- `PerformanceCalculatorInterface` — calculators for different play types
- `RepositoryFactory` / `CalculatorFactory` — factories for creating implementations
