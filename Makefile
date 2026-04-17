# Variables
COMPOSE_FILE = docker-compose.yml
LOGIC_SERVICE = kafka-logic
DB_SERVICE = timescaledb

.PHONY: help build up down restart logs db-shell kafka-ui-info clean

help: ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build and start the stack in the background
	docker-compose up -d --build

up: ## Start existing containers
	docker-compose up -d

down: ## Stop and remove containers
	docker-compose down

restart: ## Restart the Kafka logic app
	docker-compose restart $(LOGIC_SERVICE)

logs: ## Follow logs from the Kafka logic application
	docker-compose logs -f $(LOGIC_SERVICE)

db-shell: ## Access the TimescaleDB interactive terminal
	docker exec -it $(DB_SERVICE) psql -U postgres

kafka-ui-info: ## Print access URLs for the management UIs
	@echo "\033[32mKafka UI:\033[0m http://localhost:8080"
	@echo "\033[32mGrafana:\033[0m  http://localhost:3000"

clean: ## Remove containers, images, and volumes (Fresh start)
	docker-compose down -v
	@echo "\033[31mCleanup complete. All data volumes removed.\033[0m"