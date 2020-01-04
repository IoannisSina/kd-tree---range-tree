DIMENSIONS = 2


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


def createTree(my_list, dimension=0):

	if len(my_list) == 0 or dimension >= DIMENSIONS:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = createTree(my_list[:mid], dimension)
	root.right, right_list = createTree(my_list[mid+1:], dimension)

	merged_list = []
	if dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		merged_list = merge(root, left_list, right_list, dimension + 1)

	if dimension + 2 == DIMENSIONS:	# last - 1 dimension
		for node in merged_list:
			node.left = findClosest(node.coords, left_list, dimension + 1)
			node.right = findClosest(node.coords, right_list, dimension + 1)
			
		root.next_dimension = merged_list
	else:
		root.next_dimension, _ = createTree(merged_list, dimension + 1)
	
	return root, merged_list
	

# def createTree(my_list, dimension=0):
# 	if len(my_list) == 0 or dimension >= DIMENSIONS:
# 		return None, []

# 	my_root = None

# 	for node in my_list:
# 		my_root = insert(my_root, node)

# 	return my_root



def merge(root, left_list, right_list, dimension=0):
	if dimension >= DIMENSIONS:
		return []

	final_list = []

	i = 0
	j = 0

	while i < len(left_list) and j < len(right_list):
		if left_list[i].coords[dimension] < right_list[j].coords[dimension]:
			final_list.append(Node(left_list[i].coords, left_list[i].data))
			i = i + 1
		else:
			final_list.append(Node(right_list[j].coords, right_list[j].data))
			j = j + 1

	while i < len(left_list):
		final_list.append(Node(left_list[i].coords, left_list[i].data))
		i = i + 1

	while j < len(right_list):
		final_list.append(Node(right_list[j].coords, right_list[j].data))
		j = j + 1

	if root is None:
		return final_list

	for i in range(0, len(final_list)):
		if root.coords[dimension] < final_list[i].coords[dimension]:
			# case middle
			return final_list[: i] + [Node(root.coords, root.data)] + final_list[i: ]
	
	# case last
	return final_list + [Node(root.coords, root.data)]


def insert(root, node, dimension=0):
	if root is None:
		if dimension + 2 == DIMENSIONS:
			node.next_dimension = [Node(node.coords, node.data, -1, -1)]
		else:
			node.next_dimension = [Node(node.coords, node.data)]
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)


	if dimension + 2 == DIMENSIONS:
		place = findClosest(node.coords, root.next_dimension, dimension + 1) #find correct place for new node in the list
		
		#inserting
		if place == -1:
			root.next_dimension.append(Node(node.coords,node.data, -1, -1))
		else:
			root.next_dimension = root.next_dimension[: place] + [Node(node.coords,node.data)] + root.next_dimension[place: ]

		#for every node in the lists find new closests.
		for node_y in root.next_dimension:
			if root.left:
				node_y.left = findClosest(node_y.coords, root.left.next_dimension, dimension + 1)
			if root.right:
				node_y.right = findClosest(node_y.coords, root.right.next_dimension, dimension + 1)
	
	elif dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
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


	if dimension + 2 == DIMENSIONS:

		for node in root.next_dimension:
			if node.coords == delete_coords:
				root.next_dimension.remove(node)
		
		for node_y in root.next_dimension:
			if root.left:
				node_y.left = findClosest(node_y.coords, root.left.next_dimension, dimension+1)
			if root.right:
				node_y.right = findClosest(node_y.coords, root.right.next_dimension, dimension+1)
		
	elif dimension + 1 < DIMENSIONS:  # y = 1 DIMENSIONS = 2
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

		index = findClosest([0, range_coords[1][0]], split_node.next_dimension, dimension + 1)

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


def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))

        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")


def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tdata:" + str(node.data))


# checks if two lists have same Nodes
def are_equal(list1, list2):

	if len(list1) != len(list2):
		return False

	list1_sorted = sorted(list1,key=lambda l:(l.coords[0], l.coords[1]))
	list2_sorted = sorted(list2,key=lambda l:(l.coords[0], l.coords[1]))

	for i in range(0, len(list1_sorted)):
		if list1_sorted[i].coords != list2_sorted[i].coords:
			print(list1_sorted[i].coords)
			print(list2_sorted[i].coords)
			return False
	
	return True


# brute force range search for checking answer
def bruteforce_range_search(root, range_coords):
	nodes_list = []
	if root:
		if is_in_range(root.coords, range_coords):
			nodes_list.append(root)
		
		
		nodes_list += bruteforce_range_search(root.left, range_coords)
		nodes_list += bruteforce_range_search(root.right, range_coords)
	
	return nodes_list


# def bruteforce_range_search(my_list, range_coords):
# 	nodes_list = []
# 	for node in my_list:
# 		if is_in_range(node.coords, range_coords):
# 			nodes_list.append(node)

# 	return nodes_list


# Main Program

my_nodes = [
	Node([1.7, 0.0], 'aaa'),
	Node([1.5, 1.0], 'bbb'),
    Node([2.0, 5.0], 'ccc'),
    Node([3.0, 4.0], 'ddd'),
    Node([6.0, 8.0], 'eee'),
    Node([1.0, 9.0], 'fff'),
    Node([5.0, 7.0], 'ggg'),
    Node([1.2, 3.0], 'hhh'),
    Node([1.1, 2.0], 'iii'),
    Node([1.3, 4.4], 'jjj'),
    Node([1.4, 2.2], 'kkk')
]


x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])


my_root, _ = createTree(x_sorted_nodes)



print('-----------------------')
pre_order(my_root)
print('-----------------------')


# Insert Test
my_root = insert(my_root, Node([1.5, 1], '111'))
# pre_order(my_root)
# print('-----------------------')

# Search Test
alist = search(my_root, [1.3, 4.4])
# print_nodes(alist)
# print('-----------------------')

# Delete Test
my_root = delete(my_root, [1.5, 1])
# pre_order(my_root)
# print('-----------------------')

# Insert Test
my_root = insert(my_root, Node([1.5, 1.0], '222'))
# pre_order(my_root)
# print('-----------------------')

# Insert Test
my_root = insert(my_root, Node([1.5, 1.0], '333'))
# pre_order(my_root)
# print('-----------------------')

# Insert Test
my_root = insert(my_root, Node([3.0, -7.0], '...'))
# pre_order(my_root)
# print('-----------------------')

# Delete Test
my_root = delete(my_root, [1.3, 4.4])
# pre_order(my_root)
# print('-----------------------')


# Range Search Test
# print_nodes(range_search(my_root, [[1.3, 3],[float('-inf'), float('inf')]]))

# Update Test
# my_root = update(my_root)
# pre_order(my_root)
# print('-----------------------')

my_range = [[1, 8], [8, 10]]
res_list = range_search(my_root, my_range)
print(res_list)
print_nodes(res_list)
# print('-----------------------')

brute_list = bruteforce_range_search(my_root, my_range)
if are_equal(brute_list, res_list):
	print("Lists are equal!")
else:
	print("Lists are NOT equal!")


