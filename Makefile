init:
	poetry shell

run:
	python main.py

kill_proccess:
	sudo lsof -ti :8000 | xargs -r sudo kill -9
	