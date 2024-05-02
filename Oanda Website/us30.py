import os
import psycopg2
from config import config
import requests 
import json
import time
def fetch_data(url, params):
    try:
        with requests.post(url, params=params) as response:
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            # print(f"Statuse Candlse: {response.text}")
            candles = response.json().get('candles', [])
            return candles
    except requests.requests.RequestException as e:
        print(f"An error occurred:{e}")
        return()

def get_chart_data(granularity, sleep_time):
    url = "https://dashboard.acuitytrading.com/OandaPriceApi/GetCandles"
    params = {
        'widgetName': 'oandainstrumentpage',
        'apikey': '4b12e6bb-7ecd-49f7-9bbc-2e03644ce41f',
        'Remote Address': '51.158.239.38:443',
        'Request-Context': 'appId=cid-v1:c0a124e5-71c0-4ced-b978-78e4ff157a5c',
        'granularity': granularity,
        'instrumentName': 'US30_USD',
        'region': 'OEL'
    }
   
    while True:
        candles = fetch_data(url, params)
        print(f"Inserted {len(candles)} candlse from the API.")
        if candles:
            data_candles = list(map(lambda candle: {'t': candle['time'], 'l': candle['mid']['l'], 'h': candle['mid']['h'], 'c': candle['mid']['c'], 'o': candle['mid']['o']}, candles))
            # print(data_candles)
            save_to_db(data_candles)
            time.sleep(sleep_time)
    

def save_to_db(data_candles):
    """Save candles data to the PostgreSQL database"""
    conn = None
    cur = None
    try:
        # Read connection parameters from config
        params = config()

        # Connect to PostgreSQL database
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # Create a cursor object
        cur = conn.cursor()

        # Insert data into the database
        for candle in data_candles:
            cur.execute("""
                INSERT INTO candles (time, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (candle['t'], candle['o'], candle['h'], candle['l'], candle['c'], 0))  # Setting volume to 0
            
            print(f"Inserted row: {candle['t']}, {candle['o']}, {candle['h']}, {candle['l']}, {candle['c']}, 0")

        # Commit the transaction
        conn.commit()
        print(f"Inserted {len(data_candles)} rows into the database.")

    except psycopg2.Error as e:
        print(f"Error inserting data into PostgreSQL: {e}")

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()
            print('Database connection closed.')

# Example usage
# data_candles = get_chart_data('H1', 3600)
# save_to_db(data_candles)
get_chart_data('H1',3600)



