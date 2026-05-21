
create_network:
	@echo "Creating network..."
	@docker network create control_network || true

start_env:
	@echo "Installing environment..."
	@docker-compose -f docker-compose.env.yml --env-file control_host.env up -d --build

stop_env:
	@echo "Stopping environment..."
	@docker-compose -f docker-compose.env.yml --env-file control_host.env down

stop_manager:
	@echo "Stopping manager..."
	@docker-compose -f docker-compose.manager.yml --env-file control_host.env down

start_manager:
	@echo "Starting manager..."
	@docker-compose -f docker-compose.manager.yml --env-file control_host.env up -d

start_all: create_network start_env start_manager
