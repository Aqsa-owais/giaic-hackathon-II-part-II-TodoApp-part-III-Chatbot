# MCP Server - Task Management Tools
# Development commands

.PHONY: help install install-dev test test-unit test-property test-integration lint format clean run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements-dev.txt

test:  ## Run all tests
	pytest tests/ -v

test-unit:  ## Run unit tests only
	pytest tests/unit/ -v

test-property:  ## Run property-based tests only
	pytest tests/property/ -v

test-integration:  ## Run integration tests only
	pytest tests/integration/ -v

test-coverage:  ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 src/ tests/
	mypy src/

format:  ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

format-check:  ## Check code formatting
	black --check src/ tests/
	isort --check-only src/ tests/

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

run:  ## Run the MCP server
	python -m src.server

setup-env:  ## Copy .env.example to .env
	cp .env.example .env
	@echo "Created .env file. Please update with your actual configuration."

validate:  ## Validate the setup
	python -c "from src.config import validate_settings; validate_settings(); print('Configuration is valid')"