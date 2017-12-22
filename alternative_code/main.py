
#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import timeit

### The location of network (not neccesary since the code looks for the files from network_data folder):
### ---> network_datas = os.listdir('network_data')
# FILE_PATH_1 = "../wiki-Vote.txt"  # 7 115 nodes
# FILE_PATH_2 = "../soc-Epinions1.txt"  # 75 879 nodes
# FILE_PATH_3 = "../gplus_combined.txt"  # 107 614 nodes
# FILE_PATH_4 = "../soc-pokec-relationships.txt"  # 1 632 803 nodes


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


def get_subgraph_and_nodes_and_edges(G, node_list):
    H = G.subgraph(node_list)
    nodes = H.nodes()
    edges = H.edges()
    return H, nodes, edges

def get_path_lenghts(G, diameter):
    print('\nCalculatin shortest path lenghts for each node pair...')
    shortest_path_length = nx.shortest_path_length(G)
    keyDict = list(range(diameter + 1))
    path_lengt_dict = (dict([(key, 0) for key in keyDict]))
    for nodes_distances in shortest_path_length.values():
        for distance in nodes_distances.values():
            path_lengt_dict[distance] = path_lengt_dict[distance] + 1
    print('done.')
    return path_lengt_dict

if __name__ == "__main__":
    network_datas = os.listdir('network_data')
    print('network_data:', network_datas)
    
    for network_path in network_datas:
        file_path = 'network_data/{}'.format(network_path)
        data = import_data(file_path)
        
        print('\nCalculating strongest connected component...')
        dG = get_dir_graph(data)
        largest_strongly = max(nx.strongly_connected_components(dG), key=len)
        dG, d_nodes, d_edges = get_subgraph_and_nodes_and_edges(
            dG, largest_strongly)
        d_diameter = nx.diameter(dG)
        print('done.')

        print('\nCalculating largest connected component...')
        G = get_undir_graph(data)
        largest_weakly = max(nx.connected_components(G), key=len)
        G, nodes, edges = get_subgraph_and_nodes_and_edges(G, largest_weakly)
        #### Takes forever... (less than 7 min)
        #diameter = nx.diameter(G)
        print('done.')
        
#### Takes less than 15 sec.
    print('\nLargest strongly connected:')
    print('Nodes:', len(d_nodes))
    print('Edges:', len(d_edges))
    print('Diameter', d_diameter)
    get_path_lenghts(dG, d_diameter)

#### Takes forever... (less than 5 min)
    print('\nLargest connected component:')
    print('Nodes:', len(nodes))
    print('Edges:', len(edges))
    get_path_lenghts(G, 10)
