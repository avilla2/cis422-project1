
#import preprocessing
#import modeling

import copy
from anytree import Node, RenderTree
'''
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
		self.leaves = None
		self.pipeline = None

	def print_tree(self, node):
		'''
		using anytree function RenderTree, display tree with node as root
		'''
		print(RenderTree(node))

	def create_tree(self, title, ts): 
		'''
		Create a new tree : initialize tree
		'''
		#Node will make node automatically from anytree
		self.root = Node(title, data=ts)#preprocesesing.read(ts))
		self.current_node = self.root
		return self.current_node
		
	def add_operator(self, node, op): 
		'''
		Add operators to the transformation tree
		checking type compatibility of output/input of operators. 
		No operateTree means it's Default condition
		
		We need to get function from user which will be choices
		Easist way to handle cornercases

		We have to make sure that we only providing this function
		when user create_tree first (user must provide ts)

		pnode is for parent node
		'''
		if self.root:
			if op and node.data:
	            #index is for the numbering purpose
	            #anytree doesn't allow nodes with same name
				name = "operator_" + op
				self.current_node = Node(name, parent=node, operator=op, data=node.data.copy()) 
				return True
			else:
				print("Insufficient Arguments : node, operator")
		else:
			return False


	def replace_process(self, node, prc): 
		'''
	    This function is to fix node to new operator
		Replace a process step with a different operator. 
		-difference(ts)   -scaling(ts)   -standardize(ts)   -logarithm(ts)   -cubic_root(ts)
		from preprocesesing or it has to be on add_operator
		'''
		if self.root:
			if prc and node.data:
				name = "process_" + prc
				self.current_node = Node(name, parent=node, process=prc, data=node.data.copy())
				return True
			else:
				print("Insufficient Arguments : node, operator")
		else:
			return False
	        
	def replicate_subtree(self, node):
		'''
		Copy and paste the one node, no following nodes : path below
		using deepcopy mathod, copy data but separate from original
		and return the copied subtree
		'''
		copy_name = node.name + "_copy"
		copy_node = copy.deepcopy(node)
		copy_node.parent = None
		copy_node.name = copy_name
		return copy_node

	def replicate_tree_path(self, node):
		'''
		Different 
		Copy and paste the path following the one node : path above
		using deepcopy mathod, copy data but separate from original
		and return the copied path
		'''
		if node:
			copy_nodes = copy.deepcopy(node.path)
			return copy_nodes
		else:
			print("node is empty!")

	def add_subtree(self, pnode, node):
		'''
		Add a subtree to a node. 
		Add path to input node children list
		Make this node a sibling of current node
		'''
		if pnode and node:
			node.parent = pnode

	def get_ready_tree(self): 
		'''
		Load/Save whole tree. ###Load and save where?

		If we know leaves, we can run tree using path of leaf
		but im not sure, if this is right way to do
		'''
		self.leaves = self.root.leaves
		return True

	def get_ready_pipeline(self, node):
		'''
		Load/Save a pipeline 

		If user node is a leaf, we can run single pip using path of leaf
		but im not sure, if this is right way to do
		'''
		if node.name in self.leaves.name:
			self.pipline = replicate_tree_path(node)
		return self.pipline

	def exec_tree(self): 
		'''
		Execute whole tree.
		If tree is in default, use default for ML
		if tree has pipeline, wait until they are all done
		
		Contains modeling and forecasting functions
		then result present
		'''
		if self.leaves:
			for leaf in self.leaves:
				leaf_path = replicate_tree_path(leaf)
				for path in leaf_path:
					#have to execute each node now
					return True

	def exec_pipeline(self): 
		'''
		Execute a pipeline.
		If pipeline exists, run all

		Contains modeling and forecasting functions
		return all the results
		'''
		if self.current_pip:
			for node in self.current_pip:
				#have to execute each node now
				return True



