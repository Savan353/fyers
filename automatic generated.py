import os

def run_rf_script():
    """
    Run the series of Python scripts for refreshing financial data.
    
    This function executes a sequence of Python scripts in a specified order to refresh financial data.
    If any of the scripts encounter an error, this function will catch the exception and print an error message.

    Steps:
    1. Run '01_previous_close.py' to get previous close data.
    2. Run '02_refresh_token.py' to refresh authentication token.
    3. Run '03_getbankniftyindex.py' to fetch Bank Nifty index data.
    4. Run '04_CEPE.py' to process call and put option data.

    Note: Make sure that the required Python scripts are in the same directory as this script.

    Raises:
        Exception: If any of the scripts encounter an error during execution.

    """
    try:
        # Step 1: Get previous close data
        os.system("python auto/01_previous_close.py")
        
        # Step 2: Refresh authentication token
        os.system("python auto/02_refresh_token.py")
        
        # Step 3: Fetch Bank Nifty index data
        os.system("python auto/03_getbankniftyindex.py")
        
        # Step 4: Process call and put option data
        os.system("python auto/04_CEPE.py")
        
    except Exception as e:
        print(f"Error while running rf.py: {e}")

if __name__ == "__main__":
    run_rf_script()
