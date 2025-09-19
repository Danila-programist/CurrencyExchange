init:
	poetry shell

run:
	python3 main.python3

kill_proccess:
	sudo lsof -ti :8000 | xargs -r sudo kill -9
	