"""
This script fetches symbol data using the Fyers API WebSocket and updates a JSON file
with real-time data. It also retrieves fund details using the Fyers API and updates the
JSON file with available balance information.

Dependencies:
- fyers_api (Python library for Fyers API interaction)
- dotenv (Python library for loading environment variables from .env file)

Ensure that the required environment variables are set in the .env file and the
necessary dependencies are installed.

Author: Savan Sutariya
Date: August 13, 2023
"""
import os
import time
import json
import multiprocessing
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv

# Path to the confidential JSON file
CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Load environment variables from .env file
load_dotenv()

# Open the JSON file
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# Get the client ID from environment variables
client_id = os.environ.get("client_id")

def run_process_symbol_data(access_token):
    """
    Run the WebSocket process to fetch symbol data and update JSON.

    Args:
        access_token (str): The concatenated client ID and auth code.

    Returns:
        None
    """
    data_type = os.environ.get("data_type")
    symbol = ["NSE:NIFTYBANK-INDEX"]

    # Create a FyersSocket instance
    fyers_socket = ws.FyersSocket(access_token=access_token, log_path="./Log/")
    fyers_socket.websocket_data = custom_message
    fyers_socket.subscribe(symbol=symbol, data_type=data_type)
    fyers_socket.keep_running()

def custom_message(msg):
    """
    Custom message handling function for WebSocket.

    Args:
        msg (list): List of messages from WebSocket.

    Returns:
        None
    """
    # Update the LTP in the JSON data
    data["LTP"] = msg[0]["ltp"]

    # Write updated JSON to file
    json_object = json.dumps(data, indent=4)
    with open(CONFIDENTIAL_PATH, "w") as outfile:
        outfile.write(json_object)

def funds():
    """
    Fetch fund details from Fyers API and update JSON.

    Returns:
        None
    """
    found_dict = None

    # Create a FyersModel instance
    fyers = fyersModel.FyersModel(client_id=client_id, token=data['auth_code'], log_path="./Log/")
    response = fyers.funds()
    
    if response['code'] == 200:
        for item in response['fund_limit']:
            if item['id'] == 10:
                found_dict = item
                break

        # Update the available balance in the JSON data
        data["Available_Balance"] = found_dict['equityAmount']

        # Write updated JSON to file
        json_object = json.dumps(data, indent=4)
        with open(CONFIDENTIAL_PATH, "w") as outfile:
            outfile.write(json_object)
    else:
        print(f'funds : {response}')

def main():
    """
    Orchestrate the data processing.

    Returns:
        None
    """
    # Fetch fund details and update JSON
    funds()

    # Prepare access token
    access_token = client_id + ":" + data['auth_code']

    # Start WebSocket process
    proc = multiprocessing.Process(target=run_process_symbol_data, args=(access_token,))
    proc.start()

    # Allow WebSocket process to run for 5 seconds
    time.sleep(5)

    # Terminate the WebSocket process
    proc.terminate()

if __name__ == '__main__':
    # Call the main function
    main()
    print("Fund and open data have been updated and saved in 'confidential.json'")
