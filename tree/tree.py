class Tree:
    def __init__(self, name, root): #TODO get filename instead of root. create root node from filename
        self.name = name
        self.root = root

    def __createNodeList__(self, leaf):
        node = leaf
        node_list = [node]
        while node != self.root:
            node = node.parent
            node_list.append(node)
        node_list.reverse()
        return node_list

    def __executeTreeHelper__(self, node):
        node.execute()
        for n in node.children:
            self.__executeTreeHelper__(n)

    # ii. Add operator to the transformation tree
    # need to check for type compatibility
    def add_node(self, node, parent):
        node.set_parent(parent)
        if node.type_compatibility():
            parent.add_child(node)
            return True
        else:
            return False

    # iii. Replace a process step with a different operator
    # need to check for type compatibility
    def replace_node(self, old_node, new_node):
        for child in old_node.children:
            child.parent = new_node
            new_node.children.append(child)
        new_node.parent = old_node.parent

    # iv. Replicate a subtree
    def replicate_subtree(self, node, name):
        return Tree(name, node)

    # v. Replicate a tree path
    # not sure what this is supposed to do. it currently returns a list of nodes from root to leaf
    # it's the exact same function as __createNodeList__
    def replicate_tree_path(self, leaf):
        node = leaf
        node_list = [node]
        while node != self.root:
            node = node.parent
            node_list.append(node)
        node_list.reverse()
        return node_list

    # vi. Add a subtree to a node
    def add_subtree_to_node(self, subtree, node):
        node.children.append(subtree.root)

    # ix. Execute a tree
    def execute_tree(self):
        self.__executeTreeHelper__(self.root)

    # x. Execute a pipeline
    def execute_pipeline(self, leaf):
        node_list = self.__createNodeList__(leaf)
        for n in node_list:
            n.execute()

    # this would probably be a useful function
    def print_tree(self):
        raise NotImplementedError


# this class is for saving/loading/managing trees
# note: pipelines are just trees where every node only has 1 child
class Forest:
    def __init__(self):
        self.trees = {}  # tree dictionary, not sure if necessary
        self.pipelines = {}  # pipeline dictionary, not sure if necessary

    def create_tree(self, name, node):
        tree = Tree(name, node)
        self.trees[name] = tree
        return tree

    def save_tree(self, tree):
        raise NotImplementedError

    def load_tree(self, name):
        raise NotImplementedError

    def save_pipeline(self, name, pipeline):
        raise NotImplementedError

    def load_pipeline(self, name):
        raise NotImplementedError
