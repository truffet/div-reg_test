import sqlite3  
import pandas as pd  

# Database connection setup  
def create_connection():  
    conn = None  
    try:  
        conn = sqlite3.connect('../database/bitmex.db') # create a database connection to a SQLite database  
        print(f'successful connection with sqlite version {sqlite3.version}')  
    except sqlite3.Error as e:  
        print(e)  
    return conn  

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cur.fetchone()[0]==1:
        return True
    else:
        return False

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

def store_rsi(conn, table_name, rsi):  
    rsi_df = pd.DataFrame(rsi, columns=['timestamp', 'RSI'])  
    rsi_df.to_sql(table_name + '_rsi', conn, if_exists='append', index=False)  

def main():  
    conn = create_connection()  
    if conn is not None:  
        bin_sizes = ['1m', '5m', '1h', '1d']  
        for bin_size in bin_sizes:  
            table_name = f'XBTUSD_{bin_size}'
            if table_exists(conn, table_name):
                df = fetch_data(conn, table_name)
                # directly use the open, high, low, and close columns  
                df['Open'] = df['open']
                df['High'] = df['high']  
                df['Low'] = df['low']  
                df['Close'] = df['close']  

                # Check if 'Close' column exists and is numeric
                if 'Close' in df.columns and pd.api.types.is_numeric_dtype(df['Close']):
                    # calculating RSI and storing it in a new dataframe  
                    rsi = calculate_rsi(df)  
                    store_rsi(conn, table_name, rsi)  
                else:
                    print(f"'Close' column issue in table {table_name}")
            else:
                print(f"Table {table_name} does not exist")

if __name__ == '__main__':  
    main()
