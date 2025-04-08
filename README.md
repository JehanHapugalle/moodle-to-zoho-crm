# moodle-to-zoho-api

This Python application automates the daily synchronization of user data from Moodle LMS to Zoho CRM using API integration.

Features

• Fetch New Students: Retrieves students created in the last 24 hours from Moodle API.

• Push to Zoho CRM: Uses Zoho OAuth API to authenticate and add new students to CRM.

• Update Existing Records: Compares all Moodle users with previously stored JSON data and updates any changes in Zoho CRM.

• Logging: Maintains logs of successful syncs, errors, and transaction details.

• Secure Credentials: Stores API keys and credentials securely using a .env file.

• Automated Execution: Runs daily via a CRON job on the hosting server.

Installation & Usage

1. Set up API credentials in .env.
2. Configure Moodle and Zoho API settings.
3. Schedule the script to run daily using a CRON job.

Requirements

• requests==2.26.0

• python-dotenv==0.19.2

• pylint==2.6.0

This ensures a seamless and automated student data sync between Moodle and Zoho CRM.

Documentation

• The docs/ folder includes visual diagrams explaining how the push and update functions operate.

• Future documentation will also include:

- A CRON job command example for automation and how to set up on a server

- How to sync all historical Moodle user data to Zoho CRM
  
- Where the code has been generalized, showing what parts should be updated for your specific Moodle module or Zoho CRM setup

- How the application can be modified or extended for different modules or workflows

- How to setup Moodle API credentials and Zoho API Console to obtain tokens
