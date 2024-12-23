run:
	export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python && \
	( \
		python main.py & \
		/home/mark/TnTeQAQ/workspace/dpg\ demo/Rocos/ZBin/Client > logs/client_logs/client.log 2>&1 \
	)
run_debug:
	kernprof -l -v main.py
test:
	pytest -s

