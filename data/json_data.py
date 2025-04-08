import json
import os
from config.config import USER_DATA_FILE

# Function to read data from JSON file
def read_json_data():
    if not os.path.exists(USER_DATA_FILE):  # Check if JSON file exists
        write_json_data([])  # Create empty JSON file if missing
        return []

    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load data from JSON file
            return data if isinstance(data, list) else []  # Ensure data is a list
    except (json.JSONDecodeError, ValueError):  # Handle corrupted or invalid JSON
        write_json_data([])  # If so reset file with empty list 
        return []

# Function to write data to JSON file
def write_json_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4) # Format and save data with indentation for readability