"""
Input and Output Functions
CIS 422 Group 3
Functions to read and write to csv files
"""
import pandas as pd


def read_from_file(input_file_name):
    """input_file_name: str -> Series"""
    csv_data = pd.read_csv(input_file_name)
    return csv_data


def write_to_file(output_file_name):
    """input_file_name: str -> Series"""
    pass
