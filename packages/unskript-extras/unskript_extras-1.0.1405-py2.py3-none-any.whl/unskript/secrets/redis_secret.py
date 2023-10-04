##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import redis
import base64
import json

from unskript.secrets.interface import SecretInterface

REDIS_SECRET_PREFIX = "REDIS_SECRET_PREFIX"
REDIS_HOST = "REDIS_HOST"


class RedisSecret(SecretInterface):
    def __init__(self, input_dict):
        host = input_dict.get(REDIS_HOST)
        pool = redis.ConnectionPool(host=host)
        self.client = redis.Redis(connection_pool=pool)
        self.secretPrefix = input_dict.get(REDIS_SECRET_PREFIX)

    def get_secret(self, connectorType:str, key:str)->str:
        """
            Create the key based on how its stored in the secret store.
        """
        key = self.create_key(connectorType, key)
        try:
            value = self.client.get(key)
        except Exception as e:
            print(f'Get key {key} failed, {str(e)}')
            raise e
        if value is None:
            print(f'Key {key} not found')
            raise Exception(f'Key {key} not found')
        #Secrets are base64 encoded
        message_bytes = base64.b64decode(value)
        text_secret_data = json.loads(message_bytes.decode('ascii'))
        return text_secret_data
    """
    Creates the key based
    """
    def create_key(self, connectorType:str, key:str)->str:
            separator = ":"
            secretKeys = (self.secretPrefix, connectorType, key)
            return separator.join(secretKeys)
