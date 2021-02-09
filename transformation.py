import preprocessing
import modeling
import visualization
import copy
import operations
import pickle
from anytree import Node, RenderTree, search
'''
Credit by Jay Shin
anytree is a great tree library.
anytree creates root and nodes for us
'''

class tf_tree(object): 
	'''
	This is TransFormation tree
	preDicTable creates tree with this
	''' 
	def __init__(self):
		'''
		Initializing the tree. It creates empty tree.
		node_count is for unique naming
		'''
		self.root = None
		self.current_node = None
		self.node_count = 0
		self.results = {}

	def print_tree(self, node):
		'''
		using anytree function RenderTree, display tree with node number and operator
		'''
		nd = search.find_by_attr(self.root, node)
		if nd:
			for pre, fill, n in RenderTree(nd):
				print("%s%s %s" % (pre, n.name, n.operator))

	def create_tree(self, ts): 
		'''
		Set the begining of tree. Root is always 1.
		takes time series data address and read from prerocessing
		'''
		if ts:
			self.node_count += 1
			self.root = Node(self.node_count, data=preprocessing.read(ts), operator="Time Series Data")
			self.current_node = self.root
			return True
		else:
			print("Invalid Data")
			return False

	def add_operator(self, node, op):
		'''
		Add operators to the transformation tree
		checking type compatibility of output/input of operators. 
		'''
		if self.root:
			nd = search.find_by_attr(self.root, node)
			if nd and op:
				# index is for the numbering purpose
				# anytree doesn't allow nodes with same name
				self.node_count += 1
				add_node = Node(self.node_count, parent=nd, operator=op)
				operations.check_operator(add_node)
				self.current_node = add_node
				return True
		else:
			print("Invalid Node")
			return False

	def remove_operator(self, node):
		'''
		Remove input node. Node and its related data will be removed(children)
		'''
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
				n
				nd.children = nd.children
				return True
		else:
			print("Invalid Node")
			return False

	def replicate_subtree(self, node):
		'''
		Find subtree of input node.
		It returns copied subtree
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
		Find path of input node.
		It returns copied path
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
		Add input subtree of path to to_node. 
		to_node add one child
		'''
		if node and to_node:
			tnd = search.find_by_attr(self.root, to_node)
			node.parent = tnd
			return True
		else:
			print("Invalid Node")
			return False

	def save_load_tree(self, method, name): 
		'''
		Load/Save whole tree
		pickle module assists this function
		'''
		nm = name + ".pickle"
		if method.lower() == "save":
			f = open(nm, "wb")
			dt = copy.deepcopy(self.root)
			dt.data = self.root.data
			pickle.dump(dt, f)
			f.close()
		elif method.lower() == "load":
			f = open(nm, "rb")
			self.root = pickle.load(f)
			f.close()
		else:
			print("Invalid Input")
			return False

	def save_load_pipeline(self, method, node):
		'''
		Load/Save a pipeline 
		pickle module assists this function
		'''
		nm = str(node) + ".pickle"
		if method.lower() == "save":
			nd = search.find_by_attr(self.root, node)
			if nd:
				f = open(nm, "wb")
				dts = copy.deepcopy(nd.path)
				dts[0].data = self.root.data
				pickle.dump(dts, f)
				f.close()
		elif method.lower() == "load":
			f = open(nm, "rb")
			self.root = pickle.load(f)[0]
			f.close()
		else:
			print("Invalid Input")
			return False

	def exec_tree(self): 
		'''
		Execute whole tree.
		It goes each leaf and run assigened operator from its path
		This saves result data in its result dictionary
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
		It goes down to input leaf and run assigened operator from its path
		This saves result data in its result dictionary
		'''
		if node:
			nd = search.find_by_attr(self.root, node)
			for pl in nd.path:
				if not pl.is_root and pl.operator:
					pl.data = copy.deepcopy(pl.parent.data)
					pl.data = operations.pick_operator(pl)
			return pl.data
		else:
			print("No leaf exists")
			return False
