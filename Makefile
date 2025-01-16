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
	export DESCRIPTION=$$(cat README.md) && \
		uv run pytest \
		--cov=app --cov-branch --cov-report=xml \
		--junitxml=junit.xml -o junit_family=legacy

.PHONY: dev
dev:
	export DESCRIPTION=$$(cat README.md) && \
		source ./envs/dev.env && \
		uv run uvicorn app.main:app --host 0.0.0.0 --port $${PORT} \
		--env-file ./envs/dev.env \
		--proxy-headers --forwarded-allow-ips='*' \
		--reload

.PHONY: prod
prod:
	export DESCRIPTION=$$(cat README.md) && \
		uv run uvicorn app.main:app --host 0.0.0.0 \
		--env-file ./envs/prod.env \
		--proxy-headers --forwarded-allow-ips='*'

.PHONY: k8s
k8s:
	kubectl delete -n fastapi -f k8s/dev.yaml 2> /dev/null || echo "Not deployed to the dev environment! 🌎"
	kubectl apply -n fastapi -f k8s/secrets.yaml
	kubectl apply -n fastapi -f k8s/dev.yaml

.PHONY: exec
exec:
	kubectl exec -it -n fastapi deploy/fastapi-dev -- zsh
