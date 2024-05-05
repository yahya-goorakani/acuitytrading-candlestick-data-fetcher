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
    url = "****"
    params = {
        'widgetName': '***',
        'apikey': '****',
        'Remote Address': '****',
        'Request-Context': '****',
        'granularity': '****',
        'instrumentName': '***',
        'region': '***'
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



