"""
Pre-processing Transformations
CIS 422 Group 3
Function Library for pre-processing time series data
"""
import pandas as pd

'''
Data from csv files will be read (using another python file, work in progress) and converted
to pandas Series ex:

ages = pd.Series([22, 35, 58], name="Age")
Api Reference Here: 
https://pandas.pydata.org/docs/reference/series.html
'''


def denoise(ts: "Series"):
    pass


def impute_missing_data(ts):
    pass


def impute_outliers(ts):
    pass


def longest_continuous_run(ts):
    pass


def clip(ts, starting_date, final_date):
    pass


def assign_time(ts, start, increment):
    pass


def difference(ts):
    pass


def scaling(ts):
    pass


def standardize(ts):
    pass


def logarithm(ts):
    pass


def cubic_root(ts):
    pass


def split_data(ts, perc_training, perc_valid, perc_test):
    pass


def design_matrix(ts, input_index, output_index):
    pass


def design_matrix2(ts, mi, ti, mo, to):
    pass


def ts2db(input_filename, perc_training, perc_valid, perc_test, input_index, output_index, output_file_name):
    pass