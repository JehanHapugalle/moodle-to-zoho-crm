import os
import time
from config.config import LOG_FILE

def clear_old_logs():
    log_file = LOG_FILE  # Log file path

    # Ensure log file exists
    if not os.path.exists(log_file):
        print(f"{log_file} does not exist.")  # Notify if log file missing
        return 

    # Calculate time threshold (1 day ago)
    time_threshold = time.time() - (7 * 24 * 60 * 60)  # 24 hours in seconds

    with open(log_file, "r") as f:
        lines = f.readlines()

    # Find first valid line meeting timestamp criteria
    for i, line in enumerate(lines):
        try:
            timestamp_str = line.split(" - ")[0][:16]  # Extract timestamp in format (YYYY-MM-DD HH:MM) from log file
            timestamp = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d %H:%M"))  # Convert extracted timestamp to epoch time
            
            # If timestamp meets threshold criteria, retain this line and all subsequent lines
            if timestamp >= time_threshold:
                with open(log_file, "w") as f:
                    f.writelines(lines[i:])  # Write only relevant lines back to file (removes all outdated lines)
                return  # Exit the function once lines are updated in log file
        except (ValueError, IndexError):
            # Skip invalid lines without valid timestamp when checking for timestamp criteria without crashing
            continue

if __name__ == "__main__":
    clear_old_logs()  # Execute the function when the script is run directly