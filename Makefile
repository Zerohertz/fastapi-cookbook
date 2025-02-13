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

.PHONY: alembic
alembic:
	@uv sync
	@export DESCRIPTION=$$(cat README.md) && \
		set -o allexport && \
		source envs/$${ENV,,}.env && \
		set +o allexport && \
		if [ "$(revision)" = "downgrade" ]; then \
			uv run alembic downgrade base; \
		elif [ -z "$(revision)" ]; then \
			uv run alembic upgrade head; \
		else \
			uv run alembic revision --autogenerate -m "$(revision)"; \
		fi

.PHONY: test
test:
	uv sync --group test
	export DESCRIPTION=$$(cat README.md) && \
		PYTHONASYNCIODEBUG=1 uv run pytest -vv \
		--cov=app --cov-branch --cov-report=xml \
		--junitxml=junit.xml -o junit_family=legacy

.PHONY: dev
dev:
	export DESCRIPTION=$$(cat README.md) && \
		source ./envs/dev.env && \
		PYTHONASYNCIODEBUG=1 uv run uvicorn app.main:app --host 0.0.0.0 --port $${PORT} \
		--loop uvloop --http httptools \
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

.PHONY: deploy
deploy:
ifndef tag
	$(error tag is not set)
endif
	echo $(tag)
	sed -i 's|version = [^ ]*|version = "$(shell echo $(tag) | sed 's/^v//')"|' pyproject.toml
	uv sync
	git add pyproject.toml
	git add uv.lock
	sed -i 's|zerohertzkr/fastapi-cookbook:[^ ]*|zerohertzkr/fastapi-cookbook:$(tag)|' k8s/postgresql/fastapi.yaml
	git add k8s/postgresql/fastapi.yaml
	sed -i 's|VERSION=[^ ]*|VERSION="$(tag)"|' k8s/postgresql/configmap.yaml
	git add k8s/postgresql/configmap.yaml
	sed -i 's|VERSION=[^ ]*|VERSION="$(tag)"|' envs/test.env
	git add envs/test.env
	git commit -m ":ship: release: $(tag)"
	git tag -a $(tag) -m ":ship: release: $(tag)"
	git push origin main
	git push origin $(tag)
