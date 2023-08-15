
import os
import threading
import json
from datetime import date
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv
import time


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


# position = {'s': 'ok', 'code': 200, 'message': '', 'netPositions': [{'symbol': 'NSE:BANKNIFTY2381744100PE', 'id': 'NSE:BANKNIFTY2381744100PE-INTRADAY', 'buyAvg': 289.25, 'buyQty': 15, 'buyVal': 4338.75, 'sellAvg': 297.15, 'sellQty': 15, 'sellVal': 4457.25, 'netAvg': 0, 'netQty': 0, 'side': 0, 'qty': 0, 'productType': 'INTRADAY', 'realized_profit': 118.49999999999966, 'crossCurrency': '', 'qtyMulti_com': 1, 'segment': 11, 'ltp': 316.75, 'fyToken': '101123081739016', 'exchange': 10, 'unrealized_profit': 0, 'dayBuyQty': 15, 'cfBuyQty': 0, 'daySellQty': 15, 'cfSellQty': 0, 'rbiRefRate': 1, 'pl': 118.49999999999966, 'slNo': 0, 'avgPrice': 0}], 'overall': {'count_open': 0, 'count_total': 1, 'pl_realized': 118.49999999999966, 'pl_total': 118.49999999999966, 'pl_unrealized': 0}}

# @Savan353 ➜ /workspaces/fyers (main) $ /home/codespace/.python/current/bin/python3 /workspaces/fyers/06_order_place.py
# {'s': 'error', 'code': -52, 'message': 'Not a pending order', 'id': '23081400126034-BO-1'}
# @Savan353 ➜ /workspaces/fyers (main) $ /home/codespace/.python/current/bin/python3 /workspaces/fyers/06_order_place.py
# {'s': 'error', 'code': -52, 'message': 'Not a pending order', 'id': '23081400126034'}
# @Savan353 ➜ /workspaces/fyers (main) $ /home/codespace/.python/current/bin/python3 /workspaces/fyers/06_order_place.py
# {'s': 'ok', 'code': 1101, 'message': 'Position NSE:BANKNIFTY2381742000PE-BO is closed.'}
# @Savan353 ➜ /workspaces/fyers (main) $ 