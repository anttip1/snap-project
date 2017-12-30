
#import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import timeit
import random
import matplotlib.pyplot as plt

### The location of network (not neccesary since the code looks for the files from network_data folder):
### ---> network_datas = os.listdir('network_data')
FILE_PATH_1 = "wiki-Vote.txt"  # 7 115 nodes
FILE_PATH_2 = "soc-Epinions1.txt"  # 75 879 nodes
FILE_PATH_3 = "gplus_combined.txt"  # 107 614 nodes
FILE_PATH_4 = "soc-pokec-relationships.txt"  # 1 632 803 nodes


def import_data(file_path):
    assert os.path.exists(
        file_path), 'File {} could not be found'.format(event_fname)
    if file_path is "gplus_combined.txt":
        data = np.genfromtxt(
            file_path,
            #delimiter='\t',
            delimiter=' ',
            comments='#'
        )
    else:
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


def get_random_pairs_path_lenghts(G, max_diameter, approx_node_count):
    #print('\nCalculatin approximations with random pairs ({} node pairs)...'.format(approx_node_count))
    #start_time = timeit.default_timer()
    node_1 = random.choice(G.nodes())
    #print('Random nodes time:', timeit.default_timer() - start_time)

    #start_time = timeit.default_timer()
    keyDict = list(range(max_diameter + 1))
    path_lengt_dict = (dict([(key, 0) for key in keyDict]))
    for i in range(approx_node_count): 
      node_1 = random.choice(G.nodes())
      node_2 = random.choice(G.nodes())
      while node_1 == node_2:
        node_2 = random.choice(G.nodes())
      shortest_path_length = nx.shortest_path(
          G, source=node_1, target=node_2)
      distance = len(shortest_path_length) - 1
      path_lengt_dict[distance] = path_lengt_dict[distance] + 1
    #print('done.')
    #print('Time:', timeit.default_timer() - start_time)
    return path_lengt_dict


def get_bfs_path_lenghts(G, max_diameter, approx_node_count):
    #print('\nCalculatin approximations with a complete breadth-first search (BFS) for each source ({} node sources)...'.format(approx_node_count))
    #start_time = timeit.default_timer()
    node_1 = random.choice(G.nodes())
    #print('Random nodes time:', timeit.default_timer() - start_time)

    #start_time = timeit.default_timer()
    keyDict = list(range(max_diameter + 1))
    path_lengt_dict = (dict([(key, 0) for key in keyDict]))
    visited_nodes = []
    node_1 = random.choice(G.nodes())
    for i in range(approx_node_count):
      while node_1 in visited_nodes:
          node_1 = random.choice(G.nodes())
      visited_nodes.append(node_1)
      shortest_path_lengths = nx.shortest_path(
          G, source=node_1)
      for distance in shortest_path_lengths.values():
          path_lengt_dict[len(distance) -
                          1] = path_lengt_dict[len(distance) - 1] + 1
    for_visited_nodes = list(visited_nodes)
    for source in for_visited_nodes:
        for target in visited_nodes:
            shortest_path_length = nx.shortest_path(
                G, source=source, target=target)
            path_lengt_dict[len(shortest_path_length) -
                            1] = path_lengt_dict[len(shortest_path_length) - 1] - 1
        visited_nodes.pop(0)
    #print('done.')
    #print('Time:', timeit.default_timer() - start_time)
    return path_lengt_dict


def get_values(path_lengt_dict):
    # 1. median distance
    amount_of_distances = sum(path_lengt_dict.values())

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
            break

    # 2. mean distance
    distance_sum = 0
    distance_count = 0
    for distance, count in path_lengt_dict.items():
        distance_sum += distance * count
        distance_count += count
    mean_distance = distance_sum / distance_count

    # 3. diameter
    for distance, count in sorted(path_lengt_dict.items()):
        if count > 0:
            diameter = distance

    # 4. effective diameter
    # Effective diameter is the φ-quantile of set of n items, with 0 ≤ φ ≤ 1, is obtained by sorting the items in increasing order and returning the [φn] - th item in that order
    eff_diameter = amount_of_distances * 0.9 - ((amount_of_distances * 0.9) % 1)
    for distance, count in sorted(path_lengt_dict.items()):
        eff_diameter -= count
        if eff_diameter <= 0:
            eff_diameter = distance
            break

    return median_distance, mean_distance, diameter, eff_diameter



