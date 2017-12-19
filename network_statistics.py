#!usr/bin/env python

import numpy as np
import networkx as nx

def main():
	analyze_wiki_vote()


def analyze_wiki_vote():
	data = np.genfromtxt("wiki-Vote.txt", delimiter="\t", comments="#")
	G = nx.DiGraph()
	G.add_edges_from(data)
	print(G.graph)




if __name__ == '__main__':
	main()
