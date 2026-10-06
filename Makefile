.PHONY: help install install-dev format lint type test clean all pre-commit-setup

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies
	uv sync --all-extras

install-dev:  ## Install base + dev dependencies only
	uv sync --extra dev

format:  ## Format code with ruff
	uv run ruff format .
	uv run ruff check --fix .

lint:  ## Check code with ruff (no fixes)
	uv run ruff check .

type:  ## Run mypy type checking
	uv run mypy SRC/utils/ TESTS/

test:  ## Run pytest tests
	uv run pytest TESTS/ -v

clean:  ## Remove cache and temp files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

all: format lint type test  ## Run all checks

pre-commit-setup:  ## Install pre-commit hooks
	uv run pre-commit install
