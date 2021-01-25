
#import preprocessing
#import modeling

import copy
from anytree import Node, RenderTree
'''
anytree is a great tree library. I believe 
using this library will save us a lot of time
'''

#class tf_tree(object): 
'''
This is TransFormation tree
NodeMixin is a feature in anytree library
NodeMixin will add node feature to our functions
''' 
def print_tree(node):
    '''
    using anytree function RenderTree, display tree with node as root
    '''
    print(RenderTree(node))

def create_tree(title, ts): 
	'''
	Create a new tree : initialize tree
	'''
	#Node will make node automatically from anytree
	return Node(title, operator=[], process=[], data=ts)#preprocesesing.read(ts))
	
def add_operator(node, op): 
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
	if op and node.data:
            #index is for the numbering purpose
            #anytree doesn't allow node with same name
		index = len(node.operator) + 1
		name = "operator_" + str(index) + "_" + op
		op_node = Node(name, parent=node, operator=node.operator.copy(), process=node.process, data=node.data)
		op_node.operator.append(op)
        return op_node
	else:
		print("Insufficient Arguments : node, operator")


def replace_process(node, prc): 
	'''
    This function is to fix node to new operator
	Replace a process step with a different operator. 
	-difference(ts)   -scaling(ts)   -standardize(ts)   -logarithm(ts)   -cubic_root(ts)
	from preprocesesing or it has to be on add_operator
	'''
	if prc and node.data:
		index = len(node.process) + 1
		name = "process_" + str(index) + "_" + prc
		prc_node = Node(name, parent=node, operator=node.operator, process=node.process.copy(), data=node.data)
		prc_node.process.append(prc)
        return prc_node
	else:
		print("Insufficient Arguments : node, operator")
        
def replicate_subtree(node):
	'''
	Copy and paste the one node, no following nodes : path below
	'''
	copy_name = node.name + "_copy"
	copy_node = copy.deepcopy(node)
	copy_node.name = copy_name
	return copy_node

def replicate_tree_path(node):
	'''
	Different 
	Copy and paste the path following the one node : path above
	'''
	copy_nodes = copy.deepcopy(node.path)
	return copy_nodes

def add_subtree(pnode, node):
	'''
	Add a subtree to a node. 
	Add path to input node children list
	Make this node a sibling of current node
	'''
	if pnode and node:
		node.parent = pnode

def get_ready_tree(self, root): 
	'''
	Load/Save whole tree. ###Load and save where?
	'''
	return True

def get_ready_pipeline(self, leaf):
	'''
	Load/Save a pipeline 
	'''
	return True

def exec_tree(self, path): 
	'''
	Execute whole tree.
	If tree is in default, use default for ML
	if tree has pipeline, wait until they are all done
	
	Contains modeling and forecasting functions
	then result present
	'''
	return True

def exec_pipeline(self, path): 
	'''
	Execute a pipeline.
	If pipeline exists, run all

	Contains modeling and forecasting functions
	return all the results
	'''
	return True