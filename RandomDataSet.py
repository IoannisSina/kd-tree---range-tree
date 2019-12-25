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




for j in range(0,int(input("Give the number of Nodes you want to create: "))):
	coords= []
	res = ''.join(secrets.choice(string.ascii_uppercase) for i in range(N))
	for k in range(0,DIMENSIONS):
		coords.append(random.randint(-1000,1000))
	
	my_nodes.append(Node( coords, res))
		
		
	


x_sorted_nodes = sorted(my_nodes,key=lambda l:l.coords[0])
my_root, _ = createBST(x_sorted_nodes)



while(1):
	print("1.Insert\n2.Search\n3.Delete\n4.Range search\n5.Update\n6.Print Nodes\n7.exit")
	answer=int(input("Chose operation: "))

	print("-----------------------------------")

	if answer==1:
		coords= []
		for i in range(0,DIMENSIONS):
			coords.append(int(input("Give key for dimension "+ str(i)+": ")))
		my_root = insert(my_root,Node(coords, input("Give data for this node: ")) )



	elif answer==2:
		coords=[]
		for i in range(0,DIMENSIONS):
			coords.append(int(input("Give key for dimension "+str(i)+" to search: ")))
		print_nodes(search(my_root,coords))

	elif answer==3:
		coords= []
		for i in range(0,DIMENSIONS):
			coords.append(int(input("Give key for dimension "+str(i)+" to delete: ")))
		my_root = delete(my_root, coords)

	elif answer==4:
		range_coords= []
		for i in range(0,DIMENSIONS):
			left_bound=int(input("Give left bound for dimension "+str(i)+": "))
			right_bound=int(input("Give right bound for dimension "+str(i)+": "))
			range_coords.append([left_bound,right_bound])
		print_nodes(range_search(my_root,range_coords))
	
	elif answer==5:
		my_root = update(my_root)

	elif answer==6:
		range_coords= []
		for i in range(0,DIMENSIONS):
			range_coords.append([float("-inf"),float("inf")])
		print_nodes(range_search(my_root,range_coords))
		
	
	else:
		break

	print("-----------------------------------\n\n")
print_nodes(my_list)
check_range(my_list, my_range)
