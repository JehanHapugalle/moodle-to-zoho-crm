from logs.log_config import setup_logging
setup_logging()  # Configure logging to include timestamps and write to application.log
import logging
import requests
from config.config import ZOHO_CRM_API_URL
from api.zoho_auth import get_access_token
from api.moodle_api import get_all_users, get_custom_field_value
from data.json_data import read_json_data, write_json_data

# Updates local JSON file with ammended Moodle user data and pushes updated data to Zoho CRM
def update_json_and_zoho():
    # Retrieve list of users updated in JSON
    updated_users = update_user_data()

    successful_updates = 0  # Initialize counter for successful user updates in Zoho CRM

    # If any updated users, send updated information to Zoho CRM
    if updated_users:
        for user in updated_users:
            # Prepare user data in format required by Zoho CRM
            user_data = {
                "Custom_Field_1": user["Custom_Field_1"],
                "F_Name": user["firstname"],
                "L_Name": user["lastname"],
                "Email": user["email"],
                "Username": user["username"]
            }
            
            # Update existing user record in Zoho CRM
            if update_zoho_user(user["id"], user_data):
                successful_updates += 1   # Increment counter for successful updates
                
    logging.info(f"{successful_updates} existing users updated in Zoho CRM.")  # Log total number of existing users updated in Zoho CRM

# Compares users stored in JSON file with latest user data from Moodle and updates JSON file if any data changed
def update_user_data():
    logging.info("* Updating Existing Users *")
    
    # Fetch all users from Moodle
    all_users = get_all_users()
    if not all_users:
        logging.info("No users to update.")  # Log if no users retrieved from Moodle
        return []

    users = read_json_data()  # Load existing user data from JSON file
    updated_users_count = 0  # Initialize counter for successful existing user updates in JSON file
    updated_users = []  # Store updated users as a list

    # Compare each user from Moodle with corresponding entry in JSON file
    for user in all_users:
        existing_user = next((u for u in users if u['id'] == user['id']), None)
        if existing_user:
            updated = False

            # Check and update Custom Field if ammended
            if existing_user.get('Custom_Field_1') != get_custom_field_value(user):
                existing_user['Custom_Field_1'] = get_custom_field_value(user)
                updated = True
            
            if existing_user['firstname'] != user['firstname']:
                existing_user['firstname'] = user['firstname']
                updated = True

            if existing_user['lastname'] != user['lastname']:
                existing_user['lastname'] = user['lastname']
                updated = True

            if existing_user['email'] != user['email']:
                existing_user['email'] = user['email']
                updated = True

            # If any update made, add user to updated users list and increment updated user counter
            if updated:
                updated_users_count += 1
                updated_users.append(existing_user)

    # Write updated user data to JSON file (overrides previous user data)
    if updated_users_count > 0:
        write_json_data(users)
        logging.info(f"{updated_users_count} existing users updated in the JSON file. List of User ID's updated in JSON file: {[user['id'] for user in updated_users]}")
    else:
        logging.info("No users were updated in the JSON file.") # Log if no updates made to any user
    
    return updated_users

# Updates existing user in Zoho CRM based on user ID and data passed to function
def update_zoho_user(user_id, user_data):
    # Retrieve valid Zoho access token
    access_token = get_access_token()[0]
    zoho_headers = {'Authorization': f'Zoho-oauthtoken {access_token}', 'Content-Type': 'application/json'}
    zoho_user_id = f"A{user_id}" # Prefix user ID with "A" required by Zoho CRM to match record
    
    # Search user's record in Zoho CRM with user ID
    response = requests.get(f"{ZOHO_CRM_API_URL}/search?criteria=(Name:equals:{zoho_user_id})", headers=zoho_headers)

    # If user found, proceed with update
    if response.status_code == 200 and response.json().get('data'):
        record_id = response.json()['data'][0]['id']

        # Prepare data payload for update request
        data = {"data": [{"id": record_id, **user_data}]}
        response = requests.put(f"{ZOHO_CRM_API_URL}/{record_id}", json=data, headers=zoho_headers)

        # Log outcome of update request
        if response.status_code in [200, 201, 202]:
            logging.info(f"User ID {user_id} updated in Zoho CRM. Zoho record ID: {record_id}")
            return True  # Indicate successful update
        else:
            logging.error(f"Failed to update Zoho record: {response.status_code} - {response.text}")
            return False  # Indicate failure to update
    else:
        logging.error(f"Error checking Zoho record: {response.status_code} - {response.text}")
        return False  # Indicate error in fetching user record