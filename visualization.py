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

