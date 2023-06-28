import sqlite3
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('bitmex.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def get_1d_data(conn):
    table_name = "XBTUSD_1m"
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")

    timestamps = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    while True:
        rows = c.fetchmany(10000)  # fetch 10000 rows at a time
        if not rows:
            break

        for row in rows:
            data = json.loads(row[0])
            for trade in data:
                timestamps.append(datetime.datetime.strptime(trade['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ"))
                opens.append(trade['open'])
                highs.append(trade['high'])
                lows.append(trade['low'])
                closes.append(trade['close'])
                volumes.append(trade['volume'])

    return timestamps, opens, highs, lows, closes, volumes

def plot_data(timestamps, opens, highs, lows, closes, volumes):
    fig, ax1 = plt.subplots()

    # plot OHLC data
    ax1.plot(timestamps, opens, label='Open')
    ax1.plot(timestamps, highs, label='High')
    ax1.plot(timestamps, lows, label='Low')
    ax1.plot(timestamps, closes, label='Close')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price')
    ax1.legend()

    # plot volume data on a separate axis
    ax2 = ax1.twinx()
    ax2.bar(timestamps, volumes, alpha=0.2, color='grey')
    ax2.set_ylabel('Volume')

    fig.autofmt_xdate()  # auto format the x-axis date labels
    plt.show()

def main():
    conn = create_connection()
    if conn is not None:
        timestamps, opens, highs, lows, closes, volumes = get_1d_data(conn)
        plot_data(timestamps, opens, highs, lows, closes, volumes)

if __name__ == '__main__':
    main()
