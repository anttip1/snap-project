
#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

# The location of network:
FILE_PATH_1 = "../wiki-Vote.txt"  # 7 115 nodes
# FILE_PATH_2 = "../soc-Epinions1.txt"  # 75 879 nodes
# FILE_PATH_3 = "../gplus_combined.txt"  # 107 614 nodes
# FILE_PATH_4 = "../soc-pokec-relationships.txt"  # 1 632 803 nodes
# FILE_PATH_5 = "../soc-LiveJournal1.txt"  # 4 847 571 nodes

def import_data(file_path):
    assert os.path.exists(
        file_path), 'File {} could not be found'.format(event_fname)
    data = np.genfromtxt(
        file_path,
        delimiter='\t',
        comments='#'
    )
    return data

def get_dir_graph(data):
    dG = nx.DiGraph()
    dG.add_edges_from(data)
    return dG


def get_undir_graph(data):
    G = nx.Graph()
    G.add_edges_from(data)
    return G

def get_subgraph_nodes_and_edges(G, node_list):
    H = G.subgraph(node_list)
    nodes = H.nodes()
    edges = H.edges()
    return nodes, edges

if __name__ == "__main__":
    network_datas = os.listdir('network_data')
    print('network_datas', network_datas)
    for network_path in network_datas:
        data = import_data(network_path)
        
        dG = get_dir_graph(data)
        largest_strongly = max(nx.strongly_connected_components(dG), key=len)
        d_nodes, d_edges = get_subgraph_nodes_and_edges(dG, largest_strongly)

        G = get_undir_graph(data)
        largest_weakly = max(nx.connected_components(G), key=len)
        nodes, edges = get_subgraph_nodes_and_edges(G, largest_weakly)

    data = import_data(FILE_PATH_1)
    dG = get_dir_graph(data)
    largest_strongly = max(nx.strongly_connected_components(dG), key=len)
    

    print('\nLargest strongly connected')
    print('Nodes:', len(nodes))
    print('Edges:', len(edges))

    data = import_data(FILE_PATH_1)
    G = get_undir_graph(data)
    largest_weakly = max(nx.connected_components(G), key=len)
    H = G.subgraph(largest_weakly)
    nodes = H.nodes()
    edges = H.edges()

    print('\nLargest weakly connected:')
    print('Nodes:', len(nodes))
    print('Edges:', len(edges))
