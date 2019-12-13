DIMENSIONS = 2

class Node:
    def __init__(self, coords = [DIMENSIONS]):
        self.left = None
        self.right = None
        self.coords = coords


#insert node
def insert(root, node, depth=0):
    if root is None:
        return node
    else:
        axis = depth % DIMENSIONS # axis = 0 or 1
        if node.coords[axis] <= root.coords[axis]: #= x_nodes[mid][0]
            root.left = insert(root.left, node, depth+1)
        else:
            root.right = insert(root.right, node, depth+1)
        return root


def print_nodes(nodes):
    for node in nodes:
        print(node.coords)


#create kd tree
def create(root=None, nodes, depth=0):

    axis = depth % DIMENSIONS

    if len(nodes[axis]) == 0:
        return None

    if len(nodes[axis]) == 1:
        return nodes[axis][0]

    mid = int(len(nodes[axis])/2)

    middle_node = nodes[axis][mid]

    left = []
    right = []


    for i in range (0,DIMENSIONS):
        l = []
        r = []
        for node in nodes[i]:
            if node.coords[axis] < middle_node.coords[axis]:
                l.append(node)
            elif node.coords[axis] > middle_node.coords[axis]:
                r.append(node)

        left.append(l)
        right.append(r)


    middle_node.left = create(root, left, depth+1)
    middle_node.right = create(root, right, depth+1)

    return middle_node


def pre_order(root, string):
    if root:
        print(string + str(root.coords))
        pre_order(root.left, string + "-left-")
        pre_order(root.right, string + "-right-")


#search node
def search(root, coords = [DIMENSIONS]):
	depth = 0
	while root and root.coords != coords:
		axis = depth % DIMENSIONS # axis = 0 or 1
		print(axis)
		if coords[axis] <= root.coords[axis]:
			root = root.left
			print("left")
		else:
			root = root.right
			print("right")
		depth = depth + 1

	if root:
		print("Found!")
		return root.coords
	else:
		print("Not Found!")
		return None



# bounds = [xE(0,10), yE(0,2)]

def rangesearch(root, bounds, depth=0):
	if root is None:
		return

	axis = depth % DIMENSIONS # axis = 0 or 1


	if bounds[axis][1] < root.coords[axis]:
    	# proon rightchild
		rangesearch(root.left, bounds, depth+1)

	elif bounds[axis][0] > root.coords[axis]:
    	# proon leftchild
		rangesearch(root.right, bounds, depth+1)

	elif bounds[axis][0] <= root.coords[axis] and root.coords[axis] <= bounds[axis][1]:
		# inside bounds
		flag = 0
		for axis in range (0, DIMENSIONS):
			if bounds[axis][0] > root.coords[axis] or root.coords[axis] > bounds[axis][1]:
				flag = 1
				break
		if flag == 0:
			print("maybe is in: " + str(root.coords))

		rangesearch(root.left, bounds, depth+1)
		rangesearch(root.right, bounds, depth+1)



#find node to replace
def findLeftMostNode(root, depth):

	target_axis = depth % DIMENSIONS

	leftMost = root # same axis

	while root.left is not None:
		root = root.left
		depth = depth + 1
		axis = depth % DIMENSIONS

		if axis == target_axis:
			leftMost = root

	return leftMost


def findRightMost(root, depth):

	target_axis = depth % DIMENSIONS

	rightMost = root # same axis

	while root.right is not None:
		root = root.right
		depth = depth + 1
		axis = depth % DIMENSIONS

		if axis == target_axis:
			rightMost = root

	return rightMost




# deleteNode
def delete(root, coords, depth=0):
	if root is None:
		return None

	axis = depth % DIMENSIONS # axis = 0 or 1
	print(root.coords)
	print(coords)
	print(root.coords == coords)
	if root.coords == coords:
		if root.left is None and root.right is None: # leaf
			print("KKKKKKKKKKK")
			print(root.coords)
			#del root
			return None

		elif root.left is None:
			temp = findLeftMostNode(root.right, depth)
			delete(root, temp.coords, depth)
			root.coords = temp.coords

		else:
			temp = findRightMost(root.left, depth)
			delete(root, temp.coords, depth)
			root.coords = temp.coords

	elif coords[axis] <= root.coords[axis]:
		root.left = delete(root.left, coords, depth+1)
	else: #coords[axis] > root.coords[axis]
		root.right = delete(root.right, coords, depth+1)
		#print(root.right.coords)

	return root




# MAIN PROGRAM

my_nodes = [
    Node([2,5]),
    Node([3,4]),
    Node([6,8]),
    Node([1,9]),
    Node([5,7])
]

my_sorted_nodes = []
for i in range(0, DIMENSIONS):
    my_sorted_nodes.append(sorted(my_nodes,key=lambda l:l.coords[i]))

my_root = create(my_sorted_nodes)


#search(my_root, [1,9])

# x_bounds = [0, 10]
# y_bounds = [0, 9]
# my_bounds = [x_bounds, y_bounds]

# rangesearch(my_root, my_bounds)

# node_to_delete = search(my_root, [2,5])
# delete()


insert(my_root, Node([1.5, 10]))
insert(my_root, Node([1.7, 11]))


print("=============================================\n")

pre_order(my_root, "")

print("=============================================\n")

delete(my_root, [3, 4])

print("=============================================\n")

pre_order(my_root, "")
