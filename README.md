# div-reg_test

This repository contains scripts for extracting, calculating, and visualizing trading data.

## Structure

The repository is divided into three main directories:

- `data_extraction`: Contains the `data_extractor.py` script which fetches trading data from the BitMEX API and stores it in a SQLite database.

- `data_calculation`: Contains the `rsi_calculator.py` and `extreme_price-rsi_values.py` scripts. The `rsi_calculator.py` script calculates the Relative Strength Index (RSI) for the trading data and stores it in the SQLite database. The `extreme_price-rsi_values.py` script finds extreme RSI and price values and stores them in the SQLite database.

- `data_visualization`: Contains the `print_OHLC_chart.py`, `print_extreme_rsi.py`, and `print_rsi_values.py` scripts. The `print_OHLC_chart.py` script plots OHLC (Open, High, Low, Close) candles on a chart and colors the candles in blue if they are matched with an extreme RSI value. The `print_extreme_rsi.py` and `print_rsi_values.py` scripts print the extreme RSI values and the RSI values, respectively.

- `utils`: Contains the `_delete_database.py` and `_drop_tables.py` scripts. The `_delete_database.py` script deletes the SQLite database. The `_drop_tables.py` script drops all tables from the SQLite database.

## Usage

1. Run the `data_extractor.py` script to fetch the trading data from the BitMEX API and store it in the SQLite database.

2. Run the `rsi_calculator.py` script to calculate the RSI for the trading data and store it in the SQLite database.

3. Run the `extreme_price-rsi_values.py` script to find extreme RSI and price values and store them in the SQLite database.

4. Run the `print_OHLC_chart.py`, `print_extreme_rsi.py`, and `print_rsi_values.py` scripts to visualize the trading data.

5. (Optional) Run the `_delete_database.py` and `_drop_tables.py` scripts to delete the SQLite database or drop all tables from the SQLite database.

## Requirements

- Python 3.6 or later
- pandas
- sqlite3
- mplfinance
- requests
- dateutil

## Disclaimer

This repository is for educational purposes only. No information is to be taken as financial advice. Use these scripts at your own risk.

## License

This project is licensed under the terms of the MIT license.