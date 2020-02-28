"""
Q1: Create index and load data
Please fill in the missing content in each function.
"""

import assignment4 as a4
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


def main():
    """
    The main function, do not change any code here
    """

    es = Elasticsearch()
    ic = IndicesClient(es)
    a4.create_wikipedia_index(ic)
    a4.load_data(es)

    print("The top ranked title:", search_and_rank(es))
    add_synonyms_to_index(ic)
    print("The top ranked title:", search_and_rank(es))
    print(how_does_rank_work())


def search_and_rank(es: Elasticsearch) -> str:
    """
    Based on the search in Q2, rank the documents by the terms "BC", "WA" and "AB"
    in the document body.
    Return the **title** of the top result.

    Parameters
    ----------
    es : Elasticsearch
        The Elasticsearch client

    Returns
    -------
    str
        The title of the top ranked document
    """

    # Fill in the code

    res = es.search(index="wikipedia", body={
        "query": {
            "bool": {
                'must': {
                    'bool': {
                        'should': [
                            {'match': {'body': 'lake'}},
                            {'match': {'body': 'tour'}},
                        ],
                    }
                },
                "should": [
                    {'match': {'body': {'query': 'BC', 'boost': 2}}},
                    {'match': {'body': {'query': 'AB', 'boost': 1}}},
                    {'match': {'body': {'query': 'WA', 'boost': 1}}}
                ],
                "must_not": {
                    "match_phrase": {
                        "body": "Please improve this article if you can."
                    }
                }
            }
        }
    })
    return res['hits']['hits'][0]['_source']['title']


def add_synonyms_to_index(ic: IndicesClient) -> None:
    """
    Modify the index setting, add synonym mappings for "BC" => "British Columbia",
    "WA" => "Washington" and "AB" => "Alberta"

    Parameters
    ----------
    ic : IndicesClient
        The client for control index settings in Elasticsearch

    Returns
    -------
    None
    """

    # Fill in the code
    ic.close(index="wikipedia")
    ic.put_settings(index="wikipedia", body={
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["my_stops", "lowercase", "my_synonyms"]
                    }
                },
                "filter": {
                    "my_stops": {
                        "type": "stop",
                        "stopwords": "/usr/share/elasticsearch/config/stopwords.txt"
                    },
                    "my_synonyms": {
                        "type": "synonym",
                        "synonyms": ["BC => British Columbia", "AB => Alberta", "WA => Washington"]
                    }
                }
            }
        }
    })
    ic.open(index="wikipedia")


def how_does_rank_work() -> str:
    """
    Please write the answer of the question:
    'how does rank work?' here, returning it as a str.

    Returns
    -------
    str, the answer
    """
    # Fill in the answer here
    string = "Ranking is done through ranking the score of each document. Each document is assigned a score by the searching function" \
             ", then rank the document in the score descending order. In the search query above, it has a subquery that boost the " \
             "score of the documents whose body containing British Columbia by weight of 2; boost the document whose body containing Alberta and Washington by " \
             "weight of 1. So they ranked higher because we modified their document score. \nRemember in Q3.1 we have created alias " \
             "between BC and British Columbia; AB and Alberta; and WA and Washington. Therefore, in this question, boosting the weight of " \
             "BC is the same as that of British Columbia."
    return string


if __name__ == "__main__":
    main()
