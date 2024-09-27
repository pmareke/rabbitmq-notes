.default_goal := help

.PHONY: help
help:  ## show this help.
	@grep -e '^\s+:.*?## .*$$' $(firstword $(makefile_list)) | \
		awk 'begin {fs = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: up
up:
	docker compose up --build

.PHONY: down
down: ## Stop and remove all the Docker services, volumes and networks
	docker compose down -v --remove-orphans
