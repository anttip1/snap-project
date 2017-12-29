#!usr/bin/env python

import numpy as np
import networkx as nx
from collections import Counter
import time


def main():
    networks = ["wiki-Vote.txt", "soc-Epinions1.txt", "gplus_combined.txt"]
    '''
    for network in networks:
        tic = time.clock()
        s_nodes, s_edges = lscc(network)
        toc = time.clock()
        s_time = toc - tic
        tic = time.clock()
        w_nodes, w_edges = lwcc(network)
        toc = time.clock()
        w_time = toc - tic
        print("Network: {}".format(network))
        print("LSCC nodes: {}, LSCC edges: {}. Running time: {}".format(s_nodes, s_edges, s_time))
        print("LWCC nodes: {}, LWCC edges: {}. Running time: {}".format(w_nodes, w_edges, w_time))
    '''

    analyze_graph("wiki-Vote.txt", True)
    analyze_graph("wiki-Vote.txt", False)



def lscc(filename):

    f = open(filename)
    line = f.readline()

    G = nx.DiGraph()

    while line:
        if not line.startswith("#"):
            nodes = line.split()
            if nodes:
                G.add_edge(nodes[0], nodes[1])
        line = f.readline()

    largest_strongly_connected_component = max(nx.strongly_connected_components(G), key=len)
    edge_count = 0

    f.seek(0) # reset the file back to start
    line = f.readline()

    while line:
        if not line.startswith("#"):      
            nodes = line.split()
            if nodes:
                if nodes[0] in largest_strongly_connected_component and nodes[1] in largest_strongly_connected_component:
                    edge_count += 1
        line = f.readline()

    f.close()


    return len(largest_strongly_connected_component), edge_count

def lwcc(filename):
    f = open(filename)
    line = f.readline()

    G = nx.Graph()

    while line:
        if not line.startswith("#"):
            nodes = line.split()
            if nodes:
                G.add_edge(nodes[0], nodes[1])
        line = f.readline()

    largest_weakly_connected_component = max(nx.connected_components(G), key=len)
    edge_count = 0

    f.seek(0) # reset the file back to start
    line = f.readline()

    while line:
        if not line.startswith("#"):
            nodes = line.split()
            if nodes:
                if nodes[0] in largest_weakly_connected_component and nodes[1] in largest_weakly_connected_component:
                    edge_count += 1
        line = f.readline()

    f.close()


    return len(largest_weakly_connected_component), edge_count

    



def largest_strongly_connected_component(filename):
    # This is only for directed graphs.

    data = np.genfromtxt(filename, delimiter="\t", comments="#", dtype=int)
    G = nx.DiGraph()
    G.add_edges_from(data)
    largest_strongly_connected_component = max(nx.strongly_connected_components(G), key=len)

    edge_count = 0
    for (node1, node2) in list(map(tuple, data)):
        if node1 in largest_strongly_connected_component and node2 in largest_strongly_connected_component:
            edge_count += 1

    #print("{}".format(filename))
    #print("\t{}\t{}".format("LSCC nodes", "LSCC edges"))
    #print("\t{}\t{}".format(len(largest_strongly_connected_component), edge_count))
    return len(largest_strongly_connected_component), edge_count

def largest_weakly_connected_component(filename):
    # This is only for undirected graphs.
    data = np.genfromtxt(filename, delimiter="\t", comments="#")
    G = nx.Graph()
    G.add_edges_from(data)
    largest_weakly_connected_component = max(nx.connected_components(G), key=len)

    edge_count = 0
    for (node1, node2) in list(map(tuple, data)):
        if node1 in largest_weakly_connected_component and node2 in largest_weakly_connected_component:
            edge_count += 1

    #print("{}".format(filename))
    #print("\t{}\t{}".format("LWCC nodes", "LWCC edges"))
    #print("\t{}\t{}".format(len(largest_weakly_connected_component), edge_count))
    return len(largest_weakly_connected_component), edge_count

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

    
    # Rather than gathering all lengths between node pairs, because the lengths are integers, we can just accumulate 
    # them on an dict. The dict key denotes the lenght and the value the count of that length in shortest_path_length 
    # dict. 
    length_counts = Counter()
    
    for node, other_nodes in nx.shortest_path_length(G):
        length_counts += Counter(other_nodes.values())

    
    # Take the 0 away, because it just denotes the nodes length to itself.
    del length_counts[0]

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
