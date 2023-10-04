##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from google.cloud import secretmanager
import json
import base64
from unskript.secrets.interface import SecretInterface

# GCP Specific Variables
GCP_PROJECT_ID = "GCP_PROJECT_ID"

class GCPSecret(SecretInterface):
    def __init__(self, input_dict):
        self.client = secretmanager.SecretManagerServiceClient()
        self.projectId = input_dict.get(GCP_PROJECT_ID)
    
    def get_secret(self, connectorType: str, key:str)->str:
        """
            Retrieves the First Version of key from GCP 
        """
        name = self.create_query_string(connectorType, key)
        try:
            response = self.client.access_secret_version(request={"name": name})
        except ValueError as e:
            print("The request has invalid parameters")
            raise(e)
        else:
            payload = response.payload.data.decode("UTF-8")
            base64_bytes = payload.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            text_secret_data = json.loads(message_bytes.decode('ascii'))
            return text_secret_data

    def create_query_string(self, connectorType: str, key: str) -> str:
        """
            Constructs the Query string required to retrieve secret
        """
        separator = "/"
        secret_delim = "_"
        secret_items = ('unskript', connectorType, key)
        secret = secret_delim.join(secret_items)
        values = ('projects', str(self.projectId), 'secrets', secret, 'versions', 'latest')
        ret = separator.join(values)
        return ret 