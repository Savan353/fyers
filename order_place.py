PERCENTAGE_PROFIT = 5
import os
import threading
import json
from datetime import date
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from dotenv.main import load_dotenv

CONFIDENTIAL_PATH = 'confidential/confidential.json'

with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# PERCENTAGE_LOSS = 10

# price_difference_copy=200

# take_profit = (price_difference_copy * PERCENTAGE_PROFIT) / 100
# stop_loss = (price_difference_copy * PERCENTAGE_LOSS) / 100
# data1 = take_profit + price_difference_copy
# data2 = price_difference_copy - stop_loss
# print(data1)
# print(data2)

# # price_difference = msg[0]['ltp'] - data["First_value_of_day"]

# # price_difference_copy = msg[0]['ltp']

# # Calculate equity difference
# equity_difference = 500
# if equity_difference > equity_difference - 50:
#     print('adsvffsd')
# else:
#     print('acasdfrwebwebwer')
sdv = True
while True:
    equity_difference = int(input())
    # if equity_difference < data["takeProfit"] - 50:

    if data["most_target_today"] > equity_difference:
        print('a3545453453453435d')

        if equity_difference > data["takeProfit"] - 50 and sdv:
            
    #         modify_order(data["stopLoss"] + 50,data["takeProfit"] + 50)
            data["takeProfit"] = data["takeProfit"] + 50
    #         data["stopLoss"] = data["stopLoss"] + 50
            json_object = json.dumps(data, indent=4)
            with open(CONFIDENTIAL_PATH, "w") as outfile:
                outfile.write(json_object)
    # if data["most_target_today"] < equity_difference:
            if data["most_target_today"] <= data["takeProfit"]:
                print('54654654654654654fsd')
                sdv = False
                # print()

            print('adsvffsd')
        else:
            print('aadljvmkjwsdmvuwdsvffsd')


        # modify_order(data["stopLoss"] + 50,data["takeProfit"] + 50)
        # data["takeProfit"] = data["takeProfit"] + 50
        # data["stopLoss"] = data["stopLoss"] + 50
        # json_object = json.dumps(data, indent=4)
        # with open(CONFIDENTIAL_PATH, "w") as outfile:
        #     outfile.write(json_object)