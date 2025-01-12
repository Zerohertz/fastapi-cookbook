SHELL := /bin/bash
.ONESHELL:

define init
@set -e
set -x
if [ "$$(which python)" != "$$(pwd)/.venv/bin/python" ]; then
    if [ ! -d ".venv" ]; then
        uv sync
    fi
	source .venv/bin/activate
fi
endef

.PHONY: lint
lint:
	$(init)
	# Static Typing
	mypy app
	# Linting
	ruff check app
	pylint -r n app
	flake8 app
	# Formatting
	isort app --check-only
	black app --check

.PHONY: test
test:
	$(init)
	pytest app --cov-branch --cov-report=xml

.PHONY: local
local:
	$(init)
	source ./envs/local.env
	uvicorn app.main:app --host 0.0.0.0 --port $${PORT} --env-file ./envs/local.env --reload --log-level debug

.PHONY: prod
prod:
	$(init)
	uvicorn app.main:app --host 0.0.0.0 --env-file ./envs/prod.env
