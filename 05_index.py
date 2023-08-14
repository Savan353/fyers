"""
Fyers Trading Automation Script

This script interacts with the FYERS API to perform automated trading activities
using a WebSocket connection. It fetches data, places orders, and modifies existing orders
based on a predefined trading strategy.

Author: Savan Sutariya
Date: August 13, 2023
"""
import os
import threading
import json
from datetime import date
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv
from time import sleep

# Path to the confidential JSON file containing API credentials and data
CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Constants for trading strategy
PERCENTAGE_PROFIT = 5
PERCENTAGE_LOSS = 10
MOST_PROFIT_TODAY = 20

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

# Extracting API credentials from environment variables and JSON data
client_id = os.environ.get("client_id")
access_token = data['auth_code']

# Initialize the FYERS API client
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="./Log/")

# Function to fetch order book data from the API
def orderbook_order():
    """
    Fetch order book data from the FYERS API and update the local data.
    """
    response = fyers.orderbook()
    # print(response)
    if response["code"] == 200:
        data["orderbook_order_LTP"] = response["orderBook"][0]["lp"]
        json_object = json.dumps(data, indent=4)
        with open(CONFIDENTIAL_PATH, "w") as outfile:
            outfile.write(json_object)
    else:
        print(f"orderbook_order : {response}")

# Function to fetch trade book data from the API
def tradebook_order():
    """
    Fetch trade book data from the FYERS API and update the local data.
    """
    response = fyers.tradebook()
    # print(response)
    if response["code"] == 200:
        data["tradebook_order_LTP"] = response["tradeBook"][0]["tradeValue"]
        json_object = json.dumps(data, indent=4)
        with open(CONFIDENTIAL_PATH, "w") as outfile:
            outfile.write(json_object)
    else:
        print(f"tradebook_order : {response}")

# Function to fetch positions data from the API
def positions_order():
    """
    Fetch positions data from the FYERS API and update the local data.
    """
    response = fyers.positions()
    # print(response)
    if response["code"] == 200:
        if len(response["positions_value"]) == 0:
            data["positions_value"] = 0
            json_object = json.dumps(data, indent=4)
            with open(CONFIDENTIAL_PATH, "w") as outfile:
                outfile.write(json_object)
        else:
            data["positions_value"] = response["netPositions"][0]["buyAvg"]
            json_object = json.dumps(data, indent=4)
            with open(CONFIDENTIAL_PATH, "w") as outfile:
                outfile.write(json_object)
    else:
        print(f"positions_order : {response}")

# Function to place a trading order
def place_order():
    """
    Place a trading order using the FYERS API.
    """

    data_order = {
        "symbol": data['index'],
        "qty": LOT_SIZE * data['Lot_size'],
        "type": 2,
        "side": 1,
        # "productType": "INTRADAY",
        "productType": "BO",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss":data["stopLoss"],
        "takeProfit":data["takeProfit"]
    }

    response = fyers.place_order(data=data_order)
    if response["code"] == 1101:
        data["order_ID"] = response["id"]
        json_object = json.dumps(data, indent=4)
        with open(CONFIDENTIAL_PATH, "w") as outfile:
            outfile.write(json_object)
        print(f"order place successfully : {data['order_ID']}")
    else:
        print(f"place_order : {response}")

# Function to modify an existing order
def modify_order(stop_loss,take_profit):
    """
    Modify an existing order using the FYERS API.
    
    :param stop_loss: New stop loss value for the order.
    :param take_profit: New take profit value for the order.
    """
    data_order = {
    "id":data["order_ID"], 
    "type":2, 
    "stopLoss": stop_loss, 
    "takeProfit": take_profit
    }
    response = fyers.modify_order(data=data_order)
    print(response)

def exit_position() -> None:
    """
    exit_position
    """
    pass


