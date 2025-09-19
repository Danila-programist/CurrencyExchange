.PHONY: up down logs psql

include .env
export

init_env:
	@poetry shell

run:
	@python main.py

kill_proccess:
	@sudo lsof -ti :8000 | xargs -r sudo kill -9
	
env_file:
	@$(eval SHELL:=/bin/bash)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
	elif ! cmp -s .env .env.example; then \
		cp .env.example .env; \
	fi

up:  
	docker-compose up -d ${DB}

down: 
	docker-compose down

logs:  
	docker-compose logs -f

psql: 
	docker exec -it $(DB_CONTAINER) psql -d $(DB_NAME) -U $(DB_USER)


