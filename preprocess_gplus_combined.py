import numpy as np


data = np.genfromtxt("gplus_combined.txt", delimiter="\t", comments="#", dtype=str)
output = open("gplus_combined_mapped.txt", "w")

for (node1, node2) in data:
	print("")

	

print(list_of_distinct_elements)