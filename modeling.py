from sklearn.neural_network import MLPRegressor
#from statsmodels.tsa.arima.model import ARIMA


"""
mlp_model 
    creates a neural network
parameters
    layers: an n-ary tuple, defines the number of nodes and the number of layers of the neural network
returns
    returns a neural network object
"""
def mlp_model(layers):
    return MLPRegressor(hidden_layer_sizes=layers, solver='lbfgs')


"""
learn
    fit the model to data matrix X and target(s) y
parameters:
    nn: neural network
    X: matrix e.g. [[a1, b1],[a2,b2],...,[an, bn]]
    y: matrix e.g. [[c1, d1], [c2, d2],...,[cn, dn]] or list e.g. [c1, c2,...,cn]
returns
    none (it simply trains the model)
"""
def learn(nn, x_train, y_train):
    nn.fit(x_train, y_train)


"""
forecast
    predict using the multi-layer perceptron model (neural network)
parameters
    nn: neural network
    x: vector e.g. [a1, a2,...,an]
returns
    the predicted values for each sublist
"""
def forecast(nn, x):
    prediction = nn.predict([x])
    return prediction[0]
