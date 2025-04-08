from logs.log_config import setup_logging
setup_logging()  # Configure logging to include timestamps and write to application.log 
import logging
import requests
from config.config import ZOHO_CRM_API_URL
from api.zoho_auth import get_access_token
from api.moodle_api import get_recent_users, get_custom_field_value  
from data.json_data import read_json_data, write_json_data

# Pushes newly retrieved and filtered user data from Moodle to Zoho CRM
def push_data_to_zoho():
    # Fetch most recent users from Moodle that were filtered prior
    recent_users = get_recent_users()
    
    # Log and exit if no new users to process
    if not recent_users:  
        logging.info("No new users to process.")
        return
    
    logging.info(f"* Pushing New Users *")
    
    # Retrieve valid Zoho access token
    access_token = get_access_token()[0]
    if not access_token:
        logging.error("No valid access token.")
        return

    # Prepare user data in format required by Zoho CRM
    data = {
        "data": [
            {
                "Name": f"A{user['id']}",
                "Custom_Field_1": get_custom_field_value(user),
                "Username": user["username"],
                "F_Name": user["firstname"],
                "L_Name": user["lastname"],
                "Email": user["email"]
            }
            for user in recent_users
        ]
    }

    # Set authorization headers for Zoho API request
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}'}

    # Send user data to Zoho CRM using POST request
    response = requests.post(ZOHO_CRM_API_URL, json=data, headers=headers)

    # Check response status and log an error if request failed
    if response.status_code not in [200, 201, 202]:
        logging.error(f"Failed to push data: {response.status_code}")
        return

    # Process response and identify successfully pushed users
    valid_users = [
        {**{key: user[key] for key in ["id", "username", "firstname", "lastname", "email"]}, "Custom_Field_1": get_custom_field_value(user)}
        for record, user in zip(response.json().get("data", []), recent_users)
        if record.get("status") == "success"
    ]

    added_to_zoho = 0   # Initialize counter for successful new user pushes to Zoho CRM
    
    for record, user in zip(response.json().get("data", []), recent_users):
        if record.get("status") == "success":
            added_to_zoho += 1  # Increment counter for successful pushes
            # Log successful user addition with Zoho record ID and respective User ID
            zoho_record_id = record.get("details", {}).get("id")
            logging.info(f"User ID {user['id']} added to Zoho CRM. Zoho record ID: {zoho_record_id}")
    
    # Log total number of users added to Zoho CRM
    logging.info(f"{added_to_zoho} new users added to Zoho CRM.")  

    # Update local JSON file with users successfully added to Zoho CRM
    if valid_users:
        users = read_json_data()  # Load existing user data from JSON file
        existing_ids = {user["id"] for user in users}  # Get ID's of existing users
        new_users = [user for user in valid_users if user["id"] not in existing_ids]  # Filter out duplicates

        if new_users: 
            write_json_data(users + new_users)  # Append new users to JSON file
            # Log total number of new users added to JSON file and their user ID's
            logging.info(f"{len(new_users)} new users added to the JSON file: List of User ID's added to JSON file: {[user['id'] for user in new_users]}") 