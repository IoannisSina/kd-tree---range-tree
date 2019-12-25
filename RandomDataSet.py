from range_tree import * 
import random
import secrets
import string
DIMENSIONS = 2



def check_range(nodes, range_coords):

  all_in_range=True
	for node in nodes:
		if( not is_in_range(node.coords , range_coords )):
			all_in_range=False

  if(all_in_range):
  	print("All points ane in range")
  else:
  	print("mistake")
	




#MAIN

my_nodes = []
N=5


for j in range(0,100000):
	res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))
	my_nodes.append(Node( [ random.randint(-1000,1000) , random.randint(-1000,1000) ], res))
  
x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])

my_root, _ = createBST(x_sorted_nodes)

my_range=[[ 150 , 400] ,[float('-inf'), float('inf')]]
my_list = range_search(my_root, my_range)
print_nodes(my_list)
check_range(my_list, my_range)
