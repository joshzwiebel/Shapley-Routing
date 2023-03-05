# Shapley-Routing

Documentation can be found [here](https://joshzwiebel.github.io/Shapley-Routing/build/html/index.html).

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

## Docs

Docs can be built using the following commands:

```bash
cd docs/
poetry run make html
```
