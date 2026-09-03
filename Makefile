.PHONY: up down build logs ps restart clean

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

# Usage: make logs [s=<service>]
logs:
	docker compose logs -f $(s)

ps:
	docker compose ps

restart:
	docker compose restart $(s)

# Tears the stack down and removes named volumes (e.g. ollama-data).
clean:
	docker compose down -v
