DIMENSIONS = 2


class Node:
    def __init__(self, coords, data=None, left=None, right=None):
        self.left = left
        self.right = right
        self.coords = coords
        self.data = data


# create kd tree
def create_tree(nodes, depth=0):

    axis = depth % DIMENSIONS

    if len(nodes[axis]) == 0:
        return None

    if len(nodes[axis]) == 1:
        return nodes[axis][0]

    mid = int(len(nodes[axis])/2)

    middle_node = nodes[axis][mid]

    left = []
    right = []

    for i in range(0, DIMENSIONS):
        l = []
        r = []
        for node in nodes[i]:
            if node.coords[axis] < middle_node.coords[axis]:
                l.append(node)
            elif node.coords[axis] > middle_node.coords[axis]:
                r.append(node)

        left.append(l)
        right.append(r)

    middle_node.left = create_tree(left, depth+1)
    middle_node.right = create_tree(right, depth+1)

    return middle_node


# insert node
def insert(root, node, depth=0):
    if root is None:
        return node
    else:
        axis = depth % DIMENSIONS  # axis = 0 or 1
        if node.coords[axis] <= root.coords[axis]:  # = x_nodes[mid][0]
            root.left = insert(root.left, node, depth+1)
        else:
            root.right = insert(root.right, node, depth+1)
        return root


# search node
def search(root, coords):
	depth = 0
	while root and root.coords != coords:
		axis = depth % DIMENSIONS  # axis = 0 or 1
		if coords[axis] <= root.coords[axis]:
			root = root.left
			# print("left")
		else:
			root = root.right
			# print("right")
		depth = depth + 1

	if root:
		print("Found!")
		return root.coords
	else:
		print("Not Found!")
		return None


# checks if coords are inside a given range
def is_in_range(coords, range_coords):
	is_in = True
	for d in range(0, DIMENSIONS):
		if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
			is_in = False

	return is_in


def range_search(root, bounds, depth=0):
    if root is None:
        return []
        
    axis = depth % DIMENSIONS  # axis = 0 or 1
    
    if bounds[axis][1] < root.coords[axis]:
    	# proon rightchild
        return range_search(root.left, bounds, depth+1)

    elif bounds[axis][0] > root.coords[axis]:
        # proon leftchild
        return range_search(root.right, bounds, depth+1)
        
    elif bounds[axis][0] <= root.coords[axis] and root.coords[axis] <= bounds[axis][1]:
        # inside bounds
        if is_in_range(root.coords, bounds):
            return range_search(root.left, bounds, depth+1) + [root] + range_search(root.right, bounds, depth+1)

        return range_search(root.left, bounds, depth+1) + range_search(root.right, bounds, depth+1)


# find node to replace
def find_minimum(root, depth, target_axis):

    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1


    if axis == target_axis:
        left = findMinimum(root.left, depth+1, target_axis)
        if left is not None and left.coords[axis] < root.coords[axis]:
            return left
        else:
            return root
    else:
        left = findMinimum(root.left, depth+1, target_axis)
        right = findMinimum(root.right, depth+1, target_axis)

        if left is not None and left.coords[axis] < root.coords[axis] and (right is None or left.coords[axis] < right.coords[axis]):
            return left
        elif right is not None and right.coords[axis] < root.coords[axis] and (left is None or right.coords[axis] < left.coords[axis]):
            return right
        else:
            return root


def find_maximum(root, depth, target_axis):

    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1


    if axis == target_axis:
        right = findMaximum(root.right, depth+1, target_axis)
        if right is not None and right.coords[target_axis] > root.coords[target_axis]:
            return right
        else:
            return root
    else:
        left = findMaximum(root.left, depth+1, target_axis)
        right = findMaximum(root.right, depth+1, target_axis)
        if left is not None and left.coords[target_axis] > root.coords[target_axis] and (right is None or left.coords[target_axis] > right.coords[target_axis]):
            return left
        elif right is not None and right.coords[target_axis] > root.coords[target_axis] and (left is None or right.coords[target_axis] > left.coords[target_axis]):
            return right
        else:
            return root


# deleteNode
def delete_node(root, coords, depth=0):
    if root is None:
        return None

    axis = depth % DIMENSIONS  # axis = 0 or 1
    if root.coords == coords:
        if root.left is None and root.right is None:  # leaf
            del root
            return None
        elif root.left is None:
            temp = findMinimum(root.right, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords
        else:
            temp = findMaximum(root.left, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords

    elif coords[axis] <= root.coords[axis]:
        root.left = delete(root.left, coords, depth + 1)
    else:  # coords[axis] > root.coords[axis]
        root.right = delete(root.right, coords, depth + 1)

    return root


def pre_order(root, string=""):
    if root:
        print(string + str(root.coords) + "|data:" + str(root.data))

        pre_order(root.left, "\t" + string + "-left-")
        pre_order(root.right, "\t" + string + "-right-")


def print_nodes(nodes_list):
	for node in nodes_list:
		print(str(node.coords) + "\t|\tdata:" + str(node.data))
