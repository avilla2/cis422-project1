import pandas as pd
import matplotlib.pyplot as plt

def plot(ts):
    """
    :param ts: Time series data
    :return: No return(?)
    Displays data according to their time indices
    """
    #figure out a way to read ts data
    #dplot = pd.read_csv(ts.data)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    #plt.plot(dplot)


def histogram(ts):
    """
    :param ts: Time series data
    :return: No return(?)
    Computes and Draws histogram of given TS
    Plots histogram vertically and side to side
    with a plot of the TS
    """
    pass

def box_plot(ts):
    """
    :param ts: Time series data
    :return: no return(?)
    Produces a Box and Whiskers plot of TS
    Prints 5-number summary of the data
    """
    pass

def normality_test(ts):
    """
    :param ts: Time series data
    :return: TS(?)
    Performs a hypothesis test about normality on the
    time series data distribution
    matplotlib qqplot
    """
    pass

def mse(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MSE error of two TS
    """
    pass

def mape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y TS forecast data
    :return: Error
    Computes the MAPE error of two time series
    """
    pass

def smape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y forecast data
    :return: error
    Computes the SMAPE error of two time series
    """
    pass



