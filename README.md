# Theater Billing System

Refactored theater statement generator with clean architecture.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Tests

```bash
# Simple tests
pytest tests/unit/ -v
```

## Usage

```bash
# Print to console
python3 main.py generate-statements

# Save to file
python3 main.py generate-statements -o output.txt
```

## Structure

- `theater/models/` - Domain models (Pydantic)
- `theater/domain/` - Business logic
- `theater/application/` - Services
- `theater/infrastructure/` - Data access & rendering
- `theater/interfaces/` - CLI client
- `data/` - JSON data files
