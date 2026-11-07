.PHONY: install up down create-index load lint fmt typecheck test

install:
	poetry install

up:
	docker compose up -d

down:
	docker compose down

create-index:
	poetry run python -m src.loader --create-index

load:
	poetry run python -m src.loader

lint:
	oetry run ruff check src/

fmt:
	poetry run ruff format src/

typecheck:
	poetry run mypy src/

test:
	poetry run pytest tests/ -v
