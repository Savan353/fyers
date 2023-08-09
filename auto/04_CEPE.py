import json
import pandas as pd

CONFIDENTIAL_PATH = 'confidential/confidential.json'

# Open the JSON file containing confidential data
with open(CONFIDENTIAL_PATH) as json_file:
    data = json.load(json_file)

# Load previous close from JSON
previous_close = data['previous_close']

def expiry_date_index():
    """
    Fetch the expiry date for NIFTY BANK index from a CSV file.
    
    Returns:
        str: The expiry date in the format 'yyyy-mm-dd'.
    """
    symbol_data = pd.read_csv("https://public.fyers.in/sym_details/NSE_FO.csv")
    expiry_column = symbol_data.iloc[:, 9:10]
    expiry_list = expiry_column.values.tolist()
    relevant_expiry_dates = []
    for i in range(0, len(expiry_list)):
        if "NSE:BANKNIFTY" in expiry_list[i][0]:
            relevant_expiry_dates.append(expiry_list[i][0])
    first_relevant_expiry = relevant_expiry_dates[0][:18]
    return first_relevant_expiry

def select_expiry_index(ltp, expiry_date, ce_pe):
    """
    Select the appropriate CE or PE based on LTP and update JSON.
    
    Args:
        ltp (float): The Last Traded Price.
        expiry_date (str): The expiry date in the format 'yyyy-mm-dd'.
        ce_pe (str): "CE" for Call Option or "PE" for Put Option.
    
    Returns:
        None
    """
    rounded_ltp = int(ltp)
    if abs((rounded_ltp // 100) * 100 - rounded_ltp) < 50:
        rounded_ltp_nearest_hundred = (rounded_ltp // 100) * 100
    else:
        rounded_ltp_nearest_hundred = (rounded_ltp // 100) * 100 + 100

    data["index"] = expiry_date + str(rounded_ltp_nearest_hundred) + ce_pe
    updated_json = json.dumps(data, indent=4)
    
    with open(CONFIDENTIAL_PATH, "w") as outfile:
        outfile.write(updated_json)

def find_CE_PE(expiry_date):
    """
    Determine whether to select CE or PE based on LTP and previous close.
    
    Args:
        expiry_date (str): The expiry date in the format 'yyyy-mm-dd'.
    
    Returns:
        None
    """
    if previous_close < float(data["LTP"]):
        select_expiry_index(data["LTP"], expiry_date, "CE")
    else:
        select_expiry_index(data["LTP"], expiry_date, "PE")

def main():
    """
    Orchestrate the data processing.
    
    Returns:
        None
    """
    expiry_date = expiry_date_index()
    find_CE_PE(expiry_date)

if __name__ == '__main__':
    main()
    print("CEPE has been updated and saved in 'confidential.json'")
