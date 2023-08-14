
import os
import threading
import json
from datetime import date
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv


CONFIDENTIAL_PATH = 'confidential/confidential.json'

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
# response = fyers.get_profile() #Profile
# response = fyers.funds() #funds
# response = fyers.holdings() 
# #Transaction Info
# response = fyers.orderbook()
response = fyers.positions()
# response = fyers.tradebook()
print(response)
