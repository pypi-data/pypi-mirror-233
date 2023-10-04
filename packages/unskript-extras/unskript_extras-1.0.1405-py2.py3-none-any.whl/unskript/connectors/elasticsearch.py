##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import requests
import json

from typing import Any
from elasticsearch import Elasticsearch
from pydantic import ValidationError

from unskript.connectors.schema.elasticsearch import ElasticSearchSchema
from unskript.connectors.interface import ConnectorInterface
from subprocess import PIPE, run


class ElasticSearchConnector(ConnectorInterface):
    def __init__(self):
        self.host = None
        self.api_key = None
        self.verify_certs = False

    def web_request(self, path: str, method: str, data: dict):
        es_url = self.host + path
        es_header = {
            "Authorization": "ApiKey "  + self.api_key,
            "Content-Type" : "application/json"
            }
        if method in ["GET", "DELETE"]:
            response = requests.request(method=method,
                                        url=es_url,
                                        headers=es_header,
                                        verify=self.verify_certs)
        elif method is "PUT":
            # Data cannot be empty if we are using PUT method
            if len(data) == 0:
                raise Exception("For PUT Method, data cannot be empty")

            response = requests.request(method=method,
                                        url=es_url,
                                        headers=es_header,
                                        verify=self.verify_certs,
                                        data=json.dumps(data))
        else:
            raise Exception(f"Method {method} Not supported")


        # return response
        try:
            result = response.json()
        except:
            result = response.text

        return result


    def get_handle(self, data) -> Any:
        try:
            esCredential = ElasticSearchSchema(**data)
        except ValidationError as e:
            raise e
        # store credential data
        self.host = esCredential.host
        self.api_key = esCredential.api_key
        self.verify_certs = esCredential.verify_certs

        esHandle = Elasticsearch(hosts=esCredential.host,
                            api_key=esCredential.api_key,
                            verify_certs=esCredential.verify_certs)


        esHandle.web_request = lambda path, method, data: self.web_request(path, method, data)
        return esHandle
