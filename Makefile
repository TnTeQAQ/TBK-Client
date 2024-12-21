run:
	python main.py
run_debug:
	kernprof -l -v main.py
test:
	pytest -s

