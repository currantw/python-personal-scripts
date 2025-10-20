.PHONY: help install install-dev check-format fix-format check-lint fix-lint check-type check-all fix-all test test-cov clean pre-commit

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Install dependencies
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Check code quality
check-format:
	ruff format --check --diff .

check-lint:
	ruff check .

check-type:
	mypy --strict .

check-all:
	make check-format
	make check-lint
	make check-type

# Fix code quality issues
fix-format:
	ruff format .

fix-lint:
	ruff check --fix .

fix-all:
	make fix-format
	make fix-lint

# Run tests
test:
	pytest

test-cov:
	pytest --cov=lib --cov-report=html --cov-report=term-missing --cov-report=xml --cov-fail-under=100

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage/ .pytest_cache/ .mypy_cache/

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files
