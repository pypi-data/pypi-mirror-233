##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from unskript.connectors.schema.mantishub import MantishubSchema
from unskript.connectors.interface import ConnectorInterface
from unskript.thirdparty.mantishub import Client as MantishubClient


class MantishubConnector(ConnectorInterface):
    def get_handle(self, data) -> MantishubClient:
        try:
            mantishubCredential = MantishubSchema(**data)
            if mantishubCredential.base_url != "" and mantishubCredential.api_token != "":
                mantishub_client = MantishubClient(mantishubCredential.base_url,
                                                   mantishubCredential.api_token.get_secret_value())
                if mantishub_client.api.validate_api:
                    return mantishub_client
        except Exception as e:
            raise e
