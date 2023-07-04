import sqlite3
import pandas as pd

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    return conn

def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT timestamp, RSI FROM {table_name}_rsi", conn)  # Modify the query to fetch RSI from the correct table
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f'XBTUSD_{bin_size}'
            print(f'Fetching data from table: {table_name}_rsi')  # Update the table name to include "_rsi"
            df = fetch_data(conn, table_name)
            print(f'RSI values for {bin_size} bin size:')
            print(df)

if __name__ == '__main__':
    main()
