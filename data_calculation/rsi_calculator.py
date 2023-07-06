import sqlite3
import pandas as pd
import numpy as np

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

def calculate_rsi(df, period=14):
    delta = df['close'].diff()

    gain = delta.copy()
    gain[gain < 0] = 0
    loss = delta.copy()
    loss[loss > 0] = 0
    loss = loss.abs()

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    for i in range(period, len(df)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame({'timestamp': df['timestamp'], 'RSI': rsi})

    return rsi_df

def store_rsi(conn, table_name, rsi):
    rsi.to_sql(table_name + '_rsi', conn, if_exists='replace', index=False)

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f'XBTUSD_{bin_size}'
            df = fetch_data(conn, table_name)

            # Check if 'close' column exists and is numeric
            if 'close' in df.columns and pd.api.types.is_numeric_dtype(df['close']):
                # calculating RSI and storing it in a new dataframe
                rsi = calculate_rsi(df)
                store_rsi(conn, table_name, rsi)
                print(f'RSI data stored for table {table_name}')
            else:
                print(f"'close' column issue in table {table_name}")

if __name__ == '__main__':
    main()
