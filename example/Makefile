.default_goal := help

.PHONY: help
help:  ## show this help.
	@grep -e '^\s+:.*?## .*$$' $(firstword $(makefile_list)) | \
		awk 'begin {fs = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: hello-world
hello-world: ## set up the local environment (e.g. install git hooks)
	docker compose up --build hello-world

.PHONY: down
down: ## Stop and remove all the Docker services, volumes and networks
	docker compose down -v --remove-orphans
