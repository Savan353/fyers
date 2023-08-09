from fyers_api import fyersModel
from dotenv.main import load_dotenv
import os
import json

def place_order():
    #to load ENV file
    load_dotenv()

    # Opening JSON file
    f = open('confidential.json')
    
    # returns JSON object as 
    data = json.load(f)

    client_id = os.environ.get("client_id")
    access_token = data['auth_code']

    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="./Log/")

    data = {
        "symbol":data['index'],
        "qty":data['Lot_size'],
        "type":2,
        "side":1,
        "productType":"INTRADAY",
        "limitPrice":0,
        "stopPrice":0,
        "validity":"DAY",
        "disclosedQty":0,
        "offlineOrder":"False",
    }

    response = fyers.place_order(data=data)
    # print(response)