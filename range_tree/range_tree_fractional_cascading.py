DIMENSIONS = 3


class Node:
	def __init__(self, coords, data=None, left=None, right=None, next_dimension=None):
		self.coords = coords
		self.data = data
		self.left = left
		self.right = right
		self.next_dimension = next_dimension


def findClosest(node_coords, nodes_list, dimension):
	if len(nodes_list) == 0:
		return -1
	
	i = 0
	while i < len(nodes_list) and node_coords[dimension] > nodes_list[i].coords[dimension]:
		i = i + 1
	
	return i if i < len(nodes_list) else -1



def create_tree(my_list, dimension=0):

	if len(my_list) == 0 or dimension >= DIMENSIONS:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = create_tree(my_list[:mid], dimension)
	root.right, right_list = create_tree(my_list[mid+1:], dimension)

	merged_list = []
	if dimension + 2 == DIMENSIONS:	# last - 1 dimension
		merged_list = merge_and_set(root, left_list, right_list, dimension + 1)
		root.next_dimension = merged_list
	elif dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		merged_list = merge(root, left_list, right_list, dimension + 1)
		root.next_dimension, _ = create_tree(merged_list, dimension + 1)
	
	return root, merged_list
	


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




def merge_and_set(root, left_list, right_list, dimension=0):
	if dimension >= DIMENSIONS:
		return []

	final_list = []

	left_index = 0
	right_index = 0

	while left_index < len(left_list) and right_index < len(right_list):
		if left_list[left_index].coords[dimension] < right_list[right_index].coords[dimension]:
			new_node = Node(left_list[left_index].coords, left_list[left_index].data)
			new_node.left = left_index
			new_node.right = right_index
			final_list.append(new_node)
			left_index = left_index + 1
		else:
			new_node = Node(right_list[right_index].coords, right_list[right_index].data)
			new_node.left = left_index
			new_node.right = right_index
			final_list.append(new_node)
			right_index = right_index + 1

	while left_index < len(left_list):
		new_node = Node(left_list[left_index].coords, left_list[left_index].data)
		new_node.left = left_index
		new_node.right = -1
		final_list.append(new_node)
		left_index = left_index + 1

	while right_index < len(right_list):
		new_node = Node(right_list[right_index].coords, right_list[right_index].data)
		new_node.left = -1
		new_node.right = right_index
		final_list.append(new_node)
		right_index = right_index + 1

	if root is None:
		return final_list

	new_root = Node(root.coords, root.data)
	new_root.left = findClosest(new_root.coords, left_list, dimension)
	new_root.right = findClosest(new_root.coords, right_list, dimension)

	for i in range(0, len(final_list)):
		if root.coords[dimension] < final_list[i].coords[dimension]:
			# case middle
			return final_list[: i] + [new_root] + final_list[i: ]
	
	# case last
	return final_list + [new_root]



