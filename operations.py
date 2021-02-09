import preprocessing
import modeling
import visualization
import copy
from anytree import Node

'''
Credit by Adam.C and Jay.S
Main stream of tree
This rules the tree evolution
'''

def get_data(node, op):
	'''
	only Operation module uses this function
	It simply gets data from 
	earliest apperaing input operator from input node path
	'''
	for pth in reversed(node.path):
		# if we iterate backward plot node will take processed data before last split
		if pth.operator == op:
			return pth


def check_operator(node):
	'''
	It simply checks whether operators need variables or not.
	If operator needs variables, then it will ask the user
	'''
	operators = ['denoise', 'impute_missing_data', 'impute_outliers', 'longest_continuous_run',
					'difference', 'scaling', 'standardize', 'logarithm', 'cubic_root', 'plot', 
					'histogram', 'box_plot', 'normality_test', 'mse', 'mape', 'smape']
	if node.operator.lower() in operators:
		return True
	elif node.operator.lower() not in operators:
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
			if (tvt[0]+tvt[1]+tvt[2]) != 1:
				print("Invalid Input")
				return False
			node.tvt = tvt
			layers = input("Enter layer sizes l1 l2 ... ln : ").split()
			node.ly = []
			for layer in layers:
				for l in layer:
					if l == ',':
						layer.replace(l, "")
				node.ly.append(int(layer))

		elif op == 'create_train':
			numbers = []
			numbers.append(int(input('Enter number of inputs (mi): ')))
			numbers.append(int(input('Enter number of input spacing (ti): ')))
			numbers.append(int(input('Enter number of outputs (mo): ')))
			numbers.append(int(input('Enter number of output spacing (to): ')))
			node.mt = numbers

		elif op == 'forecast': 
			node.n = int(input('Enter number of forecasts : '))

		elif op == 'test_forecast':
			node.n = int(input('Enter number of forecasts : '))
			node.pick = input('Enter base for forecasts (Valid | Test): ')

		elif op == 'ts2db': 
			pass

		else:
			print("Invalid Operator")
			return False


def pick_operator(node):
	'''
	This calls functions from different modules
	Easier to set whole rules for the program
	'''
	data = node.data
	op = node.operator
	if op == 'denoise':
		data['ts_clean'] = preprocessing.denoise(data['ts_clean'])
		return data
	elif op == 'impute_missing_data':
		data['ts_clean'] = preprocessing.impute_missing_data(data['ts_clean'])
		return data
	elif op == 'impute_outliers':
		data['ts_clean'] = preprocessing.impute_outliers(data['ts_clean'])
		return data
	elif op == 'longest_continuous_run':
		data['ts_clean'] = preprocessing.longest_continuous_run(data['ts_clean'])
		return data
	elif op == 'clip':
		data['ts_clean'] = preprocessing.clip(data['ts_clean'], node.start, node.final)
		return data
	elif op == 'assign_time':
		data['ts_clean'] = preprocessing.assign_time(data['ts_clean'], node.start, node.inc)
		return data
	elif op == 'difference':
		data['ts_clean'] = preprocessing.difference(data['ts_clean'])
		return data
	elif op == 'scaling':
		data['ts_clean'] = preprocessing.scaling(data['ts_clean'])
		return data
	elif op == 'standardize':
		data['ts_clean'] = preprocessing.standardize(data['ts_clean'])
		return data
	elif op == 'logarithm':
		data['ts_clean'] = preprocessing.logarithm(data['ts_clean'])
		return data
	elif op == 'cubic_root':
		data['ts_clean'] = preprocessing.cubic_root(data['ts_clean'])
		return data
	elif op == 'split_models':
		node.prc_data = data['ts_clean']
		train_df, valid_df, test_df = preprocessing.split_data(data['ts_clean'], node.tvt[0], node.tvt[1], node.tvt[2])
		node.model = modeling.mlp_model(node.ly)
		data['train_ts'] = train_df
		data['valid_ts'] = valid_df
		data['test_ts'] = test_df
		return data
	elif op == 'create_train':
		model = node.parent.model
		train_df = data['train_ts']
		train_x, train_y = preprocessing.design_matrix(train_df, node.mt[0], node.mt[1], node.mt[2], node.mt[3])
		model.fit(train_x, train_y)
		data['model'] = model
		return data
	elif op == 'test_forecast':
		model = data['model']
		if node.pick.lower() == 'valid':
			df = data['valid_ts']
		elif node.pick.lower() == 'test':
			df = data['test_ts']
		else:
			print("Invalid Type")
			return False
		mts = get_data(node, 'create_train')
		mts = mts.mt
		test_a, fcast_a, fcast_df = preprocessing.forecast_test(node.n, model, df, mts[0], mts[1], mts[2], mts[3])
		data['test_array'] = test_a
		data['forecast_array'] = fcast_a
		data['forecast_ts'] = fcast_df
		data['graphs'] = [df, fcast_df]
		return data
	elif op == 'forecast':
		model = data['model']
		df = data['ts_clean']
		mts = get_data(node, 'create_train')
		mts = mts.mt
		fcast_a, fcast_df = preprocessing.forecast_predict(node.n, model, df, mts[0], mts[1], mts[2], mts[3])
		data['forecast_array'] = fcast_a
		data['forecast_ts'] = fcast_df
		print(data['ts'])
		print(data['ts_clean'])

		data['graphs'] = [data['ts_clean'], fcast_df]
		return data
	# TODO get this working? It's not necessary, so might as well skip until we have everything else complete
	#elif op == 'ts2db': return preprocessing.ts2db(data)
	elif op == 'plot':
		"""
		time_series = data
		if type(data) is tuple:
			processed = get_data(node, 'split_models')
			processed = processed.prc_data
			data = [processed, data[1]]
		"""
		visualization.plot(data['graphs'])
		return data
	elif op == 'histogram':
		return visualization.histogram(data['ts'])
	elif op == 'box_plot':
		return visualization.box_plot(data['ts'])
	elif op == 'normality_test':
		return visualization.normality_test(data['ts'])
	elif op == 'mse':
		return visualization.mse(data['test_array'], data['forecast_array'])
	elif op == 'mape':
		return visualization.mape(data['test_array'], data['forecast_array'])
	elif op == 'smape':
		return visualization.smape(data['test_array'], data['forecast_array'])
