# GraphID DB

A database project for graph identification and processing.

## Installation

### Using Poetry (Recommended)

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

### Alternative: Using pip

If you prefer not to use Poetry, you can install dependencies manually:
```bash
pip install pre-commit
```

## Development Setup

Install pre-commit hooks:
```bash
pre-commit install
pre-commit run --all-files
```

## Testing

### Using pytest (Recommended)

Run the tests using pytest:
```bash
poetry run pytest
```

### Using the test runner

Run the simple test runner:
```bash
python run_tests.py
```

## Usage

Activate the Poetry environment and run your scripts:
```bash
poetry shell
python -m filebase.your_script
```

## Project Structure

- `graphid-db/` - Main package containing the Finder class
- `filebase/` - Additional modules for data processing
- `tests/` - Test files
- `raw/` - Raw data storage

