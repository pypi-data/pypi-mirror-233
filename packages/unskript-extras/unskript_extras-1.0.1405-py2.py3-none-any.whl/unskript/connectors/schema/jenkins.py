##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class JenkinsSchema(BaseModel):
    url: str = Field(
        title='Jenkins url',
        description='Full Jenkins URL.'
    )
    user_name: str = Field(
        "",
        title='Username',
        description='Username to authenticate with Jenkins.'
    )
    password: SecretStr = Field(
        "",
        title='Password',
        description='Password or API Token to authenticate with Jenkins.'
    )
