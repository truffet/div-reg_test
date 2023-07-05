import sqlite3
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

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

def plot_data(df_ohlc, df_rsi, df_extreme_values):
    # Convert timestamp to datetime and set it as index
    df_ohlc['timestamp'] = pd.to_datetime(df_ohlc['timestamp'])
    df_ohlc.set_index('timestamp', inplace=True)
    df_rsi['timestamp'] = pd.to_datetime(df_rsi['timestamp'])
    df_rsi.set_index('timestamp', inplace=True)

    # Create a new column for the color of the OHLC candles
    df_ohlc['color'] = 'r'
    df_ohlc.loc[df_ohlc.index.isin(df_extreme_values['timestamp']), 'color'] = 'b'

    # Create a custom style
    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)

    # Create the OHLC plot
    fig, axes = mpf.plot(df_ohlc, type='candle', style=s, returnfig=True)

    # Create the RSI plot
    axes[0].plot(df_rsi.index, df_rsi['RSI'])

    # Show the plot
    plt.show()

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1d']
        for bin_size in bin_sizes:
            table_name_ohlc = f'XBTUSD_{bin_size}'
            table_name_rsi = f'XBTUSD_{bin_size}_rsi'
            table_name_extreme_values = f'XBTUSD_{bin_size}_extreme_values'
            df_ohlc = fetch_data(conn, table_name_ohlc)
            df_rsi = fetch_data(conn, table_name_rsi)
            df_extreme_values = fetch_data(conn, table_name_extreme_values)
            #
            df = pd.read_sql_query("SELECT * FROM XBTUSD_1m_extreme_values LIMIT 5", conn)
            print(df)
            #
            #plot_data(df_ohlc, df_rsi, df_extreme_values)

if __name__ == '__main__':
    main()
