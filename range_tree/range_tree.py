DIMENSIONS = 2


class Node:
	def __init__(self, coords, data=None, left=None, right=None, bst=None):
		self.coords = coords
		self.data = data
		self.left = left
		self.right = right
		self.next_dimension = bst


# returns the tree root (type Node) and a list (used for next dimension trees)
def create_tree(my_list, dimension=0):

	if len(my_list) == 0 or dimension >= DIMENSIONS:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = create_tree(my_list[:mid], dimension)
	root.right, right_list = create_tree(my_list[mid+1:], dimension)

	merged_list = []
	if dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		merged_list = merge(root, left_list, right_list, dimension + 1)

	root.next_dimension, _ = create_tree(merged_list, dimension + 1)

	return root, merged_list


# arguments: root and two sorted lists
# returns one sorted list
def merge(root, left_list, right_list, dimension=0):
	if dimension >= DIMENSIONS:
		return []

	final_list = []

	left_index = 0
	right_index = 0

	while left_index < len(left_list) and right_index < len(right_list):
		if left_list[left_index].coords[dimension] < right_list[right_index].coords[dimension]:
			final_list.append(Node(left_list[left_index].coords, left_list[left_index].data))
			left_index = left_index + 1
		else:
			final_list.append(Node(right_list[right_index].coords, right_list[right_index].data))
			right_index = right_index + 1

	while left_index < len(left_list):
		final_list.append(Node(left_list[left_index].coords, left_list[left_index].data))
		left_index = left_index + 1

	while right_index < len(right_list):
		final_list.append(Node(right_list[right_index].coords, right_list[right_index].data))
		right_index = right_index + 1

	if root is None:
		return final_list

	for i in range(0, len(final_list)):
		if root.coords[dimension] < final_list[i].coords[dimension]:
			# case middle
			return final_list[: i] + [Node(root.coords, root.data)] + final_list[i: ]
	
	# case last
	return final_list + [Node(root.coords, root.data)]


# returns the new tree root (type Node)
def insert(root, node, dimension=0):
	if root is None:
		node.next_dimension = Node(node.coords, node.data)
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)

	if dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		root.next_dimension = insert(root.next_dimension, Node(node.coords, node.data), dimension + 1)

	return root


# returns type Node
def leftmost_node(node):
    while node.left is not None:
        node = node.left
    return node


# returns the new tree root (type Node)
def delete(root, delete_coords, dimension=0):
	if root is None:
		return None

	if delete_coords[dimension] < root.coords[dimension]:  # if given node smaller than root value go to the left sub-tree
		root.left = delete(root.left, delete_coords, dimension)
	elif delete_coords[dimension] > root.coords[dimension]: # if given node bigger than root value go to the right sub-tree
		root.right = delete(root.right, delete_coords, dimension)
	else: # when the coordinate of THIS dimension is equal
		if root.coords == delete_coords:
			if root.left is None and root.right is None: # no children
				root = None
				return None
			if root.left is None or root.right is None: # 1 child
				temp = root.right if root.right else root.left
				root = None
				return temp # replace root with avaialable child
			else: # 2 children
				temp = leftmost_node(root.right)  # find the leftmost node of the right subtree
				root.coords = temp.coords
				root.data = temp.data
				root.right = delete(root.right, temp.coords, dimension)

		# for dublicates
		root.left = delete(root.left, delete_coords, dimension)
	
	if dimension + 1 < DIMENSIONS:  # y = 1 DIMENSIONS = 2
		root.next_dimension = delete(root.next_dimension, delete_coords, dimension + 1)

	return root


# returns a list of Nodes which have the exact coordinates
def search(root, coords, dimension=0):
	if root is None:
		return []

	if coords[dimension] > root.coords[dimension]:
		return search(root.right, coords, dimension)
	elif coords[dimension] < root.coords[dimension]:
		return search(root.left, coords, dimension)
	else:
		nodes_list = []
		if root.coords == coords:
			nodes_list.append(root)
		return nodes_list + search(root.left, coords, dimension) # also check left child for dublicates


# returns the Node where the split takes place
# range_coords[dimension][0] - left
# range_coords[dimension][1] - right
def find_split_node(root, range_coords, dimension=0):
	if root:
		if root.coords[dimension] < range_coords[dimension][0]:
			return find_split_node(root.right, range_coords, dimension)
		elif root.coords[dimension] > range_coords[dimension][1]:
			return find_split_node(root.left, range_coords, dimension)
		else: # range_coords[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= range_coords[dimension][1]
			# root is the split node or None
			return root
	
	return None


# checks if coords are inside a given range
def is_in_range(coords, range_coords):
	for d in range(0, DIMENSIONS):
		if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
			return False
	
	return True


# returns a list of Nodes inside a range
def range_search(root, range_coords, dimension=0):
	if root is None:
		return []


	# last dimension
	if dimension + 1 == DIMENSIONS:
		if root.coords[dimension] < range_coords[dimension][0]:
			return range_search(root.right, range_coords, dimension)
		elif root.coords[dimension] > range_coords[dimension][1]:
			return range_search(root.left, range_coords, dimension)
		else: #range_coords[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= range_coords[dimension][1]:
			nodes_list = [root] + range_search(root.right, range_coords, dimension) + range_search(root.left, range_coords, dimension)
			return nodes_list

	# d-1 dimensions
	if dimension + 1 < DIMENSIONS:
		split_node = find_split_node(root, range_coords, dimension)

		if split_node is None:
			return []

		nodes_list = []

		if is_in_range(split_node.coords, range_coords):
			nodes_list.append(split_node)


		left_child = split_node.left
		while left_child:
			if is_in_range(left_child.coords, range_coords):
				nodes_list.append(left_child)
			if range_coords[dimension][0] <= left_child.coords[dimension]:
				# 1DRangeSearch
				if left_child.right:
					nodes_list += range_search(left_child.right.next_dimension, range_coords, dimension + 1) # go to the next dimension
				left_child = left_child.left	# continue same dimension
			else:
				left_child = left_child.right	# continue same dimension


		right_child = split_node.right
		while right_child:
			if is_in_range(right_child.coords, range_coords):
				nodes_list.append(right_child)
			if right_child.coords[dimension] <= range_coords[dimension][1]:
				# 1DRangeSearch
				if right_child.left:
					nodes_list += range_search(right_child.left.next_dimension, range_coords, dimension + 1) # go to the next dimension
				right_child = right_child.right	# continue same dimension
			else:
				right_child = right_child.left	# continue same dimension

		return nodes_list


# returns the new tree root (type Node)
def update(root, coords, new_coords):
	to_change_nodes = search(root, coords)
	if len(to_change_nodes) == 0:
		print("Node NOT Found!")
		return root

	new_nodes = []
	for node in to_change_nodes:	# create new nodes
		new_nodes.append(Node(new_coords, node.data))
	for node in to_change_nodes:	# delete old nodes
		root = delete(root, coords)
	for node in new_nodes:			# insert new nodes
	  root = insert(root, node)

	return root
