import requests
import sqlite3
from sqlite3 import Error
import json
import time
from dateutil.parser import parse


# Database connection setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

# Table creation
def create_table(conn, table_name):
    try:
        c = conn.cursor()
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                timestamp text UNIQUE, 
                symbol text, 
                open real, 
                high real, 
                low real, 
                close real, 
                trades integer, 
                volume real, 
                vwap real, 
                lastSize integer, 
                turnover integer, 
                homeNotional real, 
                foreignNotional real
            )
        """)
        print(f"Table {table_name} loaded successfully")
    except Error as e:
        print(e)

# Data insertion
def insert_data(conn, table_name, data):
    try:
        c = conn.cursor()
        for entry in data:
            c.execute(f"""
                INSERT OR IGNORE INTO {table_name} (
                    timestamp, 
                    symbol, 
                    open, 
                    high, 
                    low, 
                    close, 
                    trades, 
                    volume, 
                    vwap, 
                    lastSize, 
                    turnover, 
                    homeNotional, 
                    foreignNotional
                ) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry['timestamp'], 
                entry['symbol'], 
                entry['open'], 
                entry['high'], 
                entry['low'], 
                entry['close'], 
                entry['trades'], 
                entry['volume'], 
                entry['vwap'], 
                entry['lastSize'], 
                entry['turnover'], 
                entry['homeNotional'], 
                entry['foreignNotional']
            ))
        conn.commit()
        print("Data inserted successfully")
    except Error as e:
        print(e)

# API request with error handling
def get_bucketed_trades(binSize, start_time, end_time):
    url = "https://www.bitmex.com/api/v1/trade/bucketed"
    params = {
        "binSize": binSize,
        "partial": "false",
        "symbol": "XBTUSD",
        "count": 1000,
        "reverse": "false",
        "startTime": start_time,
        "endTime": end_time
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

# Fetch latest timestamp
def get_latest_timestamp(conn, table_name, default_start_date):
    try:
        c = conn.cursor()
        c.execute(f"SELECT MAX(timestamp) FROM {table_name}")
        result = c.fetchone()[0]
        if result is None:
            return default_start_date
        else:
            return result
    except Error as e:
        print(e)
        return default_start_date

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f"XBTUSD_{bin_size}"
            create_table(conn, table_name)
            default_start_date = '2023-01-01T00:00:00Z' # where you start search
            default_end_date = '2023-07-03T00:00:00Z' # when you want the search to stop
            start_time = get_latest_timestamp(conn, table_name, default_start_date)
            print(f'Start  date for data extraction: {start_time}')
            print(f'End date for the data extraction: {default_end_date}')
            while parse(start_time) < parse(default_end_date):
                data = get_bucketed_trades(bin_size, start_time, default_end_date)
                if data and len(data) > 0:
                    print(f'Retrieved data from {start_time} to {data[-1]["timestamp"]}')
                    insert_data(conn, table_name, data)
                    start_time = data[-1]['timestamp']
                    print(f'Updated start_time to {start_time}')
                    time.sleep(2)  # delay to respect the BitMEX API rate limit
                else:
                    break


if __name__ == '__main__':
    main()
