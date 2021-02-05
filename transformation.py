import preprocessing
import modeling
import visualization
import copy
import operations
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
			print("Invalid Data")
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
				operations.check_operator(add_node)
				self.current_node = add_node 
				return True
		else:
			print("Invalid Node")
			return False

	def remove_operator(self, node):
		if self.root:
			nd = search.find_by_attr(self.root, node)
			nd.parent = None
			return True
		else:
			print("Invalid Node")
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
			print("Invalid Node")
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
			print("Invalid Node")
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
			print("Invalid Node")
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
			print("Invalid Node")
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
			return True
		else:
			print("No leaves exist")
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
					pl.data = operations.pick_operator(pl)
			return pl.data
		else:
			print("No leaf exists")
			return False
