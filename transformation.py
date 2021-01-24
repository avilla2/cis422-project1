
import preprocesesing
import modeliing

from anytree import NodeMixin, RenderTree
'''
anytree is a great tree library. I believe 
using this library will save us a lot of time
'''

class tf_tree(self, NodeMixin): 
	'''
	This is TransFormation tree
	NodeMixin is a feature in anytree library
	NodeMixin will add node feature to our functions
	''' 

	def create_tree(self, ts): 
		'''
		Create a new tree : initialize tree
		'''
		#Node will make node automatically
		return Node("root", data=preprocesesing.read(ts))
	
	def add_operator(preprocesesing, pnode, function, ts): 
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
		if function and ts:
			return Node("operator", parent=pnode, op=function, data=ts)


	def replace_process(self, node, function, ts): 
		'''
		Replace a process step with a different operator. 
		-difference(ts)   -scaling(ts)   -standardize(ts)   -logarithm(ts)   -cubic_root(ts)
		from preprocesesing or it has to be on add_operator
		'''
		if function and ts:
			return Node("process", parent=pnode, op=function, data=ts)

	def replicate_subtree(self):
		'''
		Copy and paste the one node, no following nodes : path below
		'''
		return path

	def replicate_tree_path(self, function):
		'''
		Different 
		Copy and paste the path following the one node : entire path with diff op

		return path list
		'''
		return path

	def add_subtree(self, node, ):
		'''
		Add a subtree to a node. 
		Add path to input node children list
		Make this node a sibling of current node
		'''

	def get_ready_tree(self, root): 
		'''
		Load/Save whole tree. ###Load and save where?
		'''
		return path

	def get_ready_pipeline(self, leaf):
		'''
		Load/Save a pipeline 
		'''
		return path 

	def exec_tree(self, path): 
		'''
		Execute whole tree.
		If tree is in default, use default for ML
		if tree has pipeline, wait until they are all done
		
		Contains modeling and forecasting functions
		then result present
		'''

	def exec_pipeline(self, path): 
		'''
		Execute a pipeline.
		If pipeline exists, run all

		Contains modeling and forecasting functions
		return all the results
		'''
