from fyers_api import accessToken
from dotenv.main import load_dotenv
import os
import json

CONFIDENTIAL_PATH = 'confidential/confidential.json'
# Load environment variables from .env file
load_dotenv()

# Open the JSON file
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# Fetch environment variables
client_id = os.environ.get("client_id")
secret_key = os.environ.get("secret_key")
redirect_uri = os.environ.get("redirect_uri")
response_type = os.environ.get("response_type")
state = os.environ.get("state")
grant_type = os.environ.get("grant_type")

# Create a session for generating authorization code
session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

# Generate authorization code
auth_code = session.generate_authcode()
print("Authorization Code:", auth_code)

# Create a session for generating access token
access_token_session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

# Set the authorization code and generate access token
auth_code_input = str(input("Enter the Authorization Code: "))
access_token_session.set_token(auth_code_input)
access_token_response = access_token_session.generate_token()

# Extract access token from the response
access_token = access_token_response['access_token']

refresh_token = access_token_response['refresh_token']


# Update the JSON data with the access token
data['auth_code'] = access_token
data['refresh_token'] = refresh_token

# Convert the updated data back to a formatted JSON string
updated_json = json.dumps(data, indent=4)

# Write the updated JSON back to the file
with open(CONFIDENTIAL_PATH, "w") as json_file:
    json_file.write(updated_json)

# Inform the user about the update
print("Access token has been updated and saved in 'confidential.json'")
