import sqlite3
import json

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('bitmex.db')
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def get_date_range(conn, table_name):
    c = conn.cursor()

    # Fetch first row
    c.execute(f"SELECT data FROM {table_name} LIMIT 1")
    first_row = c.fetchone()
    first_data = json.loads(first_row[0])
    first_date = first_data[0]['timestamp']  # get timestamp of the first trade in the first row

    # Fetch last row
    c.execute(f"SELECT data FROM {table_name} ORDER BY ROWID DESC LIMIT 1")
    last_row = c.fetchone()
    last_data = json.loads(last_row[0])
    last_date = last_data[-1]['timestamp']  # get timestamp of the last trade in the last row

    return first_date, last_date

def main():
    conn = create_connection()
    if conn is not None:
        table_names = ["XBTUSD_1m", "XBTUSD_5m", "XBTUSD_1h", "XBTUSD_1d"]
        for table_name in table_names:
            first_date, last_date = get_date_range(conn, table_name)
            print(f"For {table_name}, the first data point is on {first_date} and the last data point is on {last_date}")

if __name__ == '__main__':
    main()
