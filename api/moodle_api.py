from logs.log_config import setup_logging
setup_logging()  # Configure logging to include timestamps and write to application.log
import logging 
import requests
from datetime import datetime, timedelta
from config.config import MOODLE_URL, MOODLE_TOKEN

# Function to fetch all users from Moodle API by calling core_user_get_users Moodle web service function
def get_all_users():
    logging.info("* Fetching all Moodle users *")
    
    # Parameters for API request, including authentication token and API function name
    params = {
        "wstoken": MOODLE_TOKEN,  # Moodle API token for authentication
        "wsfunction": "core_user_get_users", # Moodle API web service function to get user data
        "moodlewsrestformat": "json",  # Format for the response (JSON)
        "criteria[0][key]": "email",  # Filter criteria by email
        "criteria[0][value]": "%"  # Wildcard value to fetch all users
    }

    # GET request to fetch users based on above criteria from Moodle API
    response = requests.get(MOODLE_URL, params=params)
    if response.status_code != 200:
        logging.error("Error fetching users:", response.text)  # Log error if request fails
        return []  # Return empty list if request fails
    
    # Parse (extract and format) the list of users from API response
    all_users = response.json().get("users", [])  # Extract users as a list from response
    logging.info(f"Total Moodle users fetched: {len(all_users)}") if all_users else logging.info("No users found.")
    return all_users

def get_recent_users(users=None):
    # Fetch all users if not already provided
    if users is None:
        users = get_all_users()
        
    last_24_hours = int((datetime.now() - timedelta(days=1)).timestamp())  # Calculate timestamp for 24 hours ago
    recent_users = [user for user in users if user.get("firstaccess", 0) >= last_24_hours]  # Filter users based on first access timestamp
    
    # Log number of recent users found
    logging.info(f"New Moodle users: {len(recent_users)}") if recent_users else logging.info("No new students found.")
    return recent_users

# Function to retrive custom field for a given Moodle user
def get_custom_field_value (user):
    return next((field["value"] for field in user.get("customfields", []) if field["shortname"] == "Custom_Field_1"), None)