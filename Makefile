run:
	export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python && unset http_proxy && python main.py
	# python main.py
run_debug:
	export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python && unset http_proxy && kernprof -l -v main.py

test:
	pytest -s

