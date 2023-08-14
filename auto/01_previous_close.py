"""
This script fetches the last price of a financial index from a URL, updates a JSON file
with the new price, and informs the user about the update.

Dependencies:
    - requests
    - BeautifulSoup
    - json

Usage:
    Modify the CONFIDENTIAL_PATH variable to specify the path to the JSON file.
    Run the script to fetch the last price, update the JSON data, and inform the user.

Author: Savan Sutariya
Date: August 13, 2023
"""
import json
import requests
from bs4 import BeautifulSoup

CONFIDENTIAL_PATH = 'confidential/confidential.json'

def fetch_last_price(url):
    """
    Fetches the last price from a given URL.

    Args:
        url (str): The URL to fetch the last price from.

    Returns:
        float: The last price as a floating-point number.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    last_price_element = soup.find(class_='YMlKec fxKbKc')
    cleaned_last_price = float(last_price_element.text.replace(',', ''))
    return cleaned_last_price

def update_json_last_price(json_path, last_price):
    """
    Updates the last price in a JSON file.

    Args:
        json_path (str): The path to the JSON file.
        last_price (float): The new last price to be updated.
    """
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
    
    data["previous_close"] = last_price
    
    updated_json = json.dumps(data, indent=4)
    
    with open(json_path, 'w') as json_file:
        json_file.write(updated_json)

def main():
    """
    Main function to fetch the last price, update JSON data, and inform the user.
    """
    last_price_url = 'https://www.google.com/finance/quote/NIFTY_BANK:INDEXNSE?hl=en'

    cleaned_last_price = fetch_last_price(last_price_url)
    update_json_last_price(CONFIDENTIAL_PATH, cleaned_last_price)

    print("Last price has been updated and saved in 'confidential.json'")

if __name__ == "__main__":
    main()
