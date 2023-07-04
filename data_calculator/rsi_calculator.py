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

# Check if the table exists in the database
def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone()[0] == 1:
        return True
    else:
        return False

# Fetch OHLC data from the database
def fetch_data(conn, table_name):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    return df

# Calculate RSI values
def calculate_rsi(df, period=14):
    daily_returns = df['Close'].diff()
    positive_returns = daily_returns.where(daily_returns > 0, 0)
    negative_returns = -daily_returns.where(daily_returns < 0, 0)
    positive_avg = positive_returns.ewm(span=period).mean()
    negative_avg = negative_returns.ewm(span=period).mean()
    rsi = 100 - (100 / (1 + (positive_avg / negative_avg)))
    return rsi

# Store RSI values in the database
def store_rsi(conn, table_name, rsi):
    rsi_df
