import sqlite3
import pandas as pd

# Database connection setup
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

def calculate_rsi(df, period=14):
    daily_returns = df['Close'].diff()
    positive_returns = daily_returns.where(daily_returns > 0, 0)
    negative_returns = -daily_returns.where(daily_returns < 0, 0)
    positive_avg = positive_returns.ewm(span=period).mean()
    negative_avg = negative_returns.ewm(span=period).mean()
    rsi = 100 - (100 / (1 + (positive_avg / negative_avg)))
    return rsi

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f'XBTUSD_{bin_size}'
            df = fetch_data(conn, table_name)

            # converting the data column from string to dictionary
            df['data'] = df['data'].apply(eval)

            # creating separate columns for open, high, low and close
            df['Open'] = df['data'].apply(lambda x: x[0]['open'])
            df['High'] = df['data'].apply(lambda x: x[0]['high'])
            df['Low'] = df['data'].apply(lambda x: x[0]['low'])
            df['Close'] = df['data'].apply(lambda x: x[0]['close'])

            # calculating RSI and storing it in a new column 'RSI'
            df['RSI'] = calculate_rsi(df)

            # storing the updated dataframe back into the database
            df.to_sql(table_name, conn, if_exists='replace')

if __name__ == '__main__':
    main()
