.PHONY: up down logs psql run kill_proccess init_env env_file

include .env
export

init_env:
	poetry shell

env_file:
	$(eval SHELL:=/bin/bash)
	if [ ! -f .env ]; then \
		cp .env.example .env; \
	elif ! cmp -s .env .env.example; then \
		cp .env.example .env; \
	fi

run:
	python3 main.py

kill_proccess:
	sudo lsof -ti :8000 | xargs -r sudo kill -9
	
up:  
	docker-compose up -d  

down: 
	docker-compose down

logs:  
	docker-compose logs -f

psql: 
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(DB_NAME) -U $(DB_USER)

redis-cli:
	docker exec -it ${REDIS_CONTAINER_NAME} redis-cli 

revision:
	alembic revision --autogenerate

migration:
	alembic upgrade head

format:
	black .

lint:
	pylint app main.py