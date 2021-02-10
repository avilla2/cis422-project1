"""
Usage:
mlp_model() to create a neural network
mlp.fit(x_train, y_train) or learn(mlp, x_train, y_train) to train the model
mlp.predict(x_test) or forecast(mlp, x_test) to create a forecast
"""
from sklearn.neural_network import MLPRegressor
#from statsmodels.tsa.arima.model import ARIMA


def mlp_model(layers):
    """
    mlp_model
        creates a neural network
    :param
        layers: an n-ary tuple, defines the number of nodes and the number of layers of the neural network
        the input and output nodes are defined by the training matrices
    :return
        returns a neural network object
    """
    return MLPRegressor(hidden_layer_sizes=layers)
    # solver='lbfgs'


def learn(nn, x_train, y_train):
    """
    learn
        fit the model to data matrix X and target(s) y
    :param
        nn: neural network
        X: matrix e.g. [[a1, b1],[a2,b2],...,[an, bn]]
        y: matrix e.g. [[c1, d1], [c2, d2],...,[cn, dn]] or list e.g. [c1, c2,...,cn]
    :return
        none (trains the model)
    """
    nn.fit(x_train, y_train)


def forecast(nn, x):
    """
    forecast
        predict using the multi-layer perceptron model (neural network)
    :param
        nn: neural network model
        x: array-like e.g. [a1, a2,...,an]
    :return
        list
    """
    prediction = nn.predict([x])
    return prediction[0]
