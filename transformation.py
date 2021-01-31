
import preprocessing
import modeling
#import visualization
import copy
from anytree import Node, RenderTree, search
'''
Credit by Jay Shin
anytree is a great tree library. I believe 
using this library will save us a lot of time
'''
##/Users/hyojaeshin/Desktop/CIS422/Project1/Time Series Data/1_temperature_test.csv
class tf_tree(object): 
	'''
	This is TransFormation tree
	NodeMixin is a feature in anytree library
	NodeMixin will add node feature to our functions
	''' 
	def __init__(self):
		self.root = None
		self.current_node = None
		self.leaves = None
		self.pipeline = None
		self.node_count = 0
		self.copy = False

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


	def replace_process(self, node, op): 
		'''
	    This function is to fix node's operator to new one
		from preprocesesing
		'''
		if self.root:
			nd = search.find_by_attr(self.root, node)
			if op and nd:
				nd.operator = op
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

	def get_ready_tree(self): 
		'''
		Load/Save whole tree. ###Load and save where?

		If we know leaves, we can run tree using path of leaf
		but im not sure, if this is right way to do
		'''
		self.leaves = self.root.leaves
		return self.leaves

	def get_ready_pipeline(self, node):
		'''
		Load/Save a pipeline 
		'''
		if node:
			nd = search.find_by_attr(self.root, node)
			if nd in self.leaves:
				self.pipeline = copy.deepcopy(nd.path)
				return self.pipeline
		else:
			return False

	def exec_operator(self, operator, ts):
		operation = {
			'denoise': preprocessing.denoise(ts),
			'impute_missing_date': preprocessing.impute_missing_date(ts),
			'impute_outliers': preprocessing.impute_outliers(ts),
			'logarithm': preprocessing.logarithm(ts),
			'plot': preprocessing.impute_outliers(ts),
		}
		return operation.get(operator, 'Invalid Index'.format(operator))
		pass

	def exec_tree(self): 
		'''
		Execute whole tree.
		If tree is in default, use default for ML
		if tree has pipeline, wait until they are all done
		
		Contains modeling and forecasting functions
		then result present
		'''
		if self.leaves:
			transformer = self.root.data.copy()
			for leaf in self.leaves:
				for pl in leaf.path:
					if pl != self.root:
						if pl.operator:
							print(pl.operator, " is operator \n")
							print(transformer, " is data \n")
							self.exec_operator(pl.operator,transformer)
				print(transformer)
			return True
		else:
			return False

	def exec_pipeline(self): 
		'''
		Execute a pipeline.
		If pipeline exists, run all

		Contains modeling and forecasting functions
		return all the results
		'''
		if self.pipeline:
			transformer = self.root.data.copy()
			for pl in self.pipeline:
				if pl != self.root:
					if pl.operator:
						print(pl.operator, " is operator \n")
						print(transformer, " is data \n")
						self.exec_operator(pl.operator, transformer)
			return transformer
		else:
			return False
