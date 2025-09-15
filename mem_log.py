import psutil
from datetime import datetime


MEM_THRESHOLD_GB = 0.0049  #change to any GB amount

# Define the log file where alerts will be written.
LOG_FILE = "high_memory_processes_python.log"


def log_high_memory_processes():
    """
    Scans all running processes and logs those that exceed the memory threshold.
    """

    # Create a timestamp string to mark when the scan was run.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Convert the memory threshold into bytes (since psutil reports memory in bytes).
    mem_threshold_bytes = MEM_THRESHOLD_GB * (1024 ** 3)

    # Open the log file in append mode ("a"), so new alerts get added at the end.
    with open(LOG_FILE, "a") as log_file:

        # Iterate through all running processes.
        # The process_iter() call fetches only the attributes we need:
        # - pid: process ID
        # - name: process name
        # - memory_info: includes the RSS (Resident Set Size = memory in RAM)
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                # Get process information as a dictionary
                info = proc.info

                # Extract individual fields for readability
                pid = info['pid']
                # Some processes might not have a name, so default to "Unknown"
                name = info['name'] or "Unknown"
                # RSS is the resident memory size in bytes
                rss_bytes = info['memory_info'].rss

                # Compare process memory usage against threshold
                if rss_bytes > mem_threshold_bytes:
                    # Convert RSS to GB for easier human reading
                    rss_gb = rss_bytes / (1024 ** 3)

                    # Format the alert message
                    alert = (
                        f"{timestamp} - ALERT: High memory usage detected! "
                        f"PID: {pid}, Name: {name}, Memory Used: {rss_gb:.2f} GB"
                    )

                    # Print alert to the console for immediate visibility
                    print(alert)

                    # Write alert to the log file for record-keeping
                    log_file.write(alert + "\n")

            # Handle exceptions gracefully:
            # - NoSuchProcess: Process ended before we could inspect it
            # - AccessDenied: We don’t have permission to inspect it
            # - ZombieProcess: The process is a "zombie" (terminated but not cleaned up yet)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue



if __name__ == "__main__":
    log_high_memory_processes()
