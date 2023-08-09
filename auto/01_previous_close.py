import requests
from bs4 import BeautifulSoup
import json

CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Load JSON data from file
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# URL for the last price
last_price_url = 'https://www.google.com/finance/quote/NIFTY_BANK:INDEXNSE?hl=en'

# Send a GET request to fetch the HTML content
response = requests.get(last_price_url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find the element containing the last price using its class
last_price_element = soup.find(class_='YMlKec fxKbKc')

# Clean the extracted text (remove commas) and convert to float
cleaned_last_price = float(last_price_element.text.replace(',', ''))

# Update the JSON data with the new last price
data["previous_close"] = cleaned_last_price

# Convert the updated data back to a formatted JSON string
updated_json = json.dumps(data, indent=4)

# Write the updated JSON back to the file
with open(CONFIDENTIAL_PATH, "w") as json_file:
    json_file.write(updated_json)

# Inform the user about the update
print("Last price has been updated and saved in 'confidential.json'")
