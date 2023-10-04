##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr


class PingdomSchema(BaseModel):
    apikey: SecretStr = Field(
        title='API Key',
        description=' API key to access Pingdom'
    )