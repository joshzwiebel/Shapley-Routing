# Shapley-Routing

## Installation

:one: Install [Poetry](https://python-poetry.org/):

```bash
pip install poetry
```

:two: Install dependencies:

```bash
poetry install
```

## Testing

### Run style check

```bash
poetry run flake8 .
poetry run black .
```

### Running unit tests

```bash
poetry run pytest -v .
```

### Running unit tests with coverage

```bash
poetry run coverage run -m pytest -v .
poetry run coverage report -m
```
