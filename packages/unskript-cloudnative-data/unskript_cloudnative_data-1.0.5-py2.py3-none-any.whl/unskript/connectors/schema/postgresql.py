##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class PostgreSQLSchema(BaseModel):
    Host: str = Field(
        title='Hostname',
        description='Hostname of the postgres server.'
    )
    Port: Optional[int] = Field(
        5432,
        title='Port',
        description='Port on which postgres server is listening.')
    User: Optional[str] = Field(
        '',
        title='Username',
        description='Username to authenticate to postgres.'
    )
    Password: Optional[SecretStr] = Field(
        '',
        title='Password',
        description='Password to authenticate to postgres.'
    )
    DBName: str = Field(
        title='Database name',
        description='Name of the database to connect to.'
    )
