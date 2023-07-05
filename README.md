# Trading Data Analysis

This repository contains scripts for fetching, storing, analyzing, and visualizing trading data.

## Structure

The repository is structured into three main directories: `data_extraction`, `data_calculation`, and `data_visualization`.

### data_extraction

The `data_extraction` directory contains a script for fetching trading data from the BitMEX API and storing it into a SQLite database.

- `data_extractor.py`: Fetches trading data from the BitMEX API for different bin sizes ('1m', '5m', '1h', '1d') and for a specific time range. The data is stored into a SQLite database.

### data_calculation

The `data_calculation` directory contains a script for fetching trading data from the SQLite database, calculating the Relative Strength Index (RSI) for the data, and storing the RSI values back into the database.

- `rsi_calculator.py`: Fetches trading data from the SQLite database, calculates the RSI for the data, and stores the RSI values back into the database. The RSI is calculated for different bin sizes ('1m', '5m', '1h', '1d').

### data_visualization

The `data_visualization` directory contains scripts for visualizing the stored and calculated data.

- `OHLC_print_chart.py`: Fetches trading data from the SQLite database and visualizes it using the mplfinance library. The Open, High, Low, and Close (OHLC) values are plotted.

- `rsi_print_values.py`: Fetches the RSI values calculated by the `rsi_calculator.py` script from the SQLite database and prints them. The RSI values are fetched for different bin sizes ('1m', '5m', '1h', '1d').

### utils

The `utils` directory contains utility scripts.

- `_delete_database.py`: Deletes the SQLite database if it exists.

## Usage

1. Run the `data_extractor.py` script to fetch trading data from the BitMEX API and store it into the SQLite database.

2. Run the `rsi_calculator.py` script to calculate the RSI for the stored data and store the RSI values into the SQLite database.

3. Run the `rsi_print_values.py` script to print the calculated RSI values.

4. Run the `OHLC_print_chart.py` script to visualize the stored trading data.

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
