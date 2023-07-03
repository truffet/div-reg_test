import sqlite3
import pandas as pd
import numpy as np

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
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def store_divergences(conn, table_name, divergence_list):
    c = conn.cursor()
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            timer_timestamp text, 
            timer_RSI real, 
            current_timestamp text, 
            current_RSI real
        )
    """)
    for div in divergence_list:
        c.execute(f"""
            INSERT INTO {table_name} (
                timer_timestamp, 
                timer_RSI, 
                current_timestamp, 
                current_RSI
            ) 
            VALUES (?, ?, ?, ?)
        """, (
            div[0], 
            div[1], 
            div[2], 
            div[3]
        ))
    conn.commit()
    print(f"Divergences stored successfully in table {table_name}")

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            table_name = f'XBTUSD_{bin_size}_rsi'
            df = fetch_data(conn, table_name)
            divergence = []
            state = None
            timer = None

            for i in range(1, len(df)):
                current = df.iloc[i]
                if state == "short" and current['RSI'] < timer['RSI'] and current['high'] > timer['high']:
                    divergence.append((str(timer['timestamp']), timer['RSI'], str(current['timestamp']), current['RSI']))
                elif state == "long" and current['RSI'] > timer['RSI'] and current['low'] < timer['low']:
                    divergence.append((str(timer['timestamp']), timer['RSI'], str(current['timestamp']), current['RSI']))

                if current['RSI'] >= 70:
                    state = "short"
                    if timer is not None and current['RSI'] > timer['RSI']:
                        timer = current
                    elif timer is None:
                        timer = current
                elif current['RSI'] <= 30:
                    state = "long"
                    if timer is not None and current['RSI'] < timer['RSI']:
                        timer = current
                    elif timer is None:
                        timer = current

            divergence_table_name = f'XBTUSD_{bin_size}_rsi_divergences'
            store_divergences(conn, divergence_table_name, divergence)

if __name__ == '__main__':
    main()
