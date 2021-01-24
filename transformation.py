
import preprocesesing
import modeliing

from anytree import NodeMixin, RenderTree
'''
anytree is a great tree library. I believe 
using this library will save us a lot of time
'''

class tree_node:
	"""Tree Node"""
	def __init__(self, ts):
		self.data = ts
		self.children = []

class tf_tree(tree_node, NodeMixin): 
	'''
	This is TransFormation tree
	NodeMixin is a feature in anytree library
	NodeMixin will add node feature to our functions
	''' 

	def create_tree(self, ts, name, parent=None, children=None): 
		'''
		Create a new tree : initialize tree
		'''
		self.root = name
		self.data = preprocesesing.read(ts)
		self.parent = parent
		if children:
			self.children = children

	
	def add_operate_tree(self, ts): 
		'''
		Add operators to the transformation tree
		checking type compatibility of output/input of operators. 
		No operateTree means it's Default condition
		
		We need to get function from user which will be choices
		Easist way to handle cornercases
		'''
		if self.data:
			if self.function:
				ret = preprocesesing.function(ts)
				return 


	def replace_process(self, ts, function): 
		'''
		Replace a process step with a different operator. 
		-difference(ts)   -scaling(ts)   -standardize(ts)   -logarithm(ts)   -cubic_root(ts)
		from preprocesesing
		'''
		if function:
			

	def replicate_subTree(self):
		'''
		Copy and paste the one node, no following nodes : path above
		'''

	def replicate_treePath(self, function):
		'''
		Different 
		Copy and paste the path following the one node : entire path with diff op
		'''

	def add_subTree(self):
		'''
		Add a subtree to a node. 
		'''

	def get_readyTree : Load/Save a tree. ###Load and save where?

	def get_readyPipeline : Load/Save a pipeline. 

	def exec_tree : Execute a tree. 

	def exec_pipeline : Execute a pipeline.
