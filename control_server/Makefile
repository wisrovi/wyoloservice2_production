
create_network:
	@echo "Creating network..."
	@docker network create control_network || true

start_env:
	@echo "Installing environment..."
	@docker-compose -f docker-compose.env.yml --env-file control_host.env up -d --build

stop_env:
	@echo "Stopping environment..."
	@docker-compose -f docker-compose.env.yml --env-file control_host.env down