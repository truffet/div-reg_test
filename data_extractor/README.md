# div-reg_test
# BitMEX API Data Fetch and Store

This Python script fetches bucketed trade data from the BitMEX API for the XBTUSD perpetual contract with bin sizes of 1 minute, 5 minutes, 1 hour, and 1 day. The fetched data is then stored into a SQLite database with a separate table for each bin size.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You need Python 3.6+ installed on your machine. You can verify your Python version with the following command:

python --version

You also need the `requests` and `sqlite3` libraries. You can install them with pip:

pip install requests sqlite3

### Installation

Clone this repository or download the Python script to your local machine.

## Usage

To run the script, navigate to the directory containing the script and use the following command in your terminal:

python data_extractor.py

## Functionality

The script performs the following tasks:

1. Establishes a connection to a SQLite database named `bitmex.db`.
2. For each bin size ('1m', '5m', '1h', '1d'), it:
    - Creates a table (if it doesn't exist).
    - Sends a GET request to the BitMEX API to fetch the bucketed trade data.
    - Inserts the fetched data into the respective table.
3. Includes a one-second delay between each API request to respect the BitMEX API rate limit.
4. Includes basic error handling for API requests.

## Notes

- The fetched data is stored in the database as JSON strings. You might want to parse the JSON and store the data in separate columns if you want to perform SQL queries on the data.
- The script includes a one-second delay between each API request to respect the BitMEX API rate limit. Adjust this delay as necessary according to the actual rate limit mentioned in the BitMEX API documentation.
- The script includes basic error handling for API requests. For a production script, consider adding more comprehensive error handling and logging.
- This script is intended for learning purposes and is not ready for production use without further modifications and robust testing.

## Authors

- Thomas Ruffet

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

- Thanks to the BitMEX API for providing the data.
