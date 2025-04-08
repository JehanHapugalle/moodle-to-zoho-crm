from logs.log_config import setup_logging
setup_logging()  # Configure logging to include timestamps and write to application.log
import logging
import requests
from config.config import ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, SCOPE, ZOHO_TOKEN_URL, ZOHO_SOID

# Function to get access token using client credentials flow for self client created in Zoho API console
def get_access_token():
    # Payload containing parameters required for OAuth client credentials grant flow
    payload = {
        'client_id': ZOHO_CLIENT_ID,  # Zoho client ID from the API console
        'client_secret': ZOHO_CLIENT_SECRET,  # Zoho client secret from the API console
        'grant_type': 'client_credentials',  # Specifies the OAuth grant type to use client credentials above
        'scope': SCOPE,  # API access scope
        'soid': ZOHO_SOID  # Zoho Organization ID for client
    }
    
    logging.info(f"* Requesting Zoho access tokens *")
    logging.info(f"Request payload: {{'client_id': 'XXXX', 'client_secret': 'XXXX', 'grant_type': 'client_credentials'}}")  # Log request payload structure without exposing sensitive credentials

    response = requests.post(ZOHO_TOKEN_URL, params=payload)  # Make POST request to Zoho's token endpoint with above payload
    logging.info(f"Response status: {response.status_code}. Access token received") # Log response status code

    # If response above successful, parse (extract and format) the JSON data
    if response.status_code == 200:
        data = response.json()  # Store response data in JSON format
        access_token = data['access_token']  # Extract access token
        api_domain = data['api_domain']  # Extract the API domain for future API calls
        return access_token, api_domain  # Return above extracted credentials
    else:
        # Log an error if request fails, along with status code and response
        logging.error(f"Error: {response.status_code}, {response.text}")
        return None, None   # Return None if request unsuccessful