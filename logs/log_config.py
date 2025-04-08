import logging
from config.config import LOG_FILE  

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,  # Specify log file path
        level=logging.INFO,  # Set the logging level to INFO without revealing sensitive data
        format='%(asctime)s - %(message)s'  # Format log message with timestamp
    )