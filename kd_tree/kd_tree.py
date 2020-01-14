DIMENSIONS = 3


class Node:
    def __init__(self, coords, data=None, left=None, right=None):
        self.left = left
        self.right = right
        self.coords = coords
        self.data = data


# create kd tree
def create_tree(nodes, depth=0):

    dimension = depth % DIMENSIONS

    if len(nodes[dimension]) == 0:
        return None

    if len(nodes[dimension]) == 1:
        return nodes[dimension][0]

    mid = int(len(nodes[dimension])/2)

    middle_node = nodes[dimension][mid]

    left = []
    right = []

    for i in range(0, DIMENSIONS):
        l = []
        r = []
        for node in nodes[i]:
            if node.coords[dimension] < middle_node.coords[dimension]:
                l.append(node)
            elif node.coords[dimension] > middle_node.coords[dimension]:
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
        dimension = depth % DIMENSIONS  # dimension = 0 or 1
        if node.coords[dimension] <= root.coords[dimension]:  # = x_nodes[mid][0]
            root.left = insert(root.left, node, depth+1)
        else:
            root.right = insert(root.right, node, depth+1)
        return root


# search node
def search(root, coords):
    res_list = []

    depth = 0
    while root:
        dimension = depth % DIMENSIONS  # dimension = 0 or 1
        if coords[dimension] < root.coords[dimension]:
            root = root.left
        elif coords[dimension] > root.coords[dimension]:
            root = root.right
        else:
            res_list.append(root)
            root = root.left
        depth = depth + 1
    
    return res_list


# checks if coords are inside a given range
def is_in_range(coords, range_coords):
	for d in range(0, DIMENSIONS):
		if coords[d] < range_coords[d][0] or coords[d] > range_coords[d][1]:
			return False

	return True


def range_search(root, bounds, depth=0):
    if root is None:
        return []
        
    dimension = depth % DIMENSIONS  # dimension = 0 or 1
    
    if bounds[dimension][1] < root.coords[dimension]:
    	# proon rightchild
        return range_search(root.left, bounds, depth+1)

    elif bounds[dimension][0] > root.coords[dimension]:
        # proon leftchild
        return range_search(root.right, bounds, depth+1)
        
    elif bounds[dimension][0] <= root.coords[dimension] and root.coords[dimension] <= bounds[dimension][1]:
        # inside bounds
        if is_in_range(root.coords, bounds):
            return range_search(root.left, bounds, depth+1) + [root] + range_search(root.right, bounds, depth+1)

        return range_search(root.left, bounds, depth+1) + range_search(root.right, bounds, depth+1)


# find node to replace
def find_minimum(root, depth, target_dimension):

    if root is None:
        return None

    dimension = depth % DIMENSIONS  # dimension = 0 or 1


    if dimension == target_dimension:
        left = find_minimum(root.left, depth+1, target_dimension)
        if left is not None and left.coords[dimension] < root.coords[dimension]:
            return left
        else:
            return root
    else:
        left = find_minimum(root.left, depth+1, target_dimension)
        right = find_minimum(root.right, depth+1, target_dimension)

        if left is not None and left.coords[dimension] < root.coords[dimension] and (right is None or left.coords[dimension] < right.coords[dimension]):
            return left
        elif right is not None and right.coords[dimension] < root.coords[dimension] and (left is None or right.coords[dimension] < left.coords[dimension]):
            return right
        else:
            return root


def find_maximum(root, depth, target_dimension):

    if root is None:
        return None

    dimension = depth % DIMENSIONS  # dimension = 0 or 1


    if dimension == target_dimension:
        right = find_maximum(root.right, depth+1, target_dimension)
        if right is not None and right.coords[target_dimension] > root.coords[target_dimension]:
            return right
        else:
            return root
    else:
        left = find_maximum(root.left, depth+1, target_dimension)
        right = find_maximum(root.right, depth+1, target_dimension)
        if left is not None and left.coords[target_dimension] > root.coords[target_dimension] and (right is None or left.coords[target_dimension] > right.coords[target_dimension]):
            return left
        elif right is not None and right.coords[target_dimension] > root.coords[target_dimension] and (left is None or right.coords[target_dimension] > left.coords[target_dimension]):
            return right
        else:
            return root


def delete(root, coords, depth=0):
    if root is None:
        return None

    dimension = depth % DIMENSIONS  # dimension = 0 or 1
    if root.coords == coords:
        if root.left is None and root.right is None:  # leaf
            del root
            return None
        elif root.left is None:
            temp = find_minimum(root.right, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords
        else:
            temp = find_maximum(root.left, depth+1, depth % DIMENSIONS)
            delete(root, temp.coords, depth)
            root.coords = temp.coords

    elif coords[dimension] <= root.coords[dimension]:
        root.left = delete(root.left, coords, depth + 1)
    else:  # coords[dimension] > root.coords[dimension]
        root.right = delete(root.right, coords, depth + 1)

    return root


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