if __name__ == "__main__":
    #network_datas = os.listdir('network_data')
    network_datas = [FILE_PATH_1, FILE_PATH_2]
    print('network_data:', network_datas)
    
    for network_path in network_datas:
        if network_path == '.DS_Store':
            pass
        else:
            print('\nCalculating strongest connected component for {}...'.format(
                network_path))
            file_path = 'network_data/{}'.format(network_path)

            start_time = timeit.default_timer()
            data = import_data(file_path)
            print('Import time:', timeit.default_timer() - start_time)

            start_time = timeit.default_timer()
            dG = get_dir_graph(data)
            print('Directed graph time:', timeit.default_timer() - start_time)

            start_time = timeit.default_timer()
            largest_strongly = max(nx.strongly_connected_components(dG), key=len)
            print('Largest strongly component time:', timeit.default_timer() - start_time)

            dG, d_nodes, d_edges = get_subgraph_and_nodes_and_edges(
                dG, largest_strongly)
            print('done.')

            ###print('\nCalculating largest connected component...')
            # G = get_undir_graph(data)
            # largest_weakly = max(nx.connected_components(G), key=len)
            # G, nodes, edges = get_subgraph_and_nodes_and_edges(G, largest_weakly)
            # dG = G
            # d_nodes = nodes
            # d_edges = edges
            ###print('done.')

            approx_node_count = 100
            #### Takes less than 15 sec. with 'wiki-Vote.txt'
            print('\nLargest strongly connected component for {}:'.format(network_path))
            print('Nodes:', len(d_nodes))
            print('Edges:', len(d_edges))
            
            ## 1)
            start_time = timeit.default_timer()
            path_lengt_dict = get_bfs_path_lenghts(
                dG, 25, approx_node_count)
            print('BFS time:',
                      timeit.default_timer() - start_time)
            print('path_lengt_dict:', path_lengt_dict)
            median_distance, mean_distance, diameter, eff_diameter = get_values(path_lengt_dict)
            print('1. median distance:', median_distance)
            print('2. mean distance:', mean_distance)
            print('3. diameter', diameter)
            print('4. effective diameter:', eff_diameter)

            ## 2)
            start_time = timeit.default_timer()
            path_lengt_dict = get_random_pairs_path_lenghts(
                dG, 25, approx_node_count)
            print('Random pairs time:',
                  timeit.default_timer() - start_time)
            print('path_lengt_dict:', path_lengt_dict)
            median_distance, mean_distance, diameter, eff_diameter = get_values(path_lengt_dict)
            print('1. median distance:', median_distance)
            print('2. mean distance:', mean_distance)
            print('3. diameter', diameter)
            print('4. effective diameter:', eff_diameter)

            ### Plots

            rand_pair_median = []
            rand_pair_mean = []
            rand_pair_diameter = []
            rand_pair_eff = []

            bfs_median = []
            bfs_mean = []
            bfs_diameter = []
            bfs_eff = []

            count_rand_pair_median = []
            count_rand_pair_mean = []
            count_rand_pair_diameter = []
            count_rand_pair_eff = []

            count_bfs_median = []
            count_bfs_mean = []
            count_bfs_diameter = []
            count_bfs_eff = []

            node_count_for_plot = []
            node_count_for_mean = []

            max_diameter = 25
            node_count_list = [2,5,9,30,60,90]
            repatitions = 10
            for node_count in node_count_list:
                rand_pair_mean_median = []
                rand_pair_mean_mean = []
                rand_pair_mean_diameter = []
                rand_pair_mean_eff = []
                
                bfs_mean_median = []
                bfs_mean_mean = []
                bfs_mean_diameter = []
                bfs_mean_eff = []
                for i in range(repatitions):
                    #print('{}.{}'.format(node_count, i+1))
                    ## Random pair:
                    path_lengt_dict = get_random_pairs_path_lenghts(
                        dG, max_diameter, node_count)
                    median_distance, mean_distance, diameter, eff_diameter = get_values(
                        path_lengt_dict)
                    rand_pair_median.append(median_distance)
                    rand_pair_mean.append(mean_distance)
                    rand_pair_diameter.append(diameter)
                    rand_pair_eff.append(eff_diameter)

                    rand_pair_mean_median.append(median_distance)
                    rand_pair_mean_mean.append(mean_distance)
                    rand_pair_mean_diameter.append(diameter)
                    rand_pair_mean_eff.append(eff_diameter)

                    ## BFS:
                    path_lengt_dict = get_bfs_path_lenghts(dG, max_diameter, node_count)
                    median_distance, mean_distance, diameter, eff_diameter = get_values(path_lengt_dict)
                    bfs_median.append(median_distance)
                    bfs_mean.append(mean_distance)
                    bfs_diameter.append(diameter)
                    bfs_eff.append(eff_diameter)

                    bfs_mean_median.append(median_distance)
                    bfs_mean_mean.append(mean_distance)
                    bfs_mean_diameter.append(diameter)
                    bfs_mean_eff.append(eff_diameter)

                    node_count_for_plot.append(node_count)

                count_rand_pair_median.append(np.mean(rand_pair_mean_median))
                count_rand_pair_mean.append(np.mean(rand_pair_mean_mean))
                count_rand_pair_diameter.append(np.mean(rand_pair_mean_diameter))
                count_rand_pair_eff.append(np.mean(rand_pair_mean_eff))
                
                count_bfs_median.append(np.mean(bfs_mean_median))
                count_bfs_mean.append(np.mean(bfs_mean_mean))
                count_bfs_diameter.append(np.mean(bfs_mean_diameter))
                count_bfs_eff.append(np.mean(bfs_mean_eff))

                node_count_for_mean.append(node_count)
            
            rand_pair_label = 'Random pair'
            mean_rand_pair_label = 'Mean of random pair bins'
            bfs_label = 'BFS'
            mean_bfs_label = 'Mean of BFS bins'
            alpha = 0.3

            plt.figure(1)
            plt.subplot(221)
            plt.scatter(node_count_for_plot, rand_pair_median, alpha=alpha, label=rand_pair_label)
            plt.plot(node_count_for_mean, count_rand_pair_median, label=mean_rand_pair_label)
            plt.scatter(node_count_for_plot, bfs_median,alpha=alpha, label=bfs_label)
            plt.plot(node_count_for_mean, count_bfs_median, label=mean_bfs_label)
            plt.title('Median edge lenght')
            plt.subplot(222)
            plt.scatter(node_count_for_plot, rand_pair_mean,alpha=alpha, label=rand_pair_label)
            plt.plot(node_count_for_mean, count_rand_pair_mean, label=mean_rand_pair_label)
            plt.scatter(node_count_for_plot, bfs_mean,alpha=alpha, label=bfs_label)
            plt.plot(node_count_for_mean, count_bfs_mean, label=mean_bfs_label)
            plt.title('Mean edge lenght')
            plt.subplot(223)
            plt.scatter(node_count_for_plot, rand_pair_diameter,  alpha=alpha, label=rand_pair_label)
            plt.plot(node_count_for_mean, count_rand_pair_diameter, label=mean_rand_pair_label)
            plt.scatter(node_count_for_plot, bfs_diameter,
                        alpha=alpha, label=bfs_label)
            plt.plot(node_count_for_mean, count_bfs_diameter, label=mean_bfs_label)
            plt.title('Diameter')
            plt.subplot(224)
            plt.scatter(node_count_for_plot, rand_pair_eff,  alpha=alpha, label=rand_pair_label)
            plt.plot(node_count_for_mean, count_rand_pair_eff, label=mean_rand_pair_label)
            plt.scatter(node_count_for_plot, bfs_eff,
                        alpha=alpha, label=bfs_label)
            plt.plot(node_count_for_mean, count_bfs_eff, label=mean_bfs_label)
            plt.title('Effective diameter')
            plt.legend()
            plt.suptitle('Network approximation statistics as a function of sample size (data:{})'.format(
                network_path), fontsize=16)
            plt.tight_layout()
            plt.show()


        #### Takes forever... (less than 5 min) with 'wiki-Vote.txt'
            # print('\nLargest connected component:')
            # print('Nodes:', len(nodes))
            # print('Edges:', len(edges))
            # get_path_lenghts(G, 10)
