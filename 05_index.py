from fyers_api.Websocket import ws
import os
import threading
from dotenv.main import load_dotenv
from fyers_api import fyersModel
import json
# Import date class from datetime module
from datetime import date
 
# Returns the current local date
today = date.today()
# print("Today date is: ", today)

formatted_date = today.strftime("%Y-%m-%d")  # Format as "YYYY-MM-DD"
# print("Today's date is:", formatted_date)

# Lot size for trading
LOT_SIZE = 15
First_data = True

# Load environment variables from .env file
load_dotenv()

# Open the JSON file containing confidential data
with open('confidential.json') as json_file:
    data = json.load(json_file)

def place_order():
    """
    Place a trading order using the FYERS API.
    """
    client_id = os.environ.get("client_id")
    access_token = data['auth_code']

    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="./Log/")

    data_order = {
        "symbol": data['index'],
        "qty": data['Lot_size'],
        "type": 2,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
    }

    response = fyers.place_order(data=data_order)
    if response["code"] == 200:
        data["order_ID"] = response["id"]
        json_object = json.dumps(data, indent=4)
        with open("confidential.json", "w") as outfile:
            outfile.write(json_object)

def run_process_symbol_data(access_token):
    """
    Run a WebSocket connection to receive symbol data updates.
    """
    data_type = "symbolData"
    inn = data['index']
    symbol = [inn]
    fs = ws.FyersSocket(access_token=access_token, log_path=os.getcwd())
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol, data_type=data_type)
    fs.keep_running()

def Lot_size(ltp):
    """
    Calculate lot size based on available balance and current price.
    """
    max_lots = data['Available_Balance'] // (LOT_SIZE * ltp)
    data["Lot_size"] = int(max_lots)
    json_object = json.dumps(data, indent=4)
    with open("confidential.json", "w") as outfile:
        outfile.write(json_object)
    # place_order()

def custom_message(msg):
    """
    Custom callback function to handle incoming symbol data messages.
    """
    # print (f"Custom:{msg}")
    global First_data
    if msg:
        if First_data and formatted_date != data["Today_date"]:
            # if :
            first_value = msg[0]['ltp']
            Lot_size(first_value)
            data["First_value_of_day"] = first_value
            data["Today_date"] = formatted_date
            json_object = json.dumps(data, indent=4)
            with open("confidential.json", "w") as outfile:
                outfile.write(json_object)
            First_data = False
        else:
            # Calculate the difference between the first value of the day and current ltp
            price_difference = msg[0]['ltp'] - data["First_value_of_day"]
            # Calculate equity difference
            equity_difference = price_difference * (15 * data["Lot_size"])
            # Update equity difference in the data or perform relevant actions
            print(f'{round(equity_difference,3)} : {price_difference} : {equity_difference}' )

def main():
    """
    Main function to start the WebSocket connection and trading activities.
    """
    access_token = os.environ.get("client_id") + ":" + data['auth_code']
    threading.Thread(target=run_process_symbol_data, args=(access_token,)).start()

if __name__ == '__main__':
    main()