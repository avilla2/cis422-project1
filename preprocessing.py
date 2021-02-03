import pandas as pd
from numpy import log10
import sklearn as sk

"""
parameters
    input: filename of a csv file
returns
    returns Dataframe of the csv file data
"""


def read(input):
    # df = pd.read_csv(input, parse_dates=True, infer_datetime_format=True)  # use if there's only one date/time column
    df = pd.read_csv(input, nrows=1)
    x, y = df.shape
    if y == 3:
        df = pd.read_csv(input, parse_dates={'Datetime': [0, 1]}, infer_datetime_format=True)
    elif y == 2:
        df = pd.read_csv(input, parse_dates={'Datetime': [0]}, infer_datetime_format=True)
    else:
        df = pd.read_csv(input, names=["Time Series"])
    return df


def denoise(ts: pd.DataFrame) -> None:
    """
    Removes noise from a time series. Produces a time series with less noise than
    the original one. This function can be implemented using moving (or rolling) media or median
    (included in the Pandas library.)
    """
    # Implementing 5 point moving average
    ts.iloc[:, -1:] = ts.iloc[:, -1:].rolling(window=5).mean()
    return ts


def impute_missing_data(ts):
    """
    Missing data are often encoded as blanks, NaNs, or other
    placeholders. At this point, let us assume that a single point is missing, and it can be computed
    from its adjacent points in time.
    """
    pass


def impute_outliers(ts):
    '''
    – Outliers are disparate data that we can treat as missing data. Use the
    same procedure as for missing data (sklearn implements outlier detection.) This function is better
    applied using the higher dimensional data produced by TS2DB (see below.)
    '''
    pass


def longest_continuous_run(ts):
    '''
    – Isolates the most extended portion of the time series without
    missing data. It returns a time series.
    '''
    pass


def clip(ts, starting_date, final_date):
    '''
    clips the time series to the specified period’s data.
    '''
    pass


def assign_time(ts, start, increment):
    '''
    In many cases, we do not have the times associated
    with a sequence of readings. Start and increment represent t0 delta, respectively.
    '''
    pass


def difference(ts):
    '''
    Produces a time series whose magnitudes are the differences between
    consecutive elements in the original time series.
    '''
    pass


def scaling(ts):
    '''
    Produces a time series whose magnitudes are scaled so that the resulting
    magnitudes range in the interval [0,1].
    '''
    floor = float(ts.iloc[:, -1:].min())
    ceiling = float(ts.iloc[:, -1:].max())
    diff = ceiling - floor  # range
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: (x - floor) / diff)


def standardize(ts):
    """
    Produces a time series whose mean is 0 and variance is 1.
    """
    mu = float(ts.iloc[:, -1:].mean())
    sigma = float(ts.iloc[:, -1:].std())
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: (x - mu) / sigma)


def logarithm(ts):
    """
    Produces a time series whose elements are the logarithm of the original
    elements.
    """
    ts.iloc[:, -1:] = log10(ts.iloc[:, -1:])


def cubic_root(ts):
    """
    Produces a time series whose elements are the original elements’ cubic root
    """
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: x ** (1 / 3))


# Splits the data based on the percents (in decimal notation).
# Percents must add to 1.0 and training and test percents cannot be 0.0.
def split_data(df, perc_training=.4, perc_valid=.3, perc_test=.3):
    total = perc_training + perc_valid + perc_test
    if total != 1:
        raise Exception("Error. Split data percents must add up to 1.0")
    if perc_training == 0 or perc_test == 0:
        raise Exception("Error. Training and Test percents must not be 0.0")

    x, y = df.shape
    t1 = round(x * perc_training)
    t2 = round(x * perc_valid) + t1

    train_df = df.iloc[:t1, :]
    valid_df = df.iloc[t1:t2, :]
    test_df = df.iloc[t2:, :]

    return train_df, valid_df, test_df


def design_matrix(ts, input_index, output_index):
    pass


"""
design matrix
    from the parameters, this function creates an input matrix and an output matrix for the neural network to train on
    it works by collecting the appropriate frames, transforming those frames into 2 dataframes (input and output) and
    then transforming those dataframes into numpy arrays (matrices)
    It is currently very slow.
parameters
    ts: time series (dataframe)
    mi: number of test input points (integer)
    ti: distance between test input points (integer)
    mo: number of test output points (integer)
    to: distance between test output points (integer)

returns
    two matrices
"""


def design_matrix(df, mi=4, ti=2, mo=4, to=1):
    x, y = df.shape

    tail = 0
    input_array = []
    for i in range(mi):
        tail = i * ti
        input_array.append(tail)
        tail += 1
    output_array = []
    for i in range(mo):
        output_array.append(i * to + tail)

    # print(input_array, output_array)
    # print(df.iloc[input_array])
    # print(df.iloc[output_array])

    input_matrix = []
    output_matrix = []
    while output_array[-1] < x:
        i_frames = []
        o_frames = []
        for i in input_array:
            i_frames.append(df.iloc[i, 1])
        for i in output_array:
            o_frames.append(df.iloc[i, 1])
        input_matrix.append(i_frames)
        output_matrix.append(o_frames)
        input_array = [x + 1 for x in input_array]
        output_array = [x + 1 for x in output_array]

    # print(input_matrix)
    # print(output_matrix)

    return output_matrix, input_matrix


def ts2dbb(input_filename, perc_training, perc_valid, perc_test, input_index,
           output_index, output_file_name):
    '''
    this function combines reading a file, splitting the
    data, converting to database, and producing the training databases.
    '''
    pass
