import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file to manage sensitive data securely

# Moodle configurations
MOODLE_URL = os.getenv("MOODLE_URL")   # Moodle API base URL
MOODLE_TOKEN = os.getenv("MOODLE_TOKEN")  # Token authenticating requests to Moodle API

# Zoho API configurations
ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")  # Zoho API client ID for OAuth
ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")  # Zoho API client secret for OAuth
ZOHO_SOID = os.getenv("ZOHO_SOID")  # Zoho organization ID for API requests
SCOPE = 'ZohoCRM.modules.ALL'  # Permission scope for Zoho CRM API
ZOHO_TOKEN_URL = 'https://accounts.zoho.com.au/oauth/v2/token'  # URL to fetch Zoho OAuth tokens
ZOHO_CRM_API_URL = "https://www.zohoapis.com.au/crm/v2/YourModuleName"  # Zoho CRM API endpoint for your module in Zoho CRM

# File Paths
USER_DATA_FILE = os.getenv("USER_DATA_FILE")  # Path to JSON file storing user data
LOG_FILE = os.getenv("LOG_FILE")  # Path to log file