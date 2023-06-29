import sqlite3
import pandas as pd
import mplfinance as mpf
from dateutil.parser import parse

# Database connection setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

def main():
    conn = create_connection()
    if conn is not None:
        table_name = 'XBTUSD_1d'  # replace with your table name
        df = fetch_data(conn, table_name)
        df['timestamp'] = df['timestamp'].apply(parse)
        df.set_index('timestamp', inplace=True)

        # converting the data column from string to dictionary
        df['data'] = df['data'].apply(eval)

        # creating separate columns for open, high, low and close
        df['Open'] = df['data'].apply(lambda x: x['open'])
        df['High'] = df['data'].apply(lambda x: x['high'])
        df['Low'] = df['data'].apply(lambda x: x['low'])
        df['Close'] = df['data'].apply(lambda x: x['close'])

        # selecting only the OHLC columns
        ohlc_df = df[['Open', 'High', 'Low', 'Close']]

        # plot the data using mplfinance
        mpf.plot(ohlc_df, type='candle', style='charles', title='XBTUSD 1d Candlestick Chart')

if __name__ == '__main__':
    main()
