# Variables
COMMAND = python3 start.py
LOG_FILE = output.log
PID_FILE = nohup_pid.txt

# Target to run the command with nohup and capture the PID
run:
	./nohup.sh

# Target to kill the process using the PID from the file
kill:
	@if [ -f $(PID_FILE) ]; then \
		PID=`cat $(PID_FILE)`; \
		echo "Killing process with PID $$PID..."; \
		kill $$PID; \
		rm $(PID_FILE); \
		echo "Process $$PID killed and $(PID_FILE) removed."; \
	else \
		echo "PID file $(PID_FILE) does not exist."; \
	fi
