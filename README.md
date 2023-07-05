# Trading Data Analysis

This repository contains scripts for fetching, storing, analyzing, and visualizing trading data.

## Structure

The repository is structured into two main directories: `data_extractor` and `data_calculator`.

### data_extractor

The `data_extractor` directory contains scripts for fetching trading data from the BitMEX API and storing it into a SQLite database. It also contains a script for visualizing the stored data.

- `data_extractor.py`: Fetches trading data from the BitMEX API for different bin sizes ('1m', '5m', '1h', '1d') and for a specific time range. The data is stored into a SQLite database.

- `data_visualizator.py`: Fetches trading data from the SQLite database and visualizes it using the mplfinance library. The Open, High, Low, and Close (OHLC) values are plotted.

### data_calculator

The `data_calculator` directory contains scripts for fetching trading data from the SQLite database, calculating the Relative Strength Index (RSI) for the data, and storing the RSI values back into the database.

- `rsi_calculator.py`: Fetches trading data from the SQLite database, calculates the RSI for the data, and stores the RSI values back into the database. The RSI is calculated for different bin sizes ('1m', '5m', '1h', '1d').

- `rsi_print_values.py`: Fetches the RSI values calculated by the `rsi_calculator.py` script from the SQLite database and prints them. The RSI values are fetched for different bin sizes ('1m', '5m', '1h', '1d').

### utils

The `utils` directory contains utility scripts.

- `_delete_database.py`: Deletes the SQLite database if it exists.

## Usage

1. Run the `data_extractor.py` script to fetch trading data from the BitMEX API and store it into the SQLite database.

2. Run the `rsi_calculator.py` script to calculate the RSI for the stored data and store the RSI values intothe SQLite database.

3. Run the `rsi_print_values.py` script to print the calculated RSI values.

4. Run the `data_visualizator.py` script to visualize the stored trading data.

5. If needed, run the `_delete_database.py` script to delete the SQLite database.

## Requirements

- Python 3.6 or later
- pandas
- sqlite3
- mplfinance
- requests
- dateutil

## Disclaimer

This repository is for educational purposes only. No information is to be taken as financial advice. Use these scripts at your own risk.
