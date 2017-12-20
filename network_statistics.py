#!usr/bin/env python

import numpy as np
import networkx as nx
from collections import Counter
import time

def main():
    analyze_wiki_vote()


def analyze_wiki_vote():

    tic = time.clock()

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
    
    # Rather than gathering all lengths between node pairs, because the lengths are integers, we can just accumulate 
    # them on an dict. The dict key denotes the lenght and the value the count of that length in shortest_path_length 
    # dict. 
    length_counts = Counter()

    for node, other_nodes in nx.shortest_path_length(G):
        length_counts += Counter(other_nodes.values())

    # Take the 0 away, because it just denotes the nodes length to itself.
    del length_counts[0]
    print(length_counts)

    length_sum = 0
    max_length = max(length_counts, key=int)
    count_of_pairs = 0

    for length in length_counts:
        length_sum += length * length_counts[length]
        count_of_pairs += length_counts[length]

    mean_distance = length_sum / count_of_pairs
    diameter = max_length
    median_distance = None
    effective_diameter = None

    middle_point = count_of_pairs / 2
    cumulative_count = 0
    for length in sorted(length_counts):
        if cumulative_count <= middle_point and cumulative_count + length_counts[length] > middle_point:
            median_distance = length
            break
        cumulative_count += length_counts[length]

    cumulative_count = 0
    for length in sorted(length_counts):
        if cumulative_count / count_of_pairs >= 0.9:
            effective_diameter = length
            break
        cumulative_count += length_counts[length]

    print("1. Median distance: {}".format(median_distance))
    print("2. Mean distance: {}".format(mean_distance))
    print("3. Diameter: {}".format(diameter))
    print("4. Effective diameter: {}".format(effective_diameter))

    toc = time.clock()

    print("Processing time: {}s".format(toc-tic))


    # This method, although more readable, is really slow compared to the above version.
    # It prints out the values for edges and nodes in LSCC
    #LSCC_graph = max(nx.strongly_connected_component_subgraphs(G), key=len)
    #print(len(LSCC_graph))
    #print(len(LSCC_graph.nodes()))
    #print(len(LSCC_graph.edges()))





if __name__ == '__main__':
    main()
