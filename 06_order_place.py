import os
import threading
import json
from datetime import date
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv

CONFIDENTIAL_PATH = 'confidential/confidential.json'
PERCENTAGE_PROFIT = 5
PERCENTAGE_LOSS = 10
MOST_TARGET_TODAY = 20

# Returns the current local date
today = date.today()

formatted_date = today.strftime("%Y-%m-%d")  # Format as "YYYY-MM-DD"

# Lot size for trading
LOT_SIZE = 15
FIRST_DATA = True

# Load environment variables from .env file
load_dotenv()

# Open the JSON file containing confidential data
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

client_id = os.environ.get("client_id")
access_token = data['auth_code']

fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="./Log/")

def modify_order(stop_loss,take_profit):

    data_order = {
    "id":data["order_ID"], 
    "type":2, 
    "stopLoss": stop_loss, 
    "takeProfit": take_profit
    }
    response = fyers.modify_order(data=data_order)
    print(response)

# modify_order(data["stopLoss"] + 0.5,data["takeProfit"] + 0.5)
data = {}

response = fyers.exit_positions(data=data)
print(response)
