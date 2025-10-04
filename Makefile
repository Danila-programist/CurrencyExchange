.PHONY: up down logs psql run kill_proccess init_env env_file

include .env
export

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
	print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
	@{$$help{$$_}},"\n" for keys %help;

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command. Use 'make help' for list of commands."
else
MESSAGE = "Done"
endif

init_env: ##@Environment Activate Poetry shell
	poetry shell

env_file: ##@Environment Create or update .env file
	$(eval SHELL:=/bin/bash)
	if [ ! -f .env ]; then \
		cp .env.example .env; \
	elif ! cmp -s .env .env.example; then \
		cp .env.example .env; \
	fi

run:   ##@Application Run main.py
	python3 main.py

kill_proccess: ##@Application Kill process on port 8000
	sudo lsof -ti :8000 | xargs -r sudo kill -9
	
up:  ##@Docker Start docker-compose services
	docker-compose up -d  

down:  ##@Docker Stop docker-compose services
	docker-compose down

logs:   ##@Docker Show logs from docker-compose
	docker-compose logs -f

psql:  ##@Database Open PostgreSQL inside docker container
	docker exec -it $(DB_CONTAINER_NAME) psql -d $(DB_NAME) -U $(DB_USER)

redis-cli:  ##@Database Open Redis CLI inside docker container
	docker exec -it ${REDIS_CONTAINER_NAME} redis-cli 

revision:  ##@Database Create Alembic revision
	alembic revision --autogenerate

migration:  ##@Database Apply Alembic migrations
	alembic upgrade head

format:   ##@Code Format code with black
	black .

lint: ##@Code Lint code with pylint
	pylint app main.py

check: ##@Test Check out application
	pytest tests

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

%::
	@echo $(MESSAGE)