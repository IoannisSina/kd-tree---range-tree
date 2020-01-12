import csv
import time
import pathlib


from range_tree.range_tree import *
filename = 'airports.csv'
fn = pathlib.Path(__file__).parent / 'datasets' / filename


my_nodes = []

with open(fn, mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count > 0 and (row["type"] == "medium_airport" or row["type"] == "large_airport"):
            my_nodes.append(Node([float(row["latitude_deg"]), float(row["longitude_deg"])], row["name"]))
        line_count += 1
    print('Processed ' + str(line_count) + ' lines')



# Build Start

start = time.time()

x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])

my_root, _ = create_tree(x_sorted_nodes)

end = time.time()
print("Build Time: " + str(end - start))

# Build End


# print('-----------------------')
# pre_order(my_root)
# print('-----------------------')

# # Insert Test
# my_root = insert(my_root, Node([1.5, 1], '111'))
# # pre_order(my_root)
# # print('-----------------------')

# # Search Test
# alist = search(my_root, [1.3, 4.4])
# # print_nodes(alist)
# # print('-----------------------')

# # Delete Test
# my_root = delete(my_root, [1.5, 1])
# # pre_order(my_root)
# # print('-----------------------')

# # Insert Test
# my_root = insert(my_root, Node([1.5, 1.0], '222'))
# # pre_order(my_root)
# # print('-----------------------')

# # Insert Test
# my_root = insert(my_root, Node([1.5, 1.0], '333'))
# # pre_order(my_root)
# # print('-----------------------')

# # Insert Test
# my_root = insert(my_root, Node([3.0, -7.0], '...'))
# # pre_order(my_root)
# # print('-----------------------')

# # Delete Test
# my_root = delete(my_root, [1.3, 4.4])
# # pre_order(my_root)
# # print('-----------------------')

# # Update Test
# # my_root = update(my_root)
# # pre_order(my_root)
# # print('-----------------------')

start = time.time()


my_range = [[33, 34], [-119, -118]]
res_list = range_search(my_root, my_range)
# print(res_list)
# print_nodes(res_list)

brute_list = bruteforce_range_search(my_root, my_range)
if are_equal(brute_list, res_list):
	print("Lists are equal!")
else:
	print("Lists are NOT equal!")


end = time.time()

print("Range Time: " + str(end - start))