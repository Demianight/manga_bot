#!/bin/bash

COMMAND="python3 start.py"

LOG_FILE="nohup.out"

PID_FILE="nohup_pid.txt"

# Run the command with nohup, redirect output to the log file, and run it in the background
nohup $COMMAND > $LOG_FILE 2>&1 &

# Capture the PID of the last background process
PID=$!

# Save the PID to the PID file
echo $PID > $PID_FILE

