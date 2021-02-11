preDicTable

README

Team V3 - 2-10-2021 - v2.1.0

Contributors: Alex Villa, Jay Shin, Adam Christianson, Isaac Priddy, Ellie Bruhns

preDicTable
--------------
Transformation Tree program to process and study time series

Environment Requirement
------------------------
Python3, Pandas, SKLearn, and Anytree

Overview
-----------
preDicTable simply asks users to pick functionalities from the transformation module.
Because this program is still a prototype, users must enter exact numbers or variables for each function.
As long as users type the right inputs, this program will not fail.


Rules
--------
Preprocessing operators are expected to be used before modeling and visualization operators, however this is not enforced.

IMPORTANT : 
-The “split_models” operator should be used before the “create_train” operator which should be used before any forecast operators are used. 
-The “test_forecast” operator should always be used before the “test_plot” operator.

-Make sure that Time Series do not contain any NaN or Infinite Values

Getting Started
------------------
To begin, open preDicTable.py in the terminal.

preDicTable will ask the user to enter ‘0’ to create a new tree or ‘1’ to load an a previously created tree

If ‘0’ is selected, a tree will be initialized after the user enters the file path for the .csv file
NOTE: csv file header should be 1 row in length, and contain no more rows than the data itself.

Main Calls:
--------------------
Once the user has a tree, they will be given actions that can be used by entering their respective number

0: Quit - quits the program

1: Add - add an operator (see below), or a subtree

2: Remove Operator - removes an operator and all its children

3: Replace Process - replaces a node

4: Execute - executes a pipeline or a tree

5: Save/Load - save or load a tree


-Operators you can add:
-----------------------
split_models : splits the time series into 3 sets, and creates a neural network model.

create_train : creates matrices from the training set and trains the model.

test_forecast : creates a forecast with the model on the test set

forecast : creates a forecast with the model at the end of the time series

test_plot : plots the test_forecast and the test set

plot : plots the time series and the forecast

for a full list of operators, check the documentation

Example
----------
Preprocessing + Analyzing Example :
Add a Preprocessing operator to 1 node, and Add plot from analyzing operators. Executing tree results preprocessed graph.

Forecast + Analyzing Example : 
Users may add any Preprocessing operator before Forecast. Forecast functions must be in order. Add plot to check. Executing tree results forecasted graph.

Result 
---------
Users must add a visualization node to visualize the result. Because preDicTable is still a beta, its forecast may not be accurate.
  
  
  

Revision History
-----------------

Date  Author Description

2-8-2021  Jay Shin  v1.0.0 - Initializing README

2-9-2021  Jay Shin  v2.0.0 - Descript general information of program

2-10-2021 Adam C  v2.1.0 - Wrote getting started and improved the rest
