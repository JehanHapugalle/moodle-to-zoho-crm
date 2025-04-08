from logs.log_config import setup_logging
setup_logging()  # Configure logging to include timestamps and write to application.log
import logging
from push_data import push_data_to_zoho
from update_data import update_json_and_zoho

def run_tasks():
    try:
        # Log start of task execution
        logging.info("-- Task execution started --")  # Log process in application.log with timestamp
        print("-- Task execution started --")  # Print to be displayed in CRON job log

        # Execute function to push new user data to Zoho CRM and log process
        push_data_to_zoho()
        logging.info("Push New Users executed") 
        print("Push New Users executed") 

        # Execute function to update existing user data in Zoho CRM and log process
        update_json_and_zoho()
        logging.info("Update Existing Users executed")
        print("Update Existing Users executed")  

        # Log completion of task execution
        logging.info("-- Task executed successfully --")
        logging.info("")
        print("-- Task executed successfully --")  

    except Exception as e:
        # Log any exceptions that occur during task execution
        logging.error(f"Error occurred: {str(e)}")
        print(f"Error occurred: {str(e)}")  

if __name__ == "__main__":
    # Call the run_tasks() function to execute the push and update tasks
    run_tasks()