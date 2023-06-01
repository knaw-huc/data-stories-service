import json

from elasticsearch import Elasticsearch
import math

class Index:
    def __init__(self, config):
        self.config = config
        self.es = Elasticsearch([{"host": self.config["url"], "port": self.config["port"]}])
        self.client = Elasticsearch()

    def no_case(self, str_in):
        str = str_in.strip()
        ret_str = ""
        if (str != ""):
            for char in str:
                ret_str = ret_str + "[" + char.upper() + char.lower() + "]"
        return ret_str + ".*"


    def get_facet(self, field, amount):
        ret_array = []
        response = self.client.search(
            index="ds",
            body=
                {
                    "size": 0,
                    "aggs": {
                        "names": {
                            "terms": {
                                "field": field,
                                "size": amount,
                                "order": {
                                    "_count": "desc"
                                }
                            },
                            "aggs": {
                                "byHash": {
                                    "terms": {
                                        "field": "hash"
                                    }
                                }
                            }
                        }
                    }
                }
        )
        for hits in response["aggregations"]["names"]["buckets"]:
            buffer = {"key": hits["key"], "doc_count": hits["doc_count"]}
            ret_array.append(buffer)
        return ret_array

    def get_filter_facet(self, field, amount, facet_filter):
        ret_array = []
        response = self.client.search(
            index="ds",
            body=
            {
                "query": {
                    "regexp": {
                        field : self.no_case(facet_filter)
                    }
                },
                "size": 0,
                "aggs": {
                    "names": {
                        "terms": {
                            "field": field,
                            "size": amount,
                            "order": {
                                "_count": "desc"
                            }
                        }
                    }
                }
            }
        )
        for hits in response["aggregations"]["names"]["buckets"]:
            buffer = {"key": hits["key"], "doc_count": hits["doc_count"]}
            ret_array.append(buffer)
        return ret_array



    def browse(self):

        response = self.client.search(
            index="ds",
            body={ "query": {
            "match_all": {}},
            "size": 10,
            "from": 0,
            "_source": ["title", "filename", "store", "owner", "group", "created", "modified"],
            }
        )
        ret_array = {"amount" : response["hits"]["total"]["value"] ,"items": []}
        for item in response["hits"]["hits"]:
            ret_array["items"].append(item["_source"])
        return ret_array

    def add_to_index(self, json_struc):
        pass







