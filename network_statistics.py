#!usr/bin/env python

import numpy as np
import networkx as nx
from collections import Counter
import time

from multiprocessing import Pool


def main():
    networks = ["wiki-Vote.txt", "soc-Epinions1.txt", "gplus_combined.txt"]


    analyze_graph("wiki-Vote.txt", True)
    analyze_graph("wiki-Vote.txt", False)

    analyze_graph("soc-Epinions1.txt", True)
    analyze_graph("soc-Epinions1.txt", False)
    
    analyze_graph("gplus_combined.txt", True)
    analyze_graph("gplus_combined.txt", False)


    
def analyze_graph(filename, directed=True):

    tic = time.clock()
    G = nx.DiGraph() if directed else nx.Graph()

    f = open(filename)
    line = f.readline()
    
    while line:
        if not line.startswith("#"):
            nodes = line.split()
            if nodes:
                G.add_edge(nodes[0], nodes[1])
        line = f.readline()

    lcc = max(nx.strongly_connected_component_subgraphs(G), key=len) if directed else max(nx.connected_component_subgraphs(G), key=len)

    f.seek(0) # reset the file back to start
    line = f.readline()

    lcc_nodes = lcc.nodes()
    edge_count = 0

    while line:
        if not line.startswith("#"):      
            nodes = line.split()
            if nodes:
                if nodes[0] in lcc_nodes and nodes[1] in lcc_nodes:
                    edge_count += 1
        line = f.readline()

    f.close()

    if directed:
        print("LSCC nodes: {}, LSCC edges: {}".format(len(lcc_nodes), edge_count))

    else:
        print("LWCC nodes: {}, LWCC edges: {}".format(len(lcc_nodes), edge_count))

    # Rather than gathering all lengths between node pairs, because the lengths are integers, we can just accumulate 
    # them on an dict. The dict key denotes the lenght and the value the count of that length in shortest_path_length 
    # dict. 

    #largest_strongly_connected_component = max(nx.strongly_connected_component_subgraphs(G), key=len)
    
    length_counts = Counter()
    
    for node, other_nodes in nx.shortest_path_length(lcc):
        length_counts += Counter(other_nodes.values())

    print(length_counts)
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

    print("network: {}".format(filename))
    if directed:
        print("Directed graph:")
    else:
        print("Undirected graph")

    print("1. Median distance: {}".format(median_distance))
    print("2. Mean distance: {}".format(mean_distance))
    print("3. Diameter: {}".format(diameter))
    print("4. Effective diameter: {}".format(effective_diameter))

    toc = time.clock()

    print("Processing time: {}s".format(toc-tic))




if __name__ == '__main__':
    main()
