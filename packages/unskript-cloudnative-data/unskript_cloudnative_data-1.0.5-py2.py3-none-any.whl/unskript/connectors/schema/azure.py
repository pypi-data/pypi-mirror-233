##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Union, Optional
from typing_extensions import Literal


class ServicePrincipalCredentialsSchema(BaseModel):
    auth_type: Literal['Service Principal Credentials']
    tenant_id: str = Field(
        title='Tenant ID',
        description='The Directory (tenant) ID to be used for authentication'
    )
    client_id: str = Field(
        title='Client ID',
        description='This is the app id the app will use to access Azure'
    )
    client_secret: SecretStr = Field(
        title='Client Secret',
        description='The client secret to be used for authentication. This must be generated for your app.'
    )

    class Config:
        title = 'Service Principal Credentials'


class UserPassCredentialsSchema(BaseModel):
    auth_type: Literal['User Pass Credentials']
    username: str = Field(
        title='Username',
        description='Account username.'
    )
    password: SecretStr = Field(
        title='Password',
        description='Account password.'
    )
    cloud_environment: Optional[str] = Field(
        title='Cloud Environment',
        description='A targeted cloud environment.'
    )

    class Config:
        title = 'User Pass Credentials'


class AzureSchema(BaseModel):
    subscription_id: Optional[str] = Field(
        title='Subscription ID',
        description='Azure Subscription ID'
    )
    authentication: Union[ServicePrincipalCredentialsSchema, UserPassCredentialsSchema] = Field(..., discriminator='auth_type')
