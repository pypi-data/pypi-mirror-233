##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import pymongo
from pymongo import MongoClient
from pydantic import ValidationError, SecretStr
from typing import Any
from unskript.connectors.schema.mongodb import AtlasSchema


from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.mongodb import MongoDBSchema

class MongoDBAtlasClient():

    def __init__(self, public_key:str, private_key:SecretStr):
        self.base_url = 'https://cloud.mongodb.com/api/atlas/v1.0'
        self.public_key = public_key
        self.private_key = private_key

    def get_base_url(self):
        return self.base_url

    def get_public_key(self):
        if self.public_key:
            return self.public_key
        else:
            raise Exception("atlas admin api credentials not programmed")

    def get_private_key(self):
        if self.private_key:
            return self.private_key.get_secret_value()
        else:
            raise Exception("atlas admin api credentials not programmed")

class MongoDBConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            mongoCredential = MongoDBSchema(**data)
        except ValidationError as e:
            raise e

        #client = MongoDBComboClient()
        try:
            if isinstance(mongoCredential.authentication, AtlasSchema):
                atlas_client = MongoDBAtlasClient(public_key=mongoCredential.authentication.atlas_public_key,
                                                  private_key=mongoCredential.authentication.atlas_private_key)
                client = atlas_client
            else:
                client = MongoClient(mongoCredential.host,
                                    username=mongoCredential.authentication.user_name,
                                    password=mongoCredential.authentication.password.get_secret_value(),
                                    port=mongoCredential.port)

        except pymongo.errors.PyMongoError as e:
            errString = 'Not able to connect to MongoDB, error {}'.format(str(e))
            print(errString)
            raise Exception(errString)
        return client