# Function to run WebSocket for symbol data updates
def run_process_symbol_data(access_token_local):
    """
    Run a WebSocket connection to receive symbol data updates.
    """
    data_type = "symbolData"
    inn = data['index']
    symbol = [inn]
    fyers_socket = ws.FyersSocket(access_token=access_token_local, log_path="./Log/")
    fyers_socket.websocket_data = custom_message
    fyers_socket.subscribe(symbol=symbol, data_type=data_type)
    fyers_socket.keep_running()

# Function to calculate lot size based on available balance and current price
def calculate_lot_size(ltp):
    """
    Calculate the lot size based on available balance and current price.
    
    :param ltp: Current price (Last Traded Price) of the symbol.
    """
    max_lots = data['Available_Balance'] // (LOT_SIZE * ltp)
    data["Lot_size"] = int(max_lots)
    json_object = json.dumps(data, indent=4)
    with open(CONFIDENTIAL_PATH, "w") as outfile:
        outfile.write(json_object)
    # place_order()

# Callback function to handle incoming symbol data messages
def custom_message(msg):
    """
    Custom callback function to handle incoming symbol data messages.
    """
    # print (f"Custom:{msg}")
    global FIRST_DATA
    if msg:
        if FIRST_DATA and formatted_date != data["Today_date"]:
            first_value = msg[0]['ltp']
            data["First_value_of_day"] = first_value
            data["positions_value"] = 0
            data["Today_date"] = formatted_date
            data["limit"] = "true"
            json_object = json.dumps(data, indent=4)
            with open(CONFIDENTIAL_PATH, "w") as outfile:
                outfile.write(json_object)
            calculate_lot_size(first_value)
            FIRST_DATA = False
            while (data["positions_value"] == 0):
                positions_order()
                sleep(0.5)
                if data['positions_value'] != 0:
                    price_difference_copy = data['positions_value']
                    take_profit = (price_difference_copy * PERCENTAGE_PROFIT) / 100
                    stop_loss = (price_difference_copy * PERCENTAGE_LOSS) / 100
                    most_profit_today = (price_difference_copy * MOST_PROFIT_TODAY) / 100
                    data["takeProfit"] = round((take_profit),3)
                    data["most_profit_today"] = round((most_profit_today + price_difference_copy),3)
                    data["stopLoss"] = round((stop_loss),3)
                    json_object = json.dumps(data, indent=4)
                    with open(CONFIDENTIAL_PATH, "w") as outfile:
                        outfile.write(json_object)

        else:
            # Calculate the difference between the first value of the day and current ltp
            price_difference = msg[0]['ltp'] - data["First_value_of_day"]
            price_difference_copy = msg[0]['ltp']
            # Calculate equity difference
            equity_difference = price_difference * (LOT_SIZE * data["Lot_size"])
#1323
            # if data["most_profit_today"] > price_difference_copy and data["limit"] == "true":
            #     if price_difference_copy > (price_difference_copy + data["takeProfit"] - 10):
            #         modify_order(data["stopLoss"] + 10,data["takeProfit"] + 10)
            #         data["takeProfit"] = data["takeProfit"] + 10
            #         data["stopLoss"] = data["stopLoss"] + 10
            #         json_object = json.dumps(data, indent=4)
            #         with open(CONFIDENTIAL_PATH, "w") as outfile:
            #             outfile.write(json_object)
            #         if data["most_profit_today"] <= data["takeProfit"]:
            #             data["limit"] = "flase"
            #             json_object = json.dumps(data, indent=4)
            #             with open(CONFIDENTIAL_PATH, "w") as outfile:
            #                 outfile.write(json_object)
            # Update equity difference in the data or perform relevant actions
            print(f'{round(equity_difference,3)} : {price_difference} : {price_difference_copy}')

# Main function to start WebSocket connection and trading activities
def main():
    """
    Main function to start the WebSocket connection and trading activities.
    """
    access_token = os.environ.get("client_id") + ":" + data['auth_code']
    threading.Thread(target=run_process_symbol_data, args=(access_token,)).start()

if __name__ == '__main__':
    main()
