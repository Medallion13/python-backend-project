# Makefile

.PHONY: install lint test test-watch format clean run help

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run mypy .

test:
	poetry run pytest tests/ -v --cov=app

test-watch:
	poetry run pytest-watch tests/

format:
	poetry run ruff check --fix app/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	poetry run uvicorn app.main:app --reload

run-docker:
	docker-compose up -d

stop-docker:
	docker-compose down

help:
	@echo "Available commands:"
	@echo "  install     - Install project dependencies"
	@echo "  lint        - Lint the codebase"
	@echo "  test        - Run tests with coverage"
	@echo "  test-watch  - Run tests in watch mode"
	@echo "  format      - Format the codebase"
	@echo "  clean       - Clean up __pycache__ and .pyc files"
	@echo "  run         - Run the application with Uvicorn"
	@echo "  run-docker  - Start the docker-compose services"
	@echo "  stop-docker - Stops the docker containers"
	@echo "  help        - Show this help message"
