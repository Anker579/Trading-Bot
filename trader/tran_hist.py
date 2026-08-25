import requests
import csv
#import auth
from datetime import datetime, timezone, timedelta
import pandas as pd
import config

is_live = False
has_prompted = True

def get_history(accID, access_token):
    today = datetime.now(timezone.utc)
    formatted_date = today.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_date = today - timedelta(days=364)
    formatted_start_date = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    #Set the base url based on config for live or practice endpoint
    if config.OANDA_ENVIRONMENT == "live":
        BASE_URL = "https://api-fxtrade.oanda.com/v3"
    else:
        BASE_URL = "https://api-fxpractice.oanda.com/v3"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    url = f'{BASE_URL}/accounts/{accID}/transactions'

    params = {
        'from': formatted_start_date,  # Replace with your desired start date
        'to': formatted_date,     # Replace with your desired end date 
        'pageSize': 1000
        }

    response = requests.get(url, headers=headers, params=params)

    all_transactions = []

    # While loop to iterate through multiple pages
    while url:

        # Make the API request
        response = requests.get(url, headers=headers, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()

            # Retrieve the transactions from the current page
            transactions = data.get('transactions', [])
            all_transactions.extend(transactions)

            # Follow pagination if there are more pages
            pages = data.get('pages', [])
            url = pages[0] if pages else None  # Get the next page URL
            params = None  # No need to pass params for the next page requests
        else:
            raise RuntimeError(
                f"OANDA API error {response.status_code}: {response.text}"
            )
    
    #print(response)
    #print(all_transactions)
    
    
    return pd.DataFrame(all_transactions)


    


    
    #print(response.status_code)
    #if response.status_code == 200:
    #    transactions = response.json().get('transactions', [])
    #    print(response.text)
    #    with open("hist.csv", mode='w', newline='') as file:
    #        writer = csv.DictWriter(file, fieldnames=fieldnames)
    #    
    #        # Write the header
    #        writer.writeheader()
    #    
    #        # Write the transaction data
    #        for transaction in transactions:
    #            writer.writerow(transaction)

    #with open("hist.csv", mode='w', newline='') as file:
    #    writer = None
#
    #    while url:
    #        # Make the API request
    #        response = requests.get(url, headers=headers, params=params)
#
    #        # Check if the response is successful
    #        if response.status_code == 200:
    #            data = response.json()
#
    #            # Retrieve the transactions from the current page
    #            transactions = data.get('transactions', [])
    #            all_transactions.extend(transactions)
#
    #            # If this is the first page, determine fieldnames dynamically
    #            if not writer and transactions:
    #                # Create a set of all unique fieldnames
    #                fieldnames = set()
    #                for transaction in transactions:
    #                    fieldnames.update(transaction.keys())  # Add all keys to the set
    #                fieldnames = list(fieldnames)  # Convert the set back to a list
#
    #                writer = csv.DictWriter(file, fieldnames=fieldnames)
    #                writer.writeheader()
#
    #            # Write each transaction to the CSV file
    #            for transaction in transactions:
    #                writer.writerow(transaction)
#
    #            # Follow pagination if there are more pages
    #            pages = data.get('pages', [])
    #            url = pages[0] if pages else None  # Get the next page URL
    #            params = None  # No need to pass params for the next page requests
    #        else:
    #            print(f"Error: {response.status_code} - {response.text}")
    #            break
#
    #print("All transactions have been written to hist.csv")
    #return 