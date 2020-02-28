import codecs
import json
from typing import Tuple

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from pyquery import PyQuery as pq
import tarfile


def load_data(es: Elasticsearch) -> None:
    """
    This function loads data from the tarball "wiki-small.tar.gz"
    to the Elasticsearch cluster

    Parameters
    ----------
    es : Elasticsearch
        The Elasticsearch client

    Returns
    -------
    None
    """

    # Fill in the code here
    tar = tarfile.open("/workdir/wiki-small.tar.gz", "r:gz")
    all_members = tar.getnames()
    id = 1
    for member in all_members:
        html_file = tar.extractfile(member)
        if html_file is not None:
            content = parse_html(html_file.read())
            body = {
                "title": content[0],
                "body": content[1]
            }
            es.index(index="wikipedia", id=id, doc_type="_doc", body=body)
            id += 1
    tar.close()


def parse_html(html: str) -> Tuple[str, str]:
    """
    This function parses the html, strips the tags an return
    the title and the body of the html file.

    Parameters
    ----------
    html : str
        The HTML text

    Returns
    -------
    Tuple[str, str]
        A tuple of (title, body)
    """

    # Fill in the code here
    doc = pq(html)
    title = doc("title").text()
    body = doc("body").text()
    return str(title), str(body)


def create_wikipedia_index(ic: IndicesClient) -> None:
    """
    Add an index to Elasticsearch called 'wikipedia'

    Parameters
    ----------
    ic : IndicesClient
        The client to control Elasticsearch index settings

    Returns
    -------
    None
    """
    # Fill in the code here
    ic.create(index="wikipedia", body={
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "my_analyzer"},
                "body": {"type": "text", "analyzer": "my_analyzer", "search_analyzer": "my_analyzer"}
            }
        },
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["my_stops", "lowercase"]
                    }
                },
                "filter": {
                    "my_stops": {
                        "type": "stop",
                        "stopwords": "/usr/share/elasticsearch/config/stopwords.txt"
                    }
                }
            }
        }
    })
