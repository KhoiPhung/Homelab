#!/bin/bash

# --- Configuration ---
# Set the memory usage threshold in megabytes (MB).
# Using 5MB as testing
MEM_THRESHOLD_MB=5
LOG_FILE="high_memory_processes_bash.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# --- Main Logic ---
# The `ps` command lists processes with their PID, RSS (memory in KB), and command name.
# It then pipes this output to `awk` for proc
ps -eo pid,rss,comm | awk -v threshold=$MEM_THRESHOLD_MB -v ts="$TIMESTAMP" '
  {
    # Convert RSS (KB) to MB
    mb = $2 / 1024

    # Check threshold
    if (mb > threshold) {
      print ts " - Alert: High memory usage detected! PID: " $1 ", Name: " $3 ", Memory Used: " mb " MB"
    }
  }' >> "$LOG_FILE"
