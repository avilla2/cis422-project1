import preprocessing
import modeling
import visualization
import copy
from anytree import Node

def get_data(node, op):
	for pth in reversed(node.path):
     	#if we iterate backwoard plot node will take processed data before last split
		if pth.operator == op:
			return pth

def check_operator(node):
	operators = [ 'denoise', 'impute_missing_data', 'impute_outliers', 'longest_continous_run',
					'difference', 'scaling', 'standardize', 'logarithm', 'cubic_root', 'plot', 
					'histogram', 'box_plot', 'normality_test']
	if node.operator.lower() not in operators:
		op = node.operator

		if op == 'clip': 
			node.start = input('Start Date : ')
			node.final = input('Final Date : ')

		elif op == 'assign_time': 
			node.start = input('Start Date : ')
			node.inc = input('Increment : ')

		elif op == 'split_models':
			tvt = []
			tvt.append(float(input('Training % : ')))
			tvt.append(float(input('Valid % : ')))
			tvt.append(float(input('Test % : ')))
			node.tvt = tvt
			ly1, ly2, ly3 = input("Enter Layers ly1, ly2, ly3 : ").split()
			node.ly = [int(ly1), int(ly2), int(ly3)]

		elif op == 'create_train':
			numbers = []
			numbers.append(int(input('Enter number of inputs (mi): ')))
			numbers.append(int(input('Enter number of input spacing (ti): ')))
			numbers.append(int(input('Enter number of outputs : (mo)')))
			numbers.append(int(input('Enter number of output spacing (to): ')))
			node.mt = numbers

		elif op == 'forecast': 
			node.n = int(input('Enter number of forecasts : '))
			node.pick = input('Enter base for forecasts (Valid | Test): ')

		elif op == 'ts2db': 
			pass

		elif op == 'mse': 
			pass
		elif op == 'mape': 
			pass
		elif op == 'smape': 
			pass
	elif node.operator.lower() in operators:
		return True
	else:
		print("Invalid Operator")
		return False

def pick_operator(node):
	data = node.data
	op = node.operator
	if op == 'denoise': return preprocessing.denoise(data)
	elif op == 'impute_missing_data': return preprocessing.impute_missing_data(data)
	elif op == 'impute_outliers': return preprocessing.impute_outliers(data)
	elif op == 'longest_continous_run': return preprocessing.longest_continuous_run(data)
	elif op == 'clip': 
		return preprocessing.clip(data, node.start, node.final)
	elif op == 'assign_time': 
		return preprocessing.assign_time(data, node.start, node.inc)
	elif op == 'difference': return preprocessing.difference(data)
	elif op == 'scaling': return preprocessing.scaling(data)
	elif op == 'standardize': return preprocessing.standardize(data)
	elif op == 'logarithm': return preprocessing.logarithm(data)
	elif op == 'cubic_root': return preprocessing.cubic_root(data)
	elif op == 'split_models':
		node.prc_data = data
		data = preprocessing.split_data(data, node.tvt[0], node.tvt[1], node.tvt[2])
		node.model = modeling.mlp_model((node.ly[0], node.ly[0], node.ly[0]))
		return data
	elif op == 'create_train':
		node.model = node.parent.model
		traindf = data[0]
		train_x, train_y = preprocessing.design_matrix(traindf, node.mt[0], node.mt[1], node.mt[2], node.mt[3])
		node.model.fit(train_x, train_y)
		return data
	elif op == 'forecast': 
		node.model = node.parent.model
		df = data[0]
		if node.pick.lower() == 'valid':
			df = data[1]
		elif node.pick.lower() == 'test':
			df = data[2]
		else:
			print("Invalid Type")
			return False
		mts = get_data(node, 'create_train')
		mts = mts.mt 
		return preprocessing.forecast_op(node.n, node.model, df, mts[0], mts[1], mts[2], mts[3])
	elif op == 'ts2db': return preprocessing.ts2db(data)
	elif op == 'plot':
		if type(data) is tuple:
			processed = get_data(node, 'split_models')
			processed = processed.prc_data
			data = [processed, data[1]]
		return visualization.plot(data)
	elif op == 'histogram': return visualization.histogram(data)
	elif op == 'box_plot': return visualization.box_plot(data)
	elif op == 'normality_test': return visualization.normality_test(data)
	elif op == 'mse': return visualization.mse(data)
	elif op == 'mape': return visualization.mape(data)
	elif op == 'smape': return visualization.smape(data)