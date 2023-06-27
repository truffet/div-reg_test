import requests
import sqlite3
from sqlite3 import Error
import json
import time

# Database connection setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

# Table creation
def create_table(conn, table_name):
    try:
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (data text, timestamp text, UNIQUE(timestamp))")
        print(f"Table {table_name} created successfully")
    except Error as e:
        print(e)

# Data insertion
def insert_data(conn, table_name, data):
    try:
        c = conn.cursor()
        for entry in data:
            timestamp = entry['timestamp']
            c.execute(f"INSERT OR IGNORE INTO {table_name}(data, timestamp) VALUES(?, ?)", (json.dumps(data), timestamp))
        conn.commit()
        print("Data inserted successfully")
    except Error as e:
        print(e)

# API request with error handling
def get_bucketed_trades(binSize, start_time=None):
    url = "https://www.bitmex.com/api/v1/trade/bucketed"
    params = {
        "binSize": binSize,
        "partial": "false",
        "symbol": "XBTUSD",
        "count": 1000,
        "reverse": "false",
        "startTime": start_time,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print ("Request error:",err)
        return None
    except requests.exceptions.HTTPError as errh:
        print ("HTTP error:",errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print ("Error connecting:",errc)
        return None
    except requests.exceptions.Timeout as errt:
        print ("Timeout error:",errt)
        return None
    return response.json()


def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f"XBTUSD_{bin_size}"
            create_table(conn, table_name)
            
            start_time = None
            while True:
                data = get_bucketed_trades(bin_size, start_time)
                if data is not None and len(data) > 0:
                    insert_data(conn, table_name, data)
                    start_time = data[-1]['timestamp']
                    time.sleep(2)  # delay to respect the BitMEX API rate limit
                else:
                    break

if __name__ == '__main__':
    main()
