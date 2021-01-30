<<<<<<< HEAD
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
    y_test, y_forecast = np.array(y_test), np.array(y_forecast)
    return np.mean(np.abs((y_test - y_forecast) / y_test)) * 100

def smape(y_test, y_forecast):
    """
    :param y_test: Y TS data
    :param y_forecast: Y forecast data
    :return: error
    Computes the SMAPE error of two time series
    """
    pass


=======
from matplotlib import pyplot as plt


def plot(ts):
    new_df = ts.set_index('Datetime')
    new_df.plot()
    plt.show()


def histogram(ts):
    raise NotImplementedError


def box_plot(ts):
    raise NotImplementedError


def normality_test(ts):
    raise NotImplementedError


def mse(y_test, t_forecast):
    raise NotImplementedError


def mape(y_test, t_forecast):
    raise NotImplementedError


def smape(y_test, t_forecast):
    raise NotImplementedError
>>>>>>> 02980b64c9b1fdcee461d4b25639ced48808b233

