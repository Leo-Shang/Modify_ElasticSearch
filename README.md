# Modify_ElasticSearch

## Note

Elasticsearch is a distributed search and analytics engine and provides real-time search and analytics for all types of data. This project is some modification towards the Elasticsearch library in Python. Due to the concern about the size of Elasticsearch library, this repository only includes the modification files. There is an docker image containing Elasticsearch and the wiki data (zip folder). Therefore, there is no need for preparing Elasticsearch source code.

## Environment

	1. Install Python3
	2. Install Docker

## Instructions to Run

	1. Clone this repository
	2. docker run -it --rm -v $PWD/src:/workdir/src -v $PWD/src/stopwords.txt:/usr/share/elasticsearch/config/stopwords.txt wooya/cmpt456a4 q1.py
	3. docker run -it --rm -v $PWD/src:/workdir/src -v $PWD/src/stopwords.txt:/usr/share/elasticsearch/config/stopwords.txt wooya/cmpt456a4 q2.py
	4. docker run -it --rm -v $PWD/src:/workdir/src -v $PWD/src/stopwords.txt:/usr/share/elasticsearch/config/stopwords.txt wooya/cmpt456a4 q3.py
