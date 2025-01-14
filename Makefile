SHELL := /bin/bash

.PHONY: lint
lint:
	# Static Typing
	uv run mypy app
	# Linting
	uv run ruff check app
	uv run pylint -r n app
	# Formatting
	uv run isort app --check-only
	uv run black app --check

.PHONY: test
test:
	uv run pytest --cov=app --cov-branch --cov-report=xml --junitxml=junit.xml -o junit_family=legacy

.PHONY: local
local:
	source ./envs/local.env
	uv run uvicorn app.main:app --host 0.0.0.0 --port $${PORT} --env-file ./envs/local.env --reload --log-level debug

.PHONY: prod
prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --env-file ./envs/prod.env
