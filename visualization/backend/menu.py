import csv
import time
import pathlib
from kd_tree.kd_tree import *


# checks if two lists have same Nodes
def are_equal(list1, list2):

	if len(list1) != len(list2):
		return False

	list1_sorted = sorted(list1,key=lambda l:(l.coords[0], l.coords[1], l.coords[2]))
	list2_sorted = sorted(list2,key=lambda l:(l.coords[0], l.coords[1], l.coords[2]))

	for i in range(0, len(list1_sorted)):
		if list1_sorted[i].coords != list2_sorted[i].coords:
			print(list1_sorted[i].coords)
			print(list2_sorted[i].coords)
			return False
	
	return True

# brute force range search for checking answer
def bruteforce_range_search(root, range_coords):
	nodes_list = []
	if root:
		if is_in_range(root.coords, range_coords):
			nodes_list.append(root)
		
		
		nodes_list += bruteforce_range_search(root.left, range_coords)
		nodes_list += bruteforce_range_search(root.right, range_coords)
	
	return nodes_list


# File to import selection


filename = 'airports.csv'
fn = pathlib.Path(__file__).parent / 'datasets' / filename

my_nodes = []

nodes_counter = 0
with open(fn, mode='r', encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count > 0: #and (row["type"] == "medium_airport" or row["type"] == "large_airport")
            my_nodes.append(Node([float(row["latitude_deg"]), float(row["longitude_deg"]), float(row["id"])], row["name"]))
            nodes_counter += 1
        line_count += 1
    print('Number of Nodes: ' + str(nodes_counter))


# Build Start

my_sorted_nodes = []
for i in range(0, DIMENSIONS):
    my_sorted_nodes.append(sorted(my_nodes, key=lambda l:l.coords[i]))

my_root = create_tree(my_sorted_nodes)

# Build End

# Range Search
import json
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import jsonify

app = Flask(__name__)
CORS(app)


# Main function
@app.route('/', methods=['GET'])
def hello():
    # data = request.get_json()
    xleft = float(request.args.get('xleft'))
    xright = float(request.args.get('xright'))
    yleft = float(request.args.get('yleft'))
    yright = float(request.args.get('yright'))

    my_range = [[xleft, xright],[yleft, yright]]

    res_list = range_search(my_root, my_range)
    if len(res_list) == 0:
        return "Not found"
    else:
        print('Nodes found:')
        brute_list = bruteforce_range_search(my_root, my_range)
        if are_equal(brute_list, res_list):
            print("Lists are equal!")
        else:
            print("Lists are NOT equal!")

        final_list = []
        for node in res_list:
            my_object = {}
            my_object["x"] = node.coords[0]
            my_object["y"] = node.coords[1]
            my_object["data"] = node.data
            final_list.append(my_object)

        return jsonify(final_list)


if __name__ == "__main__":
    app.run()
