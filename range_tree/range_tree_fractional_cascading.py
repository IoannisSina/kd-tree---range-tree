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



def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))

        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")


def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tdata:" + str(node.data) + "\t|\tleft:" + str(node.left) + "\t|\tright:" + str(node.right))


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
print('-----------------------')
pre_order(my_root)
print('-----------------------')
print_nodes(my_root.next_dimension)
print('-----------------------')
print_nodes(my_root.left.next_dimension)
print('-----------------------')
print_nodes(my_root.right.next_dimension)
print('-----------------------')
