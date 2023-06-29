import os

# Define the path to the database
db_path = "../database/bitmex.db"

# Check if the database exists
if os.path.exists(db_path):
    # Delete the database
    os.remove(db_path)
    print(f"Database {db_path} deleted successfully.")
else:
    print(f"No database found at {db_path}.")
