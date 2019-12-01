dimensions = 2

class Node:
    def __init__(self, left=None, right=None, coords = [dimensions]):
        self.left = left
        self.right = right
        self.coords = coords


nodes = [
    Node(None,None,[2,5]),
    Node(None,None,[3,4]),
    Node(None,None,[6,8]),
    Node(None,None,[1,9]),
    Node(None,None,[5,7])
]

x_nodes = sorted(nodes,key=lambda l:l.coords[0])
y_nodes = sorted(nodes,key=lambda l:l.coords[1])
sorted_nodes = [x_nodes, y_nodes]

for node in x_nodes:
    print(node.coords)
print("---")
for node in y_nodes:
    print(node.coords)




def insert(root, node, depth):
    if root is None:
        return node
    else:
        dimension = depth % dimensions # dimension = 0 or 1
        if node.coords[dimension] <= root.coords[dimension]: #= x_nodes[mid][0]
            root.left = insert(root.left, node, depth+1)
        else:
            root.right = insert(root.right, node, depth+1)
        return root


def create(root, left, right, depth):

    dimension = depth % dimensions
    mid = int((right[dimension]-left[dimension])/2)
    new_node = sorted_nodes[dimension][mid]
    root = insert(root, new_node, depth)

    print("here1")

    if right[0] - left[0] == 0 or right[1] - left[1] == 0:
        print("here2")
        return root


    # left
    n_right = right
    n_right[dimension] = mid - 1
    root.left = create(root, left, n_right, depth+1)

    # right
    left[dimension] = mid + 1
    root.right = create(root, left, right, depth+1)

    return root


def in_order(root):
    if root is None:
        return

    in_order(root.left)
    print(root.coords)
    in_order(root.right)


my_root = None
my_root = create(my_root, [0, 0], [len(nodes)-1, len(nodes)-1], 0)
in_order(my_root)
