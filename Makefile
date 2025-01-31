SHELL := /bin/bash

.PHONY: lint
lint:
	uv sync --all-groups
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
	uv sync --group test
	export DESCRIPTION=$$(cat README.md) && \
		uv run pytest -vv \
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
	kubectl delete -n fastapi -f k8s/postgresql/dev.yaml 2> /dev/null || echo "Not deployed to the dev environment! 🌎"
	kubectl apply -n fastapi -f k8s/postgresql/secrets.yaml
	kubectl apply -n fastapi -f k8s/postgresql/dev.yaml

.PHONY: exec
exec:
	kubectl exec -it -n fastapi deploy/fastapi-dev -- zsh

.PHONY: expose
expose:
	 kubectl expose -n fastapi po/postgresql-0 --port 5432 --type=NodePort

.PHONY: swagger
swagger:
	curl https://unpkg.com/swagger-ui-dist@5.18.3/swagger-ui-bundle.js > static/swagger-ui-bundle.js
	curl https://unpkg.com/swagger-ui-dist@5.18.3/swagger-ui.css > static/swagger-ui.css
	npx prettier --write "static/*.{js,css}"
