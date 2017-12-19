#!usr/bin/env python

import numpy as np

def main():
	analyze_wiki_vote()


def analyze_wiki_vote():
	data = np.genfromtxt("wiki-Vote.txt", delimiter="\t", comments="#")
	print(data)




if __name__ == '__main__':
	main()
