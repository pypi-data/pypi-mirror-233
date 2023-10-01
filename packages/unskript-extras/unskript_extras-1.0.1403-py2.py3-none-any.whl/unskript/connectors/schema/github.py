from pydantic import BaseModel, Field, SecretStr

class GithubSchema(BaseModel):
    token: SecretStr = Field(
        title='Access token',
        description='Github Personal Access Token.'
    )
    hostname: str =Field(
        '',
        title='Custom Hostname',
        description='Custom hostname for Github Enterprise Version.'
    )