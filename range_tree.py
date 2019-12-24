DIMENSIONS = 2


class Node:
	def __init__(self, coords, data=None, left=None, right=None, bst=None):
		self.coords = coords
		self.data = data
		self.left = left
		self.right = right
		self.bst = bst


def createBST(my_list, dimension=0):

	if len(my_list) == 0:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = createBST(my_list[:mid], dimension)
	root.right, right_list = createBST(my_list[mid+1:], dimension)


	if dimension == DIMENSIONS - 1:	# if it's y dimension
		root.bst = None
		return root, []
	else:							# if it's x dimension
		final_list = merge(root, left_list, right_list, dimension + 1)
		root.bst, _ = createBST(final_list, dimension+1)
		return root, final_list


def merge(root, left_list, right_list, dimension=0):

	temp_left_list = []
	temp_right_list = []
	final_list = []


	for node in left_list:
		temp_left_list.append(Node(node.coords, node.data))

	for node in right_list:
		temp_right_list.append(Node(node.coords, node.data))

	i = 0
	j = 0

	while i < len(temp_left_list) and j < len(temp_right_list):
		if temp_left_list[i].coords[dimension] < temp_right_list[j].coords[dimension]:
			final_list.append(temp_left_list[i])
			i = i + 1
		else:
			final_list.append(temp_right_list[j])
			j = j + 1


	while i < len(temp_left_list):
		final_list.append(temp_left_list[i])
		i = i + 1

	while j < len(temp_right_list):
		final_list.append(temp_right_list[j])
		j = j + 1


	temp_root = Node(root.coords, root.data)

	for i in range(0, len(final_list)):
		if temp_root.coords[dimension] < final_list[i].coords[dimension]:
			# case middle
			return final_list[: i] + [temp_root] + final_list[i: ]
	
	# case last
	return final_list + [temp_root]


def insert(root, node, dimension=0):
	if root is None:
		node.bst = Node(node.coords, node.data)
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)

	if dimension + 1 < DIMENSIONS: # y = 1 DIMENSIONS = 2
		root.bst = insert(root.bst, Node(node.coords, node.data), dimension + 1)

	return root


def leftmost_node(node):
    while node.left is not None:
        node = node.left
    return node


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
		root.bst = delete(root.bst, delete_coords, dimension + 1)

	return root


# range_coords[dimension][0] - left
# range_coords[dimension][1] - right

def range_search(root, range_coords, dimension=0):
	if root is None:
			return None
	
	if dimension == DIMENSIONS - 1: # for y dimension

		is_in = True
		for d in range(0, DIMENSIONS):
			if root.coords[d] < range_coords[d][0] or root.coords[d] > range_coords[d][1]:
				is_in = False

		if is_in:
			print(root.coords)

		if root.coords[dimension] < range_coords[dimension][0]:
			range_search(root.right, range_coords, dimension)
		elif root.coords[dimension] > range_coords[dimension][1]:
			range_search(root.left, range_coords, dimension)
		else: #range_coords[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= range_coords[dimension][1]:
			range_search(root.right, range_coords, dimension)
			range_search(root.left, range_coords, dimension)


	else: # for x dimension find split node
		if root.coords[dimension] < range_coords[dimension][0]:
			range_search(root.right, range_coords, dimension)
		elif root.coords[dimension] > range_coords[dimension][1]:
			range_search(root.left, range_coords, dimension)
		else: #range_coords[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= range_coords[dimension][1]:
			range_search(root.bst, range_coords, dimension+1)


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


def update(root):
	coords = []
	for i in range (0, DIMENSIONS):
		coords.append(float(input("dimension " + str(i+1) + ": ")))

	answer = input("Do you want to update the tree keys? y/n: ")

	if answer == 'y':
		new_coords = []
		for i in range (0, DIMENSIONS):
			new_coords.append(float(input("dimension " + str(i+1) + ": ")))
		
		to_change_nodes = search(root, coords, 0)
		new_nodes = []
		for node in to_change_nodes:	# create new nodes
			new_nodes.append(Node(new_coords, node.data))
		for node in to_change_nodes:	# delete old nodes
			root = delete(root, coords)
		for node in new_nodes:			# insert new nodes
		  	root = insert(root, node)

		return root
	else:
		# for each dimension
		# search for these coordinates
		# change data for the returned lists
		return root



def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))
        pre_order(root.left, string + "-left-")
        pre_order(root.right, string + "-right-")


def print_nodes(nodes):
    for node in nodes:
        print(node.coords)



# Main Program

my_nodes = [
	Node([1.7, 11], 'aaa'),
	Node([1.5, 1], 'bbb'),
    Node([2,5], 'ccc'),
    Node([3,4], 'ddd'),
    Node([6,8], 'eee'),
    Node([1,9], 'fff'),
    Node([5,7], 'ggg')
]

x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])


my_root, _ = createBST(x_sorted_nodes)
pre_order(my_root)
print('-----------------------')

# my_root = insert(my_root, Node([1.2, 2], 'yyy'))
# pre_order(my_root)
# print('-----------------------')

# my_root = insert(my_root, Node([1.5, 9], 'www'))
# pre_order(my_root)
# print('-----------------------')

# my_root = insert(my_root, Node([1.5, 1], 'www'))
# pre_order(my_root)
# print('-----------------------')

# range_search(my_root, [[float('-inf'), 2],[float('-inf'), float('inf')]])

# my_root = delete(my_root, [1.5, 1])
# pre_order(my_root)
# print('-----------------------')


my_root = update(my_root)
pre_order(my_root)
print('-----------------------')

