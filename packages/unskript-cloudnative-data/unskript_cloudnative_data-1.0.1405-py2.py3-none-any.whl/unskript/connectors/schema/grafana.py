##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field


class GrafanaSchema(BaseModel):
    host: str = Field(
        title='URL',
        description=' URL of the grafana.'
    )
    api_key: str = Field(
        '',
        title = 'API Token',
        description = 'API Token to authenticate to grafana.'
    )
