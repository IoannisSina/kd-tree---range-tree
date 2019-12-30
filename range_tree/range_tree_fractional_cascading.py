DIMENSIONS = 2


class Node:
	def __init__(self, coords, data=None, left=None, right=None, next_dimension=None):
		self.coords = coords
		self.data = data
		self.left = left
		self.right = right
		self.next_dimension = next_dimension


def findClosest(node, nodes_list, dimension):
	if len(nodes_list) == 0:
		return -1
	i = 0
	while i < len(nodes_list) and node.coords[dimension] > nodes_list[i].coords[dimension]:
		i = i + 1
	
	return i if i < len(nodes_list) else -1


def createBST(my_list, dimension=0):

	if len(my_list) == 0 or dimension >= DIMENSIONS:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = createBST(my_list[:mid], dimension)
	root.right, right_list = createBST(my_list[mid+1:], dimension)

	merged_list = []
	if dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		merged_list = merge(root, left_list, right_list, dimension + 1)

		if dimension + 2 == DIMENSIONS:	# last - 1 dimension
			for node in merged_list:
				node.left = findClosest(node, left_list, dimension + 1)
				node.right = findClosest(node, right_list, dimension + 1)
			

			root.next_dimension = merged_list

			return root, merged_list
	else:
		root.next_dimension, _ = createBST(merged_list, dimension + 1)
		return root, merged_list


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


	final_list += left_list[i:]
	final_list += right_list[j:]

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
			node.next_dimension = [Node(node.coords, node.data)]
		else:
			node.next_dimension = Node(node.coords, node.data)
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)


	if dimension + 2 == DIMENSIONS:
		place = findClosest(node, root.next_dimension, dimension+1) #find correct place for new node in the list
		
		#inserting
		if place == -1:
			root.next_dimension.append(Node(node.coords,node.data))
		else:
			root.next_dimension = root.next_dimension[: place] + [Node(node.coords,node.data)] + root.next_dimension[place: ] 
		

		#for every node in the lists find new closests.
		for node_y in root.next_dimension:
			if root.left:
				node_y.left = findClosest(node_y, root.left.next_dimension, dimension+1)
			if root.right:
				node_y.right = findClosest(node_y, root.right.next_dimension, dimension+1)
		
	
	elif dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
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



	if dimension + 2 == DIMENSIONS:

		for node in root.next_dimension:
			if node.coords == delete_coords:
				root.next_dimension.remove(node)
		
		for node_y in root.next_dimension:
			if root.left:
				node_y.left = findClosest(node_y, root.left.next_dimension, dimension+1)
			if root.right:
				node_y.right = findClosest(node_y, root.right.next_dimension, dimension+1)
		
	

	elif dimension + 1 < DIMENSIONS:  # y = 1 DIMENSIONS = 2
		root.next_dimension = delete(root.next_dimension, delete_coords, dimension + 1)

	return root



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
	is_in = True
	for d in range(0, DIMENSIONS):
		if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
			is_in = False
	
	return is_in


# returns a list of Nodes inside a range
def range_search(root, range_coords, dimension=0):
	if root is None:
		return []

	# d-1 dimensions
	if dimension + 2 < DIMENSIONS:
		# find split node
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

	# last-1 dimension
	if dimension + 2 == DIMENSIONS:

		split_node = find_split_node(root, range_coords, dimension)

		if split_node is None:
			return []

		nodes_list = []

		if is_in_range(split_node.coords, range_coords):
			nodes_list.append(split_node)
		
		split_node_index = findClosest(split_node, split_node.next_dimension, dimension+1)

		return range_search1(split_node, split_node_index, range_coords, dimension) + nodes_list



# index show where to start in node.next_dimension

def range_search1(node, index, range_coords, dimension):

	nodes_list = []

	index1 = index

	left_child = node.left
	while left_child:
		if is_in_range(left_child.coords, range_coords):
			nodes_list.append(left_child)
		if range_coords[dimension][0] <= left_child.coords[dimension]:
			# 1DRangeSearch
			if left_child.right:
				for i in range(node.next_dimension[index1].right, len(left_child.right.next_dimension)):
					if is_in_range(left_child.right.next_dimension[i].coords, range_coords):
						nodes_list.append(left_child.right.next_dimension[i])
			
			index1 = left_child.next_dimension[index1].left
			left_child = left_child.left
		else:
			index1 = left_child.next_dimension[index1].right
			left_child = left_child.right


	right_child = node.right
	while right_child:
		if is_in_range(right_child.coords, range_coords):
			nodes_list.append(right_child)
		if right_child.coords[dimension] <= range_coords[dimension][1]:
			# 1DRangeSearch
			if right_child.left:
				for i in range(node.next_dimension[index].left, len(right_child.left.next_dimension)):
					if is_in_range(right_child.left.next_dimension[i].coords, range_coords):
						nodes_list.append(right_child.left.next_dimension[i])

			index = right_child.next_dimension[index].right
			right_child = right_child.right	# continue same dimension
		else:
			index = right_child.next_dimension[index].left
			right_child = right_child.left	# continue same dimension

	return nodes_list



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


# def check_tree(root, dimension=0):

# 	result = True

# 	if dimension + 1 < DIMENSIONS:
# 		if root.left:
# 			result = result and check_tree(root.left)
# 		if root.right:
# 			result = result and check_tree(root.right)
			
# 	if dimension + 2 == DIMENSIONS:  # y = 1 DIMENSIONS = 2
# 		for node in root.next_dimension:
# 				if root.left:
# 					if node.left != findClosest(node, root.left.next_dimension, dimension + 1):
# 						return False
# 				if root.right:
# 					if node.right != findClosest(node, root.right.next_dimension, dimension + 1):
# 						return False
			
# 		return True
	
# 	# elif dimension + 1 < DIMENSIONS:
# 	# 	result1 = check_tree(root.next_dimension)
		
# 	return result




def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))

        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")

def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tdata:" + str(node.data))



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


my_root, _ = createBST(x_sorted_nodes)

# print('-----------------------')
# pre_order(my_root)
# print('-----------------------')
# print_nodes(my_root.next_dimension)
# print('-----------------------')
# print_nodes(my_root.left.next_dimension)
# print('-----------------------')
# print_nodes(my_root.right.next_dimension)
# print('-----------------------')

new_node= Node([2.5,5.0],'666')
my_root= insert(my_root, new_node ,0)

pre_order(my_root)
print('-----------------------')

# Delete Test
my_root = delete(my_root, [1.4, 2.2])


pre_order(my_root)
print('-----------------------')

my_root.right.next_dimension[0].left = 878

print_nodes(range_search(my_root, [[1.3, 3],[4, 5]]))
