DIMENSIONS = 2


class Node:
	def __init__(self, left, right, coords, bst=None):
		self.left = left
		self.right = right
		self.coords = coords
		self.bst = bst


def createBST(my_list, dimension):

	if len(my_list) == 0:
		return None, []
	
	mid = int(len(my_list)/2)

	root = my_list[mid]
	root.left, left_list = createBST(my_list[:mid], dimension)
	root.right, right_list = createBST(my_list[mid+1:], dimension)


	if dimension == DIMENSIONS - 1: # if it's y dimension
		root.bst = None
		return root, []
	else:							              # if it's x dimension
		final_list = merge(root, left_list, right_list, dimension + 1)
		root.bst, _ = createBST(final_list, dimension+1)
		return root, final_list


def merge(root, left_list, right_list, dimension):

	temp_left_list = []
	temp_right_list = []
	final_list = []


	for node in left_list:
		temp_left_list.append(Node(None, None, node.coords))

	for node in right_list:
		temp_right_list.append(Node(None, None, node.coords))

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


	temp_root = Node(None, None, root.coords)

	for i in range(0, len(final_list)):
		if temp_root.coords[dimension] < final_list[i].coords[dimension]:
			# case middle
			return final_list[: i] + [temp_root] + final_list[i: ]
	
	# case last
	return final_list + [temp_root]


def insert(root, node, dimension):

	if root is None:
		return node
	
	if node.coords[dimension] <= root.coords[dimension]:
		root.left = insert(root.left, node, dimension)
	else:
		root.right = insert(root.right, node, dimension)

	if dimension < DIMENSIONS: # y = 1 DIMENSIONS = 2
		root.bst = insert(root.bst, node, dimension + 1)

	return root

	# insert in bstX
	# recursively in every parent insert in bstY





def pre_order(root, string):
    if root:
        print(string + str(root.coords))
        pre_order(root.left, string + "-left-")
        pre_order(root.right, string + "-right-")


def print_nodes(nodes):
    for node in nodes:
        print(node.coords)






# Main Program

my_nodes = [
	Node(None,None,[1.7, 11]),
	Node(None,None,[1.5, 1]),
    Node(None,None,[2,5]),
    Node(None,None,[3,4]),
    Node(None,None,[6,8]),
    Node(None,None,[1,9]),
    Node(None,None,[5,7])
]


x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])
#print_nodes(x_sorted_nodes)
#print('-------------')


my_root, _ = createBST(x_sorted_nodes, 0)


'''
pre_order(my_root.left, "")
print('-----------------------')
pre_order(my_root.left.bst, "")
'''

pre_order(my_root, "")
print('-----------------------')
insert(my_root, Node(None,None,[10, 5]), 0)
pre_order(my_root, "")
print('-----------------------')
pre_order(my_root.right.right.bst, "")
print('-----------------------')
pre_order(my_root.right.bst, "")
print('-----------------------')
pre_order(my_root.bst, "")


