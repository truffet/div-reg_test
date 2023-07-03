import sqlite3

# Database connection setup
def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('../database/bitmex.db')  # create a database connection to a SQLite database
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    return conn

def fetch_divergences(conn, table_name):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    return c.fetchall()

def main():
    conn = create_connection()
    if conn is not None:
        bin_sizes = ['1m', '5m', '1h', '1d']
        for bin_size in bin_sizes:
            divergence_table_name = f'XBTUSD_{bin_size}_rsi_divergences'
            divergences = fetch_divergences(conn, divergence_table_name)
            
            print(f"Divergences for {bin_size} bin size:")
            for div in divergences:
                print(f"Timer Datetime: {div[0]}, Timer RSI: {div[1]}, Current Datetime: {div[2]}, Current RSI: {div[3]}")
            print()

if __name__ == '__main__':
    main()
