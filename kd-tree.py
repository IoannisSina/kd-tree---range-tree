DIMENSIONS = 2


class Node:
    def __init__(self, left, right, coords = [DIMENSIONS]):
        self.left = left
        self.right = right
        self.coords = coords


def insert(root, node, depth):
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


def create(root, nodes, depth):

    axis = depth % DIMENSIONS

    if len(nodes[axis]) == 0:
        return None

    if len(nodes[axis]) == 1:
        return nodes[axis][0]

    mid = int(len(nodes[axis])/2)

    '''
    print("mid: " + str(mid))
    print("mid node --- " + str(nodes[axis][mid].coords))
    print(print_nodes(nodes[0]))
    print("-")
    print(print_nodes(nodes[1]))
    '''
    
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

    '''
    print("left 0")
    print_nodes(left[0])
    print("left 1")
    print_nodes(left[1])
    print("right 0")
    print_nodes(right[0])
    print("right 1")
    print_nodes(right[1])
    '''

    middle_node.left = create(root, left, depth+1)
    middle_node.right = create(root, right, depth+1)

    return middle_node


def pre_order(root, string):
    if root:
        print(string + str(root.coords))
        pre_order(root.left, string + "-left-")
        pre_order(root.right, string + "-right-")



# MAIN PROGRAM

my_nodes = [
    Node(None,None,[2,5]),
    Node(None,None,[3,4]),
    Node(None,None,[6,8]),
    Node(None,None,[1,9]),
    Node(None,None,[5,7])
]

my_sorted_nodes = []
for i in range(0, DIMENSIONS):
    my_sorted_nodes.append(sorted(my_nodes,key=lambda l:l.coords[i]))

'''
for node in my_sorted_nodes[0]:
    print(node.coords)
print("---")
for node in my_sorted_nodes[1]:
    print(node.coords)
'''

my_root = None
my_root = create(my_root, my_sorted_nodes, 0)
pre_order(my_root, "")
