.PHONY: install up down create-index load lint format typecheck test

install:      ; poetry install && poetry run pre-commit install
up:        ; docker compose up -d --wait
down:         ; docker compose down
create-index: ; poetry run python -m hr_analytics create-index
load:         ; poetry run python -m hr_analytics load
lint:         ; poetry run ruff check .
format:       ; poetry run ruff format .
test:         ; poetry run pytest
typecheck:    ; poetry run mypy src
