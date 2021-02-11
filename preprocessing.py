import pandas as pd
from numpy import log10, nan
from datetime import datetime
from sklearn.neighbors import LocalOutlierFactor

"""
parameters
    input: filename of a csv file
returns
    returns Dataframe of the csv file data
"""


def read(filename):
    # df = pd.read_csv(input, parse_dates=True, infer_datetime_format=True)  # use if there's only one date/time column
    df = pd.read_csv(filename, nrows=1)
    x, y = df.shape
    if y == 3:
        df = pd.read_csv(filename, parse_dates={'Datetime': [0, 1]}, infer_datetime_format=True)
    elif y == 2:
        df = pd.read_csv(filename, parse_dates={'Datetime': [0]}, infer_datetime_format=True)
    else:
        df = pd.read_csv(filename, names=["Time Series"])
    return df


def denoise(ts: pd.DataFrame) -> pd.DataFrame:
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
    ts.iloc[:, -1:] = ts.iloc[:, -1:].fillna(method="bfill")
    ts.iloc[:, -1:] = ts.iloc[:, -1:].fillna(method="pad")
    return ts


def impute_outliers(ts):
    """
    – Outliers are disparate data that we can treat as missing data. Use the
    same procedure as for missing data (sklearn implements outlier detection.) This function is better
    applied using the higher dimensional data produced by TS2DB (see below.)
    """
    clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
    clf.fit_predict(ts.iloc[:, -1:])
    scores = clf.negative_outlier_factor_
    deletion_list = []
    for i in range(len(scores)):
        if scores[i] < -2:
            deletion_list.append(i)
    for j in deletion_list:
        ts.iloc[j, -1:] = nan
    ts = impute_missing_data(ts)
    return ts


def longest_continuous_run(ts):
    """
    – Isolates the most extended portion of the time series without
    missing data. It returns a time series.
    """
    start = 0
    ts_len = len(ts)
    ending = ts_len
    cnt = 0
    ts_max = 0
    first = 1
    na_find = ts.iloc[:, -1:].isna()
    for i in range(ts_len):
        if na_find.iloc[i, :].bool() == False and first == 1 and cnt >= ts_max:
            start = i
            first = 0
        if na_find.iloc[i, :].bool() == False and first == 0 and cnt >= ts_max:
            cnt += 1
        if na_find.iloc[i, :].bool() == True and first == 0:
            ending = i
            first = 1
            cnt = 0
    if cnt >= ts_max and first == 0:
        ending = ts_len + 1
    return ts.iloc[start:ending, :]

def clip(ts, starting_date, final_date):
    """
    clips the time series to the specified period’s data.
    """
    return ts.iloc[starting_date:final_date, -1:]


def assign_time(ts: pd.DataFrame, start: int, increment: int) -> pd.DataFrame:
    """
    In many cases, we do not have the times associated
    with a sequence of readings. Start and increment represent t0 delta, respectively.
    """
    length = ts.iloc[:, -1:].size
    end = (length * increment) + start
    if "Datetime" not in ts:
        ts.insert(0, "Datetime",
                  [datetime(2010, 1, 1, hour=(x // 3600), minute=(x // 60 % 60), second=(x % 60)) for x in
                   range(start, end, increment)])
    return ts


def difference(ts):
    """
    Produces a time series whose magnitudes are the differences between
    consecutive elements in the original time series.
    """
    ts.iloc[:, -1:] = ts.iloc[:, -1:].diff()
    return ts


def scaling(ts):
    """
    Produces a time series whose magnitudes are scaled so that the resulting
    magnitudes range in the interval [0,1].
    """
    floor = float(ts.iloc[:, -1:].min())
    ceiling = float(ts.iloc[:, -1:].max())
    diff = ceiling - floor  # range
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: (x - floor) / diff)
    return ts


def standardize(ts):
    """
    Produces a time series whose mean is 0 and variance is 1.
    """
    mu = float(ts.iloc[:, -1:].mean())
    sigma = float(ts.iloc[:, -1:].std())
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: (x - mu) / sigma)
    return ts


