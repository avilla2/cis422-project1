<<<<<<< HEAD
=======

>>>>>>> d3fc0ce1868d17cd85b60ac1057713b8b1f5d5f0
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def plot(ts):
    """
    :param ts: Time series data
    :return: No return(?)
    Displays data according to their time indices
    """
    new_df = ts.set_index('Datetime')
    new_df.plot()
    plt.show()


def histogram(ts):
    """
    :param ts: Time series data
    :return: No return(?)
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
    :return: no return(?)
    Produces a Box and Whiskers plot of TS
    Prints 5-number summary of the data
    """
    new_df = ts.set_index("DateTime")
    new_df.boxplot()
    plt.show()


def normality_test(ts):
    """
    :param ts: Time series data
    :return: TS(?)
    Performs a hypothesis test about normality on the
    time series data distribution
    matplotlib qqplot
    """
    return stats.shapiro(ts)


def mse(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MSE error of two TS
    """
    ax = None
    return (np.square(y_test - y_forecast)).mean(axix=ax)


def mape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MAPE error of two time series
    """
    y_test, y_forecast = np.array(y_test), np.array(y_forecast)
    return np.mean(np.abs((y_test - y_forecast) / y_test)) * 100


def smape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y forecast data
    :return: error
    Computes the SMAPE error of two time series
    """
    return 1/len(y_test) * np.sum(2 * np.abs(y_forecast - y_test) / (np.abs(y_test) + np.abs(y_forecast)) * 100)

