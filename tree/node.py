import preprocessing as pp
import modeling as md
import visualization as vz


class Node:
    def __init__(self, ts=None, training_x=None, training_y=None, validation_x=None, validation_y=None,
                 testing_x=None, testing_y=None, model=None, forecast=None):
        self.parent = None
        self.children = []
        self.ts = ts
        self.training_x = training_x
        self.training_y = training_y
        self.validation_x = validation_x
        self.validation_y = validation_y
        self.testing_x = testing_x
        self.testing_y = testing_y
        self.model = model
        self.forecast = forecast

    # pulls all the data from the parent node
    def __preExecute__(self):
        self.ts = self.parent.ts
        self.training_x = self.parent.training_x
        self.training_y = self.parent.training_y
        self.validation_x = self.parent.validation_x
        self.validation_y = self.parent.validation_y
        self.testing_x = self.parent.testing_x
        self.testing_y = self.parent.testing_y
        self.model = self.parent.model
        self.forecast = self.parent.forecast

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def get_child(self, i):
        return self.children[i]

    def execute(self):
        raise NotImplementedError

    def type_compatibility(self):
        raise NotImplementedError



# imports a csv from the given 'filename' as a pandas dataframe
# only works as the root of the tree. it MUST be the root of the tree
class Import(Node):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def __str__(self):
        return 'Import'

    def execute(self):
        self.ts = pp.read(self.filename)

    def type_compatibility(self):
        self.ts = True
        return True


# creates and fills a time column in the time series dataframe based on 'start' date and 'increment'
class AssignTime(Node):
    def __init__(self, start, increment):
        super().__init__()
        self.start = start
        self.increment = increment

    def __str__(self):
        return 'AssignTime'

    def execute(self):
        self.ts = pp.assign_time(self.ts, self.start, self.increment)

    def type_compatibility(self):
        self.__preExecute__()
        if self.ts:
            return True
        else:
            return False


# updates the time series dataframe to a clip of itself from 'start' date to 'final' date
class Clip(Node):
    def __init__(self, start, final):
        super().__init__()
        self.start = start
        self.final = final

    def __str__(self):
        return 'Clip'

    def execute(self):
        self.ts = pp.assign_time(self.ts, self.start, self.final)

    def type_compatibility(self):
        self.__preExecute__()
        if self.ts:
            return True
        else:
            return False


# functions: denoise, impute_missing_data, impute_outliers, longest_continuous_run,
#               difference, scaling, standardize, logarithm, cubic_root
class Preprocess(Node):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return 'Preprocess'

    def execute(self):
        self.__preExecute__()
        self.ts = self.function(self.ts)

    def type_compatibility(self):
        self.__preExecute__()
        if self.ts:
            return True
        else:
            return False


# splits the data based on the given percents: 'perc_train', 'perc_val', 'perc_test'
class Split(Node):
    def __init__(self, perc_train, perc_val, perc_test):
        super().__init__()
        self.train = perc_train
        self.val = perc_val
        self.test = perc_test

    def __str__(self):
        return 'Split'

    def execute(self):
        self.__preExecute__()
        self. training_x, self.validation_x, self.testing_x = pp.split_data(self.ts, self.train, self.val, self.test)

    def type_compatibility(self):
        self.__preExecute__()
        self.training_x = True
        self.testing_x = True
        if self.ts:
            return True
        else:
            return False


# turns the training, validation, and testing dataframes into input and output (x and y) matrices
class Matrix(Node):
    def __init__(self, mi, ti, mo, to):
        super().__init__()
        self.mi = mi
        self.ti = ti
        self.mo = mo
        self.to = to

    def __str__(self):
        return 'Matrix'

    def execute(self):
        self.__preExecute__()
        self.training_x, self.training_y = pp.design_matrix(self.training_x, self.mi, self.ti, self.mo, self.to)
        if self.validation_x: # in case split is 100% training/testing
            self.validation_x, self.validation_y = pp.design_matrix(self.validation_x, self.mi, self.ti, self.mo, self.to)
        if self.testing_x: # in case split is 100% training/validation
            self.testing_x, self.testing_y = pp.design_matrix(self.testing_x, self.mi, self.ti, self.mo, self.to)

    def type_compatibility(self):
        self.__preExecute__()
        self.training_y = True
        if self.training_x:
            return True
        else:
            return False


# creates a model
class Model(Node):
    def __init__(self, input_dimension=None, output_dimension=None, layers=None):
        super().__init__()
        if layers is None:
            layers = [16, 16, 16]
        self.input_dimension = input_dimension
        self.output_dimension = output_dimension
        self.layers = layers

    def __str__(self):
        return 'Model'

    def execute(self):
        self.__preExecute__()
        self.model = md.mlp_model(self.layers)

    def type_compatibility(self):
        self.__preExecute__()
        self.model = True
        return True


# trains the model using training matrices
class Train(Node):
    def __init__(self):
        super().__init__()  # change?

    def __str__(self):
        return 'Train'

    def execute(self):
        self.__preExecute__()
        self.model.fit(self.training_x, self.training_y)

    def type_compatibility(self):
        self.__preExecute__()
        self.validation_x = True
        if self.model:
            return True
        else:
            return False


# forecasts from user's input or from first vector of testing output matrix
class Forecast(Node):
    def __init__(self, current_state=None):
        super().__init__()
        self.current_state = current_state

    def __str__(self):
        return 'Forecast'

    def execute(self):
        self.__preExecute__()
        if self.current_state:
            self.forecast = self.model.predict([self.current_state])
        else:
            self.forecast = self.model.predict([self.testing_x[0]])

    def type_compatibility(self):
        self.__preExecute__()
        self.forecast = True
        if self.validation_x:
            return True
        else:
            return False


# functions: plot, histogram, box_plot, normality_test
class Visualize(Node):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return 'Visualize'

    def execute(self):
        self.__preExecute__()
        self.function(self.ts)

    def type_compatibility(self):
        self.__preExecute__()
        if self.ts:
            return True
        else:
            return False


# function: mse, mape, smape
class Error(Node):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def __str__(self):
        return 'Error'

    def execute(self):
        self.__preExecute__()
        self.function(self.testing_y[0], self.forecast)

    def type_compatibility(self):
        self.__preExecute__()
        if self.forecast and self.testing_x:
            return True
        else:
            return False