def logarithm(ts):
    """
    Produces a time series whose elements are the logarithm of the original
    elements.
    """
    ts.iloc[:, -1:] = log10(ts.iloc[:, -1:])
    return ts


def cubic_root(ts):
    """
    Produces a time series whose elements are the original elements’ cubic root
    """
    ts.iloc[:, -1:] = ts.iloc[:, -1:].apply(lambda x: x ** (1 / 3))
    return ts


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

    train_df.reset_index(drop=True, inplace=True)
    valid_df.reset_index(drop=True, inplace=True)
    test_df.reset_index(drop=True, inplace=True)

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
    output_array = []
    for i in range(mo + 1):
        if i == 0:
            continue
        output_array.append(i * to + tail)

    input_matrix = []
    output_matrix = []
    if mo == 1:
        while output_array[-1] < x:
            i_frames = []
            for i in input_array:
                i_frames.append(df.iloc[i, 1])
            input_matrix.append(i_frames)
            output_matrix.append(df.iloc[output_array[0], 1])
            input_array = [x + 1 for x in input_array]
            output_array = [x + 1 for x in output_array]
    else:
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

    return input_matrix, output_matrix


def ts2dbb(input_filename, perc_training, perc_valid, perc_test, input_index,
           output_index, output_file_name):
    '''
    this function combines reading a file, splitting the
    data, converting to database, and producing the training databases.
    '''
    pass


def forecast_predict(n, model, df, mi, ti, mo, to):
    test_matrix_x, test_matrix_y = design_matrix(df, mi, ti, mo, to)
    row, col = df.shape
    time = df.iloc[row - 1, 0]
    time_delta = df.iloc[1, 0] - df.iloc[0, 0]

    # if user is doing one step ahead forecasting
    time_array = [time]
    forecast_array = [df.iloc[row - 1][col - 1]]
    input_array = test_matrix_x[-1]
    if mo == 1:
        for i in range(n):
            prediction = model.predict([input_array])[0]
            forecast_array.append(prediction)
            input_array.append(prediction)
            input_array.pop(0)
            time = time + time_delta
            time_array.append(time)
    # if user is doing multiple step simultaneous
    else:
        prediction = model.predict([input_array])[0]
        for i in range(mo):
            time = time + time_delta
            time_array.append(time)
            forecast_array.append(prediction[i])

    column_names = df.columns.values.tolist()
    forecast_dataframe = pd.DataFrame(list(zip(time_array, forecast_array)), columns=[column_names[0], column_names[1]])

    return forecast_array, forecast_dataframe


def forecast_test(n, model, test_df, mi, ti, mo, to):
    test_matrix_x, test_matrix_y = design_matrix(test_df, mi, ti, mo, to)
    matrix_len = len(test_matrix_x)
    forecast_array = []
    row, col = test_df.shape
    #print(row, col)
    x = mi * ti + to
    time_array = []
    n = min(n, row - x - 1)
    # if user is doing one step ahead forecasting
    if mo == 1:
        test_array = []
        for i in range(n):
            array = test_matrix_x[i]
            prediction = model.predict([array])[0]
            forecast_array.append(prediction)
            time = test_df.iloc[x, 0]
            time_array.append(time)
            x += to
            # replace old matrix values with newly forecasted values
            for j in range(mi):
                array_num = i + to + (ti * j)
                if array_num < matrix_len - 1:
                    if j == 0:
                        test_array.append(test_matrix_x[array_num][mi - j - 1])
                    test_matrix_x[array_num][mi - j - 1] = prediction
    # if user is doing multiple step simultaneous
    else:
        test_array = test_matrix_y[0]
        array = test_matrix_x[0]
        prediction = model.predict([array])[0]
        forecast_array = prediction
        for i in range(mo):
            time = test_df.iloc[x, 0]
            time_array.append(time)
            x += to

    column_names = test_df.columns.values.tolist()
    forecast_dataframe = pd.DataFrame(list(zip(time_array, forecast_array)), columns=[column_names[0], column_names[1]])

    return test_array, forecast_array, forecast_dataframe
