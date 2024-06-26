import os
import psycopg2
from flask import Flask, jsonify
import requests
import json
import time
from config import config

app = Flask(__name__)

class CandleData:
    def __init__(self):
        self.url = "****"
        self.params = {
            'widgetName': '***',
            'apikey': '***',
            'Remote Address': '****',
            'Request-Context': '****',
            'region': 'OEL',
            'instrumentName': '****',
            "granularity": ""
        }

    def fetch_data(self, granularity):
        self.params['granularity'] = granularity
        try:
            with requests.post(self.url, params=self.params) as response:
                response.raise_for_status()
                print(f"Status Code: {response.status_code}")
                candles = response.json().get('candles', [])
                return candles
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return []

    def create_table(self, cur, table_name):
        # Create table
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                time TIMESTAMPTZ PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume FLOAT
            );
        """)
    
    def save_to_db(self, data_candles, table_name):
        """Save candles data to the PostgreSQL database"""
        try:
            # Read connection parameters from config
            params = config()

            # Connect to PostgreSQL database
            print('Connecting to the PostgreSQL database...')
            with psycopg2.connect(**params) as conn:
                with conn.cursor() as cur:
                    # Create table
                    self.create_table(cur, table_name)

                    # Map the data to the format required for the database
                    mapped_data = list(map(lambda candle: (candle['time'], candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c'], 0), data_candles))

                    # Insert data into the database
                    for data in mapped_data:
                        try:
                            cur.execute(f"""
                                INSERT INTO {table_name} (time, open, high, low, close, volume)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                ON CONFLICT (time) DO NOTHING
                            """, data)
                        except psycopg2.IntegrityError as e:
                            conn.rollback()
                            print(f"Skipping duplicate entry for timestamp {data[0]}")
                    
                    # Commit the transaction
                    conn.commit()
                    print(f"Inserted {len(data_candles)} rows into the {table_name} table.")

        except psycopg2.Error as e:
            print(f"Error inserting data into PostgreSQL: {e}")
            return False
        return True

    def get_chart_data(self, data_list):
        for item in data_list:
            granularity = item['granularity']
            sleep_time = item['sleep_time']
            
            table_name = f"candles_{granularity}"
            
            # Sending each item to the while loop
            self.process_data(granularity, sleep_time, table_name)

    def process_data(self, granularity, sleep_time, table_name):
        while True:
            candles = self.fetch_data(granularity)
            
            print(f"Inserted {len(candles)} candles from the API for granularity {granularity}.")
            if candles:
                data_candles = [
                    {
                        'time': candle['time'],
                        'mid': {
                            'o': candle['mid']['o'],
                            'h': candle['mid']['h'],
                            'l': candle['mid']['l'],
                            'c': candle['mid']['c']
                        }
                    } for candle in candles
                ]
                self.save_to_db(data_candles, table_name)
                print(data_candles)
                time.sleep(sleep_time)

@app.route('/fetch_data', methods=['GET'])
def fetch_data_from_api():
    data_list = [
        {'granularity': 'M', 'sleep_time': 3600},
        {'granularity': 'D', 'sleep_time': 86400},
        {'granularity': 'W', 'sleep_time': 604800},
        {'granularity': 'M', 'sleep_time': 2592000}
    ]
    candle_data = CandleData()
    candle_data.get_chart_data(data_list)
    return jsonify({"message": "Data fetching started"})

if __name__ == "__main__":
    app.run(debug=True)




