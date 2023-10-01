##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError
from slack_sdk import WebClient

from unskript.connectors.schema.slack import SlackSchema
from unskript.connectors.interface import ConnectorInterface


class SlackConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            slackCredential = SlackSchema(**data)
        except ValidationError as e:
            raise e

        slackClient = WebClient(token=slackCredential.bot_user_oauth_token)
        return slackClient
