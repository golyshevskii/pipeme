# System
ROOT := $(shell pwd)

path:
	export PYTHONPATH=$(ROOT)

# Lint
lint:
	cd .github/lint && poetry run black --config pyproject.toml ../../core/
	cd .github/lint && poetry run ruff check --config pyproject.toml --fix ../../core/

check-lint:
	cd .github/lint && poetry run black --config pyproject.toml --check ../../core/
	cd .github/lint && poetry run ruff check --config pyproject.toml ../../core/

# Dependencies
upreq:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Docker
prune-a:
	docker system prune -a

up:
	docker-compose up

up-b:
	docker-compose up --build

down:
	docker-compose down