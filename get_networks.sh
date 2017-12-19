### wiki-Vote: 7115 nodes:
echo Downloading the wiki-Vote network
wget http://snap.stanford.edu/data/wiki-Vote.txt.gz
### soc-Epinions1 75 879 nodes
echo Downloading the soc-Epinions1 network:
wget http://snap.stanford.edu/data/soc-Epinions1.txt.gz
### ego-Gplus: 107 614 nodes
echo Downloading the ego-Gplus network:
wget http://snap.stanford.edu/data/gplus_combined.txt.gz
### soc-Pokec: 1 632 803 nodes
echo Downloading the soc-Pokec networks:
wget http://snap.stanford.edu/data/soc-pokec-relationships.txt.gz
wget http://snap.stanford.edu/data/soc-pokec-profiles.txt.gz

## Unzip the files
echo Unzipping the files
gunzip wiki-Vote.txt.gz
gunzip soc-Epinions1.txt.gz
gunzip gplus_combined.txt.gz
gunzip soc-pokec-relationships.txt.gz
gunzip soc-pokec-profiles.txt.gz
