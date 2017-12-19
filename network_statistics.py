#!usr/bin/env python

import numpy as np
import networkx as nx

def main():
	analyze_wiki_vote()


def analyze_wiki_vote():
	data = np.genfromtxt("wiki-Vote.txt", delimiter="\t", comments="#")
	G = nx.DiGraph()
	G.add_edges_from(data)
	largest_strongly_connected_component = max(nx.strongly_connected_components(G), key=len)
		
	edge_count = 0
	for (node1, node2) in list(map(tuple, data)):
		if node1 in largest_strongly_connected_component and node2 in largest_strongly_connected_component:
			edge_count += 1
	
	print("wiki-Vote.txt")

	print("Number of nodes in wiki-Vote.txt: {}".format(len(G.nodes())))
	print("Number of edges in wiki-Vote.txt: {}".format(len(G.edges())))

	print("Number of nodes in LSCC: {}".format(len(largest_strongly_connected_component)))
	print("Number of edges in LSCC: {}".format(edge_count))


	shortest_path_lengths = []
	shortest_path_lengths_sum = 0
	number_of_values = 0
	max_value = 0
	for key, value in nx.shortest_path_length(G):
		lengths = value.values()
		#shortest_path_lengths.append(lengths)
		number_of_values += len(lengths)
		if max(lengths) > max_value: max_value = max(lengths)
		shortest_path_lengths_sum += sum(lengths)

	mean_distance = shortest_path_lengths_sum / number_of_values
	median_distance = None
	diameter = max_value
	effective_diameter = None
	

	median_distance = None
	effective_diameter = None





	print("1. Median distance: {}".format(median_distance))
	print("2. Mean distance: {}".format(mean_distance))
	print("3. Diameter: {}".format(diameter))
	print("4. Effective diameter: {}".format(effective_diameter))



	# This method, although more readable, is really slow compared to the above version.
	# It prints out the values for edges and nodes in LSCC
	#LSCC_graph = max(nx.strongly_connected_component_subgraphs(G), key=len)
	#print(len(LSCC_graph))
	#print(len(LSCC_graph.nodes()))
	#print(len(LSCC_graph.edges()))
	




if __name__ == '__main__':
	main()
