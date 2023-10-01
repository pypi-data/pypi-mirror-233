##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union
from typing_extensions import Literal


class AtlasSchema(BaseModel):
    auth_type: Literal['Atlas Administrative API using HTTP Digest Authentication']
    atlas_public_key: Optional[str] = Field(
        default='',
        title='Atlas API Public Key',
        description='The public key acts as the username when making API requests'
    )
    atlas_private_key: Optional[SecretStr] = Field(
        default='',
        title='Atlas API Private Key',
        description='The private key acts as the password when making API requests'
    )


class AuthSchema(BaseModel):
    auth_type: Literal['Basic Auth']
    user_name: Optional[str] = Field(
        '',
        title='Username',
        description='Username to authenticate with MongoDB.'
    )
    password: Optional[SecretStr] = Field(
        '',
        title='Password',
        description='Password to authenticate with MongoDB.'
    )


class MongoDBSchema(BaseModel):
    host: str = Field(
        title='Host',
        description='Full MongoDB URI, in addition to simple hostname. It also supports mongodb+srv:// URIs'
    )
    port: Optional[int] = Field(
        27017,
        title='Port',
        description='Port on which mongoDB server is listening.'
    )
    authentication: Union[AtlasSchema, AuthSchema] = Field(..., discriminator='auth_type')


