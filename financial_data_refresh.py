"""
Financial Data Refresh Script

This script automates the process of refreshing financial data by executing a sequence
of Python scripts. It includes functions to wait until a specified time and catch
exceptions during execution.

Author: Savan Sutariya
Date: August 13, 2023
"""

import os
import time as t
from datetime import datetime
from pytz import timezone

def wait_until(target_hour, target_minute):
    """
    Wait until the specified time is reached.
    
    This function waits until the current time matches or exceeds the target time 
    specified in hours and minutes.
    
    Args:
        target_hour (int): The target hour.
        target_minute (int): The target minute.
    
    """
    target_time = str(target_hour) + ":" + str(target_minute)
    while True:
        kolkata_timezone = timezone('Asia/Kolkata')
        current_time = datetime.now(kolkata_timezone)
        time_string = current_time.strftime('%H:%M')

        if time_string >= target_time:
            break

        t.sleep(10)  # Adjust the sleep interval as needed

def run_rf_script():
    """
    Run the series of Python scripts for refreshing financial data.
    
    This function executes a sequence of Python scripts in a specified order to
    refresh financial data. If any of the scripts encounter an error, this function
    will catch the exception and print an error message.

    Steps:
    1. Run '01_previous_close.py' to get previous close data.
    2. Run '02_refresh_token.py' to refresh authentication token.
    3. Wait until 09:14 AM using the 'wait_until' function.
    4. Run '03_getbankniftyindex.py' to fetch Bank Nifty index data.
    5. Run '04_CEPE.py' to process call and put option data.

    Note: Make sure that the required Python scripts are in the same directory as
    this script.

    Raises:
        Exception: If any of the scripts encounter an error during execution.
    """
    try:
        # Step 1: Get previous close data
        os.system("python auto/01_previous_close.py")
        
        # Step 2: Refresh authentication token
        os.system("python auto/02_refresh_token.py")

        # Step 3: Wait until 09:14 AM
        wait_until('09', '14')

        # Step 4: Fetch Bank Nifty index data
        os.system("python auto/03_getbankniftyindex.py")
        
        # Step 5: Process call and put option data
        os.system("python auto/04_CEPE.py")
        
    except Exception as error:
        print(f"Error while running rf.py: {error}")

if __name__ == "__main__":
    run_rf_script()
