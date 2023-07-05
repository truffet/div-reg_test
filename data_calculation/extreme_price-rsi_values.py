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

def find_extreme_values(df_ohlc, df_rsi):
    extreme_values = []
    i = 0
    while i < len(df_rsi):
        if df_rsi['RSI'].iloc[i] >= 70:
            max_rsi = df_rsi['RSI'].iloc[i]
            max_price_high = df_ohlc['high'].iloc[i]
            timestamp = df_ohlc['timestamp'].iloc[i]
            while i < len(df_rsi) and df_rsi['RSI'].iloc[i] >= 70:
                if df_rsi['RSI'].iloc[i] > max_rsi:
                    max_rsi = df_rsi['RSI'].iloc[i]
                    max_price_high = df_ohlc['high'].iloc[i]
                    timestamp = df_ohlc['timestamp'].iloc[i]
                i += 1
            extreme_values.append((timestamp, max_rsi, max_price_high))
        elif df_rsi['RSI'].iloc[i] <= 30:
            min_rsi = df_rsi['RSI'].iloc[i]
            min_price_low = df_ohlc['low'].iloc[i]
            timestamp = df_ohlc['timestamp'].iloc[i]
            while i < len(df_rsi) and df_rsi['RSI'].iloc[i] <= 30:
                if df_rsi['RSI'].iloc[i] < min_rsi:
                    min_rsi = df_rsi['RSI'].iloc[i]
                    min_price_low = df_ohlc['low'].iloc[i]
                    timestamp = df_ohlc['timestamp'].iloc[i]
                i += 1
            extreme_values.append((timestamp, min_rsi, min_price_low))
        else:
            i += 1
    return extreme_values

def store_extreme_values(conn, table_name, extreme_values):
    df = pd.DataFrame(extreme_values, columns=['timestamp', 'RSI', 'Price'])
    df.to_sql(table_name + '_extreme_values', conn, if_exists='replace', index=False)


def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name_ohlc = f'XBTUSD_{bin_size}'
            table_name_rsi = f'XBTUSD_{bin_size}_rsi'
            df_ohlc = fetch_data(conn, table_name_ohlc)
            df_rsi = fetch_data(conn, table_name_rsi)
            extreme_values = find_extreme_values(df_ohlc, df_rsi)
            store_extreme_values(conn, table_name_ohlc, extreme_values)

if __name__ == '__main__':
    main()
