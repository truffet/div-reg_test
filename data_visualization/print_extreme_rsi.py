import sqlite3
import pandas as pd

# Database connection setup
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    return conn

def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

def print_extreme_values(df):
    for index, row in df.iterrows():
        print(f"RSI: {row['RSI']}, Price: {row['Price']}")

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f'XBTUSD_{bin_size}_extreme_values'
            df = fetch_data(conn, table_name)
            print(f"Extreme values for {bin_size} bin size:")
            print_extreme_values(df)

if __name__ == '__main__':
    main()
