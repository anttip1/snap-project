
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

def get_path_lenghts(G, max_diameter):
    start_time = timeit.default_timer()
    print('\nCalculatin shortest path lenghts for each node pair...')
    shortest_path_length = nx.shortest_path_length(G)
    keyDict = list(range(max_diameter + 1))
    path_lengt_dict = (dict([(key, 0) for key in keyDict]))
    for nodes_distances in shortest_path_length.values():
        for distance in nodes_distances.values():
            path_lengt_dict[distance] = path_lengt_dict[distance] + 1
    print('done.')
    print('Time:', timeit.default_timer() - start_time)
    return path_lengt_dict


def get_values(path_lengt_dict):
    nodes = path_lengt_dict[0]
    del path_lengt_dict[0]

    # 1. median distance
    amount_of_distances = sum(path_lengt_dict.values())
    if ((nodes - 1) * nodes) != amount_of_distances:
        print('Something is wrong. There is {} nodes and only {} distances!?!..'.format(
            nodes, amount_of_distances))

    median_count_1 = amount_of_distances / 2 - ((amount_of_distances / 2) % 1)
    median_count_2 = amount_of_distances / 2 + ((amount_of_distances / 2) % 1)
    for distance, count in sorted(path_lengt_dict.items()):
        median_count_1 -= count
        median_count_2 -= count
        if median_count_1 <= 0:
            median_1 = distance
        if median_count_2 <= 0:
            median_2 = distance
            median_distance = (median_1 + median_2) / 2

    # 2. mean distance
    distance_sum = 0
    distance_count = 0
    for distance, count in path_lengt_dict.items():
        distance_sum += distance * count
        distance_count += count
    mean_distance = distance_sum / count

    # 3. diameter
    for distance, count in sorted(path_lengt_dict.items()):
        if count > 0:
            diameter = distance

    # 4. effective diameter
    # Effective diameter is the φ-quantile of set of n items, with 0 ≤ φ ≤ 1, is obtained by sorting the items in increasing order and returning the [φn] - th item in that order
    eff_diameter = amount_of_distances * \
        0.9 - ((amount_of_distances * 0.9) % 1)
    for distance, count in sorted(path_lengt_dict.items()):
        eff_diameter -= count
        if eff_diameter <= 0:
            eff_diameter = distance

    return median_distance, mean_distance, diameter, eff_diameter

if __name__ == "__main__":
    network_datas = os.listdir('network_data')
    print('network_data:', network_datas)
    
    for network_path in network_datas:
        if 'wiki-Vote.txt' is not network_path:
            file_path = 'network_data/{}'.format(network_path)
            data = import_data(file_path)
            
            print('\nCalculating strongest connected component...')
            dG = get_dir_graph(data)
            largest_strongly = max(nx.strongly_connected_components(dG), key=len)
            dG, d_nodes, d_edges = get_subgraph_and_nodes_and_edges(
                dG, largest_strongly)
            print('done.')

            #print('\nCalculating largest connected component...')
            # G = get_undir_graph(data)
            # largest_weakly = max(nx.connected_components(G), key=len)
            # G, nodes, edges = get_subgraph_and_nodes_and_edges(G, largest_weakly)
            #print('done.')
        
    #### Takes less than 15 sec.
        print('\nLargest strongly connected component for {}:'.format(network_path))
        print('Nodes:', len(d_nodes))
        print('Edges:', len(d_edges))
        path_lengt_dict = get_path_lenghts(dG, 30)
        print('path_lengt_dict:', path_lengt_dict)
        median_distance, mean_distance, diameter, eff_diameter = get_values(path_lengt_dict)
        print('1. median distance:', median_distance)
        print('2. mean distance:', mean_distance)
        print('3. diameter', diameter)
        print('4. effective diameter:', eff_diameter)

    #### Takes forever... (less than 5 min)
        # print('\nLargest connected component:')
        # print('Nodes:', len(nodes))
        # print('Edges:', len(edges))
        # get_path_lenghts(G, 10)
