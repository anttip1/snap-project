# snap-project

## Get the networks automatically via script:

### give get_networks.sh execution rights:

* chmod +x get_networks.sh
  ### Run the script
* ./get_networks.sh

### Get the networks:

#### wiki-Vote: 7115 nodes:

* wget http://snap.stanford.edu/data/wiki-Vote.txt.gz
  #### soc-Epinions1 75 879 nodes
* wget http://snap.stanford.edu/data/soc-Epinions1.txt.gz
  #### ego-Gplus: 107 614 nodes
* wget http://snap.stanford.edu/data/gplus_combined.txt.gz
  #### soc-Pokec: 1 632 803 nodes
* wget http://snap.stanford.edu/data/soc-pokec-relationships.txt.gz

### Unzip the files

* gunzip wiki-Vote.txt.gz
* gunzip soc-Epinions1.txt.gz
* gunzip gplus_combined.txt.gz
* gunzip soc-pokec-relationships.txt.gz

## Install python dependencies:

* Create a new virtualenvironment:

- python3 -m venv /path/to/virtualenv/snap-project

* Activate that virtualenvironment:

- source /path/to/virtualenv/snap-project/bin/activate

* Install the python packages:

- pip install -r requirements.txt

## Run the main.py and approximation.py

* Make sure that the networks (wiki-Vote.txt and soc-Epinions1.txt) are in the same folder with main.py and approximation.py
