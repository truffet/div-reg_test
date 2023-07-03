import sqlite3
import pandas as pd
import mplfinance as mpf
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

def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

def main():
    conn = create_connection()
    if conn is not None:
        table_name = 'XBTUSD_1h'  # replace with your table name
        df = fetch_data(conn, table_name)
        
        if df.empty:
            print(f'No data fetched from table {table_name}')
            return

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        # renaming the columns to match mplfinance expectations
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close'
        })

        # selecting only the OHLC columns
        ohlc_df = df[['Open', 'High', 'Low', 'Close']]

        if ohlc_df.empty:
            print('OHLC DataFrame is empty after processing')
            return

        # plot the data using mplfinance
        mpf.plot(ohlc_df, type='candle', style='charles', title=table_name)

if __name__ == '__main__':
    main()
