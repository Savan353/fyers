import json
import os
import requests
from dotenv.main import load_dotenv

CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Load environment variables from .env file
load_dotenv()

# Open the JSON file containing confidential data
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# URL for refreshing the access token using the refresh token
URL = 'https://api.fyers.in/api/v2/validate-refresh-token'

# Headers for the HTTP request
headers = {
    'Content-Type': 'application/json'
}

# Data for refreshing the token
data_refresh_token = {
    "grant_type": "refresh_token",
    "appIdHash": os.environ.get("appIdHash"),
    "refresh_token": data["refresh_token"],
    "pin": os.environ.get("pin")
}

# Send a POST request to refresh the token
response = requests.post(URL, headers=headers, json=data_refresh_token)

# Check if the response indicates a successful token refresh
if response.json()["code"] == 200:
    # Update the refreshed access token in the data dictionary
    data["auth_code"] = response.json()["access_token"]
    json_object = json.dumps(data, indent=4)

    # Write the updated data back to the JSON file
    with open(CONFIDENTIAL_PATH, "w") as outfile:
        outfile.write(json_object)

    # Inform the user about the update
    print("Refresh_token has been updated and saved in 'confidential.json'")

else:
    print(response)
    print("Error while upload access_token in 02_refresh_token")