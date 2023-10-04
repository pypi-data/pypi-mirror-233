##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field


class SlackSchema(BaseModel):
    bot_user_oauth_token: str = Field(
        title='OAuth Access Token',
        description='OAuth Access Token of the Slack app.'
    )