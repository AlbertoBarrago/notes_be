.PHONY: dev test lint migrate migration install docker-up docker-rebuild

dev:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

test:
	uv run pytest -p no:warnings test/**/*.py

lint:
	uv run pylint app/

migrate:
	uv run alembic upgrade head

migration:
	uv run alembic revision --autogenerate -m "$(msg)"

install:
	uv sync

docker-up:
	docker-compose up -d

docker-rebuild:
	docker-compose down && docker-compose up --build
