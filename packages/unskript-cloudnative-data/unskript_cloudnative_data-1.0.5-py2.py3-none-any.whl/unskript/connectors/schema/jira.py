##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class JiraSchema(BaseModel):
    url: str = Field(
        title='URL',
        description='URL of jira server.'
    )
    email: str = Field(
        title='Email',
        description='Email to authenticate to jira.'
    )
    api_token: SecretStr = Field(
        title='Api Token',
        description='Api token to authenticate to jira.'
    )

