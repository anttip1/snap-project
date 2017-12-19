# snap-project

# Get the networks automatically via script:
## give get_networks.sh execution rights:
* chmod +x get_networks.sh
## Run the script
* ./get_networks.sh

# OR download the networks manually:

## Get the networks:

### wiki-Vote: 7115 nodes:
* wget http://snap.stanford.edu/data/wiki-Vote.txt.gz
### soc-Epinions1 75 879 nodes
* wget http://snap.stanford.edu/data/soc-Epinions1.txt.gz
### ego-Gplus: 107 614 nodes
* wget http://snap.stanford.edu/data/gplus_combined.txt.gz
### soc-Pokec: 1 632 803 nodes
* wget http://snap.stanford.edu/data/soc-pokec-relationships.txt.gz
* wget http://snap.stanford.edu/data/soc-pokec-profiles.txt.gz

## Unzip the files
* gunzip wiki-Vote.txt.gz
* gunzip soc-Epinions1.txt.gz
* gunzip gplus_combined.txt.gz
* gunzip soc-pokec-relationships.txt.gz
* gunzip soc-pokec-profiles.txt.gz