def insert(root, node, dimension=0):
	if root is None:
		if dimension + 2 == DIMENSIONS:
			node.next_dimension = [Node(node.coords, node.data, -1, -1)]
		else:
			node.next_dimension = [Node(node.coords, node.data)]
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
		
		if dimension + 2 == DIMENSIONS:
			# find correct place for new node in the list
			place = findClosest(node.coords, root.next_dimension, dimension + 1)
			new_node = Node(node.coords, node.data, -1, -1)
			# inserting
			if place == -1:
				root.next_dimension.append(new_node)
			else:
				if root.left:
					new_node.left = findClosest(new_node.coords, root.left.next_dimension, dimension + 1)
				if root.right:
					new_node.right = findClosest(new_node.coords, root.right.next_dimension, dimension + 1)
				root.next_dimension = root.next_dimension[: place] + [new_node] + root.next_dimension[place: ]
				for i in range(place+1, len(root.next_dimension)):
					if root.next_dimension[i].left != -1:
						root.next_dimension[i].left += 1
	else:
		root.right = insert(root.right, node, dimension)

		if dimension + 2 == DIMENSIONS:
			# find correct place for new node in the list
			place = findClosest(node.coords, root.next_dimension, dimension + 1)
			new_node = Node(node.coords, node.data, -1, -1)
			# inserting
			if place == -1:
				root.next_dimension.append(new_node)
			else:
				if root.left:
					new_node.left = findClosest(new_node.coords, root.left.next_dimension, dimension + 1)
				if root.right:
					new_node.right = findClosest(new_node.coords, root.right.next_dimension, dimension + 1)
				root.next_dimension = root.next_dimension[: place] + [new_node] + root.next_dimension[place: ]
				for i in range(place+1, len(root.next_dimension)):
					if root.next_dimension[i].right != -1:
						root.next_dimension[i].right += 1

	if dimension + 2 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		root.next_dimension = insert(root.next_dimension, node, dimension + 1)

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

		if dimension + 2 == DIMENSIONS:
			# find correct place for new node in the list
			place = findClosest(delete_coords, root.next_dimension, dimension + 1)
			# inserting
			if place != -1:
				root.next_dimension = root.next_dimension[: place] + root.next_dimension[place + 1: ]
				for i in range(place, len(root.next_dimension)):
					if root.next_dimension[i].left != -1:
						root.next_dimension[i].left -= 1

	elif delete_coords[dimension] > root.coords[dimension]: # if given node bigger than root value go to the right sub-tree
		root.right = delete(root.right, delete_coords, dimension)

		if dimension + 2 == DIMENSIONS:
			# find correct place for new node in the list
			place = findClosest(delete_coords, root.next_dimension, dimension + 1)
			# inserting
			if place != -1:
				root.next_dimension = root.next_dimension[: place] + root.next_dimension[place + 1: ]
				for i in range(place, len(root.next_dimension)):
					if root.next_dimension[i].right != -1:
						root.next_dimension[i].right -= 1

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


	# if dimension + 2 == DIMENSIONS:

	# 	for node in root.next_dimension:
	# 		if node.coords == delete_coords:
	# 			root.next_dimension.remove(node)
		
	# 	for node_y in root.next_dimension:
	# 		if root.left:
	# 			node_y.left = findClosest(node_y.coords, root.left.next_dimension, dimension+1)
	# 		if root.right:
	# 			node_y.right = findClosest(node_y.coords, root.right.next_dimension, dimension+1)
		
	if dimension + 2 < DIMENSIONS:  # y = 1 DIMENSIONS = 2
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

	split_node = find_split_node(root, range_coords, dimension)

	if split_node is None:
		return []

	nodes_list = []
	if is_in_range(split_node.coords, range_coords):
		nodes_list.append(split_node)

	# last-1 dimension
	if dimension + 2 == DIMENSIONS:
		if DIMENSIONS == 2:
			index = findClosest([0, range_coords[DIMENSIONS - 1][0]], split_node.next_dimension, dimension + 1)
		if DIMENSIONS == 3:
			index = findClosest([0, 0, range_coords[DIMENSIONS - 1][0]], split_node.next_dimension, dimension + 1)

		if index == -1:
			return nodes_list
		
		return range_search1(split_node, index, range_coords, dimension) + nodes_list

	# d-1 dimensions
	elif dimension + 1 < DIMENSIONS:

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



# index shows where to start in node.next_dimension
def range_search1(split_node, split_index, range_coords, dimension):

	nodes_list = []


	index_left = split_node.next_dimension[split_index].left
	index_right = split_node.next_dimension[split_index].right

	left_child = split_node.left
	right_child = split_node.right
	

	while left_child and index_left >= 0:
		if is_in_range(left_child.coords, range_coords):
			nodes_list.append(left_child)	
		if range_coords[dimension][0] <= left_child.coords[dimension]:
			# 1DRangeSearch
			if left_child.right:
				for i in range(left_child.next_dimension[index_left].right, len(left_child.right.next_dimension)):
					if is_in_range(left_child.right.next_dimension[i].coords, range_coords):
						nodes_list.append(left_child.right.next_dimension[i])
			
			index_left = left_child.next_dimension[index_left].left
			left_child = left_child.left
		else:
			index_left = left_child.next_dimension[index_left].right
			left_child = left_child.right
	
	
	while right_child and index_right >= 0:
		if is_in_range(right_child.coords, range_coords):
			nodes_list.append(right_child)
		if right_child.coords[dimension] <= range_coords[dimension][1]:
			# 1DRangeSearch
			if right_child.left:
				for i in range(right_child.next_dimension[index_right].left, len(right_child.left.next_dimension)):
					if is_in_range(right_child.left.next_dimension[i].coords, range_coords):
						nodes_list.append(right_child.left.next_dimension[i])

			if right_child.coords[dimension] == range_coords[dimension][1]:
				break
			
			index_right = right_child.next_dimension[index_right].right
			right_child = right_child.right	# continue same dimension

		else:
			index_right = right_child.next_dimension[index_right].left
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
