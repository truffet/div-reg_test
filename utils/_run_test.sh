#!/bin/bash

# run the scripts
python3 _drop_tables.py
python3 ../data_calculation/rsi_calculator.py
python3 ../data_visualization/print_rsi_values.py
