import preprocessing
import modeling
import visualization
import copy
from anytree import Node, RenderTree, search
'''
Credit by Jay Shin
anytree is a great tree library. I believe 
using this library will save us a lot of time
'''

class tf_tree(object): 
	'''
	This is TransFormation tree
	NodeMixin is a feature in anytree library
	NodeMixin will add node feature to our functions
	''' 
	def __init__(self):
		self.root = None
		self.current_node = None
		self.node_count = 0
		self.results = {}
        
	def print_tree(self, node):
		'''
		using anytree function RenderTree, display tree with node as root
		'''
		print(RenderTree(node))

	def create_tree(self, ts): 
		'''
		Create a new tree : initialize tree
		'''
		#Node will make node automatically from anytree
		if ts:
			self.node_count += 1
			self.root = Node(self.node_count, data=preprocessing.read(ts))
			self.current_node = self.root
			return True
		else:
			return False
        
	def add_operator(self, node, op): 
		'''
		Add operators to the transformation tree
		checking type compatibility of output/input of operators. 
		No operateTree means it's Default condition
		
		We need to get function from user which will be choices
		Easist way to handle cornercases
		'''
		if self.root:
			nd = search.find_by_attr(self.root, node)
			if nd and op:
	            #index is for the numbering purpose
	            #anytree doesn't allow nodes with same name
				self.node_count += 1
				add_node = Node(self.node_count, parent=nd, operator=op)
				self.current_node = add_node 
				return True
		else:
			return False

	def remove_operator(self, node):
		if self.root:
			nd = search.find_by_attr(self.root, node)
			nd.parent = None
		else:
			return False


	def replace_process(self, node, op): 
		'''
	    This function is to fix node's operator to new one
		from preprocesesing
		'''
		if self.root:
			nd = search.find_by_attr(self.root, node)
			if op and nd:
				nd.operator = op
				nd.children = nd.children
				return True
		else:
			return False
	        
	def replicate_subtree(self, node):
		'''
		Copy and paste the one node, no following nodes : path below
		using deepcopy mathod, copy data but separate from original
		and return the copied subtree
		'''
		if node:
			nd = search.find_by_attr(self.root, node)
			copy_node = copy.deepcopy(nd)
			self.node_count += 1
			copy_node.name = self.node_count
			for descendant in copy_node.descendants:
				self.node_count += 1
				descendant.name = self.node_count
			copy_node.parent = None
			return copy_node
		else:
			return False


	def replicate_tree_path(self, node):
		'''
		Different 
		Copy and paste the path following the one node : path above
		using deepcopy mathod, copy data but separate from original
		and return the copied path
		'''
		if node:
			nd = search.find_by_attr(self.root, node)
			copy_nodes = copy.deepcopy(nd.path)
			for cp in copy_nodes:
				#because it is path, [0] is always root
				self.node_count += 1
				cp.name = self.node_count
			copy_nodes[0].parent = None
			return copy_nodes
		else:
			return False

	def add_subtree(self, node, to_node):
		'''
		Add a subtree to a node. 
		Add path to input node children list
		Make this node a sibling of current node
		'''
		if node and to_node:
			tnd = search.find_by_attr(self.root, to_node)
			node.parent = tnd
			return True
		else:
			return False

	def load_save_tree(self): 
		'''
		Load/Save whole tree. ###Load and save where?

		If we know leaves, we can run tree using path of leaf
		but im not sure, if this is right way to do
		'''
		pass

	def load_save_pipeline(self, node):
		'''
		Load/Save a pipeline 
		'''
		pass

	def exec_tree(self): 
		'''
		Execute whole tree.
		If tree is in default, use default for ML
		if tree has pipeline, wait until they are all done
		
		Contains modeling and forecasting functions
		then result present
		'''
		if self.root.leaves:
			for leaf in self.root.leaves:
				self.results[int(leaf.name)] = self.exec_pipeline(leaf.name)
			return self.results
		else:
			return False

	def exec_pipeline(self, node): 
		'''
		Execute a pipeline.
		If pipeline exists, run all

		Contains modeling and forecasting functions
		return all the results
		'''
		if node:
			nd = search.find_by_attr(self.root, node)
			for pl in nd.path:
				if not pl.is_root and (pl.operator):
					pl.data = pl.parent.data
					pl.data = self.pick_operator(pl)
					print("operator : " , pl.operator)
					print("data : " , pl.data)
			return pl.data
		else:
			return False

	def pick_operator(self, node):
		new_data = {}
		data = node.data
		op = node.operator
		if op == 'denoise': return preprocessing.denoise(data)
		elif op == 'impute_missing_data': return preprocessing.impute_missing_data(data)
		elif op == 'impute_outliers': return preprocessing.impute_outliers(data)
		elif op == 'longest_continous_run': return preprocessing.longest_continuous_run(data)
		elif op == 'clip': 
			start = input('Start Date : ')
			final = input('Final Date : ')
			return preprocessing.clip(data, start, final)
		elif op == 'assign_time': 
			start = input('Start Date : ')
			inc = input('Increment : ')
			return preprocessing.assign_time(data, start, inc)
		elif op == 'difference': return preprocessing.difference(data)
		elif op == 'scaling': return preprocessing.scaling(data)
		elif op == 'standardize': return preprocessing.standardize(data)
		elif op == 'logarithm': return preprocessing.logarithm(data)
		elif op == 'cubic_root': return preprocessing.cubic_root(data)
		elif op == 'split_models': 
			train = float(input('Training % : '))
			valid = float(input('Valid % : '))
			test = float(input('Test % : '))
			data = preprocessing.split_data(data, train, valid, test)
			ly1, ly2, ly3 = input("Enter Layers ly1, ly2, ly3 : ").split()
			node.model = modeling.mlp_model((int(ly1),int(ly2),int(ly3)))
			return data
		elif op == 'create_train':
			node.model = node.parent.model
			dfs = node.data
			mt = list(map(int, input('Enter mi, ti, mo,to : ').split()))
			dftype = input('Enter data frame type : ')
			if dftype.lower() == 'train':
				train_x, train_y = preprocessing.design_matrix(dfs[0], mt[0], mt[1], mt[2], mt[3])
			elif dftype.lower() == 'valid':
				train_x, train_y = preprocessing.design_matrix(dfs[1], mt[0], mt[1], mt[2], mt[3])
			elif dftype.lower() == 'test':
				train_x, train_y = preprocessing.design_matrix(dfs[2], mt[0], mt[1], mt[2], mt[3])
			node.model.fit(train_x, train_y)
			return dfs, mt
		elif op == 'forecast': 
			n = int(input('Enter number of forecasts : '))
			node.model = node.parent.model
			dfs = data[0]
			mt = data[1]
			ret = preprocessing.forecast_op(n, node.model, dfs[2], mt[0], mt[1], mt[2], mt[3])
			return ret[1]
		elif op == 'ts2db': return preprocessing.ts2db(data)
		elif op == 'plot': 
			return visualization.plot(data)
		elif op == 'histogram': return visualization.histogram(data)
		elif op == 'box_plot': return visualization.box_plot(data)
		elif op == 'normality_test': return visualization.normality_test(data)
		elif op == 'mse': return visualization.mse(data)
		elif op == 'mape': return visualization.mape(data)
		elif op == 'smape': return visualization.smape(data)
		else: return False
