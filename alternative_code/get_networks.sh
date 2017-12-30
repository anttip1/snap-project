### wiki-Vote: 7115 nodes:
if [ -e wiki-Vote.txt ]
then
	echo wiki-Vote.txt already exists\!
else
	echo Downloading the wiki-Vote network
	wget http://snap.stanford.edu/data/wiki-Vote.txt.gz
	echo Unzipping wiki-Vote.txt.gz
	gunzip wiki-Vote.txt.gz
	echo Done\!
fi

### soc-Epinions1 75 879 nodes
if [ -e soc-Epinions1.txt ]
then
	echo soc-Epinions1.txt already exitsts\!
else
	echo Downloading the soc-Epinions1 network:
	wget http://snap.stanford.edu/data/soc-Epinions1.txt.gz
	echo Unzipping soc-Epinions1.txt.gz
	gunzip soc-Epinions1.txt.gz
fi

### ego-Gplus: 107 614 nodes
if [ -e gplus_combined.txt ]
then
	echo gplus_combined.txt already exitsts\!
else
	echo Downloading the gplus_combined network:
	wget http://snap.stanford.edu/data/gplus_combined.txt.gz
	echo Unzipping gplus_combined.txt.gz
	gunzip gplus_combined.txt.gz
fi

### soc-Pokec: 1 632 803 nodes
if [ -e soc-pokec-relationships.txt ]
then
	echo soc-pokec-relationships.txt already exitsts\!
else
	echo Downloading the soc-pokec-relationships network:
	wget http://snap.stanford.edu/data/soc-pokec-relationships.txt.gz
	echo Unzipping soc-pokec-relationships.txt.gz
	gunzip soc-pokec-relationships.txt.gz
fi

