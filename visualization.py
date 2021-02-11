import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def plot(ts):
    """
    :param ts: Time series data
    :return: No return - plots graph
    Displays data according to their time indices
    """
    if type(ts) == list:
        ax = None
        for t in ts:
            new_df1 = t.set_index('Datetime')
            ax = new_df1.plot(ax=ax)
        plt.show()
    else:
        new_df = ts.set_index('Datetime')
        new_df.plot()
        plt.show()


def histogram(ts):
    """
    :param ts: Time series data
    :return: No return - plots graph
    Computes and Draws histogram of given TS
    Plots histogram vertically and side to side
    with a plot of the TS
    """
    new_df = ts.set_index("DateTime")
    new_df.hist()
    plt.show()


def box_plot(ts):
    """
    :param ts: Time series data
    :return: no return - plots graph
    Produces a Box and Whiskers plot of TS
    Prints 5-number summary of the data
    """
    new_df = ts.set_index("DateTime")
    new_df.boxplot()
    plt.show()


def normality_test(ts):
    """
    :param ts: Time series data
    :return: normality of data
    Performs a hypothesis test about normality on the
    time series data distribution
    """
    return stats.normaltest(ts)


def mse(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MSE error of two TS
    """
    sum = 0
    for i in range(len(y_test)):
        sum += np.square(y_test[i] - y_forecast[i])
    mse = sum/len(y_test)
    return mse


def mape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MAPE error of two time series
    """
    y_test, y_forecast = np.array(y_test), np.array(y_forecast)
    length = len(y_test)
    sum = 0
    for i in range(length):
        sum += np.abs((y_test[i] - y_forecast[i]) / y_test[i])
    return sum/length


def smape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y forecast data
    :return: error
    Computes the SMAPE error of two time series
    """

    length = len(y_test)
    sum = 0
    for i in range(length):
        sum += np.abs(y_forecast[i] - y_test[i]) / (np.abs(y_test[i]) + np.abs(y_forecast[i]))
    return 100 * sum / length

