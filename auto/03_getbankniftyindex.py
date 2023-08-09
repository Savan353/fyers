import os
import time
import json
from fyers_api.Websocket import ws
from dotenv.main import load_dotenv
from fyers_api import fyersModel
import multiprocessing

CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Load environment variables from .env file
load_dotenv()

# Open the JSON file
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

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
    fs = ws.FyersSocket(access_token=access_token, log_path="./Log/")
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol, data_type=data_type)
    fs.keep_running()

def custom_message(msg):
    """
    Custom message handling function for WebSocket.

    Args:
        msg (list): List of messages from WebSocket.

    Returns:
        None
    """
    data["LTP"] = msg[0]["ltp"]
    
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
    fyers = fyersModel.FyersModel(client_id=client_id, token=data['auth_code'], log_path="./Log/")
    response = fyers.funds()
    
    if response['code'] == 200:
        for item in response['fund_limit']:
            if item['id'] == 10:
                found_dict = item
                break

        data["Available_Balance"] = found_dict['equityAmount']
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
    funds()
    access_token = client_id + ":" + data['auth_code']
    proc = multiprocessing.Process(target=run_process_symbol_data, args=(access_token,))
    proc.start()
    time.sleep(5)
    proc.terminate()

if __name__ == '__main__':
    main()
    print("Fund and open data have been updated and saved in 'confidential.json'")
