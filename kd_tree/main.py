from kd_tree import *


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

my_root = create_tree(my_sorted_nodes)


x_bounds = [0, 10]
y_bounds = [0, 9]
my_bounds = [x_bounds, y_bounds]

print("=============================================\n")
pre_order(my_root)
print("=============================================\n")
print_nodes(rangesearch(my_root, my_bounds))


# my_root = insert(my_root, Node([1.5, 10]))

# print("=============================================\n")

# my_root = delete(my_root, [3, 4])

# print("=============================================\n")

# pre_order(my_root)
