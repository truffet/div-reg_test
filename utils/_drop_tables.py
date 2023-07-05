import sqlite3

# Database connection setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    return conn

def drop_tables(conn):
    cursor = conn.cursor()

    # Get the list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        table_name = table_name[0]
        # # Uncomment the tables you want to keep
        if table_name == 'XBTUSD_1m':
            continue
        if table_name == 'XBTUSD_5m':
            continue
        if table_name == 'XBTUSD_1h':
            continue
        if table_name == 'XBTUSD_1d':
            continue
        # if table_name == 'XBTUSD_1m_rsi':
        #     continue
        # if table_name == 'XBTUSD_5m_rsi':
        #     continue
        # if table_name == 'XBTUSD_1h_rsi':
        #     continue
        # if table_name == 'XBTUSD_1d_rsi':
        #     continue
        # if table_name == 'XBTUSD_1m_extreme_values':
        #     continue
        # if table_name == 'XBTUSD_5m_extreme_values':
        #     continue
        # if table_name == 'XBTUSD_1h_extreme_values':
        #     continue
        # if table_name == 'XBTUSD_1d_extreme_values':
        #     continue
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Dropped table {table_name}")

    conn.commit()

def main():
    conn = create_connection()
    if conn is not None:
        drop_tables(conn)

if __name__ == '__main__':
    main()
