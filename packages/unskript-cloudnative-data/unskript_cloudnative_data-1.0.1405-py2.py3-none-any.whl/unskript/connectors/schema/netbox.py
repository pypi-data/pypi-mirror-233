##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class NetboxSchema(BaseModel):
    host: str =Field(
        title='Netbox Host',
        description='Address of Netbox host'
    )
    token: Optional[SecretStr] = Field(
        '',
        title='Token',
        description='Token value to authenticate write requests.'
    )
    threading: Optional[bool] = Field(
        title='Threading',
        description='Enable for multithreaded calls like .filter() and .all() queries. To enable set to True '
    )