##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##
from typing import Optional

from pydantic import BaseModel, Field, SecretStr

class OpenSearchSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='Host name. For AWS Opensearch, this is the domain endpoint. For eg: elasticsearch.us-west-2.es.amazonaws.com'
    )
    port: Optional[int] = Field(
        9200,
        title='Port',
        description='Port on which Opensearch is listening.'
    )
    username: str = Field(
        '',
        title='Username',
        description='Username for Basic Auth.'
    )
    password: SecretStr = Field(
        '',
        title='Password',
        description='Password for Basic Auth.'
    )
    use_ssl: bool = Field(
        False,
        title='Use SSL',
        description='Use SSL for communicating to Opensearch host.'
    )

