# Makefile for common Docker Compose + Airflow tasks
# Usage: `make <target>`

.DEFAULT_GOAL := help

COMPOSE := docker-compose
SERVICE ?= airflow-webserver

.PHONY: help build up down restart ps logs exec db-upgrade create-user

help:
	@echo "Makefile - common commands"
	@echo "  make build                  Build docker images (no cache)"
	@echo "  make up                     Start all services (detached)"
	@echo "  make down                   Stop and remove containers + volumes"
	@echo "  make restart                Restart the stack"
	@echo "  make ps                     Show docker-compose ps"
	@echo "  make logs SERVICE=<svc>     Follow logs for service (default: $(SERVICE))"
	@echo "  make exec SERVICE=<svc> CMD=\"bash\"  Exec a command in a running service"
	@echo "  make db-upgrade             Run 'airflow db upgrade' inside airflow-init container"
	@echo "  make create-user            Create an Airflow user (pass USERNAME, PASSWORD, EMAIL optionally)"

build:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

restart: down up

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f $(SERVICE)

exec:
	@if [ -z "$(SERVICE)" ]; then echo "Set SERVICE=<service> and CMD='<command>'"; exit 1; fi; \
	@if [ -z "$(CMD)" ]; then echo "Set CMD='<command>' (e.g. CMD=\"bash\")"; exit 1; fi; \
	$(COMPOSE) exec $(SERVICE) sh -c '$(CMD)'

# Run Airflow DB upgrade (useful if you prefer 'upgrade' over the compose's configured command)
db-upgrade:
	$(COMPOSE) run --rm airflow-init airflow db upgrade

# Create an Airflow user. Optionally pass USERNAME, PASSWORD, EMAIL, FIRSTNAME, LASTNAME
create-user:
	@echo "Creating Airflow user (defaults: airflow / airflow / admin@example.com)"; \
	$(COMPOSE) run --rm airflow-init bash -c "airflow users create --username ${USERNAME:-airflow} --firstname ${FIRSTNAME:-Airflow} --lastname ${LASTNAME:-Admin} --role Admin --email ${EMAIL:-admin@example.com} --password ${PASSWORD:-airflow}"
