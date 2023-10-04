##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union

from pydantic import BaseModel, Field, SecretStr
from typing import Optional, Union
from typing_extensions import Literal


class AuthSchema(BaseModel):
    auth_type: Literal['Basic Auth']
    password: Optional[SecretStr] = Field(
        default='',
        title='Password',
        description='Password to use for password authentication.'
    )
    proxy_password: Optional[str] = Field(
        title='Proxy user password',
        description='Password to login to proxy_host with. Defaults to no password.'
    )
    class Config:
        title = 'Basic Auth'

class VaultSchema(BaseModel):
    auth_type: Literal['Vault']
    vault_url: str = Field(
        title='Vault URL',
        description='Vault URL eg: http://127.0.0.1:8200'
    )
    vault_secret_path: str = Field(
        title='SSH Secret Path',
        description='The is the path in the Vault Configuration tab of ssh secret. eg: ssh'
    )
    vault_role: str = Field(
        title='Vault Role',
        description='Vault role associated with the above ssh secret.'
    )

    class Config:
        title = 'Vault'

class PrivateKeySchema(BaseModel):
    auth_type: Literal['API Token']
    private_key: Optional[str] = Field(
        default='',
        title='Private Key File',
        description='Contents of the Private Key File to use for authentication.'
    )
    proxy_private_key: Optional[str] = Field(
        title='Proxy Private Key File',
        description='Private key file to be used for authentication with proxy_host.'
    )

    class Config:
        title = 'Pem File'

class KerberosSchema(BaseModel):
    auth_type: Literal['Kerberos']
    user_with_realm: str = Field(
        title="Kerberos user@REALM",
        description="Kerberos UserName like user@EXAMPLE.COM REALM is usually defined as UPPER-CASE"
    )
    kdc_server: str = Field(
        title="KDC Server",
        description="KDC Server Domain Name. like kdc.example.com"
    )
    admin_server: Optional[str] = Field(
        default="",
        title="Admin Server",
        description="Kerberos Admin Server. Normally same as KDC Server"
    )
    password: Optional[SecretStr] = Field(
        default="",
        title="Password",
        description="Password for the above Username"
    )
    proxy_password: Optional[SecretStr] = Field(
        default="",
        title='Proxy user password',
        description='Password to login to proxy_host with. Defaults is no password.'
    )
    class Config:
        title = 'Kerberos'

class SSHSchema(BaseModel):
    port: Optional[int] = Field(
        default=22,
        title='Port',
        description='SSH port to connect to.'
    )
    username: Optional[str] = Field(
        default='',
        title='Username',
        description='Username to use for authentication'
    )
    proxy_host: Optional[str] = Field(
        title='Proxy host',
        description='SSH host to tunnel connection through so that SSH clients connect to host via client -> proxy_host -> host.'
    )
    proxy_user: Optional[str] = Field(
        title='Proxy user',
        description='User to login to proxy_host as. Defaults to username.'
    )
    proxy_port: Optional[int] = Field(
        default=22,
        title='Proxy port',
        description='SSH port to use to login to proxy host if set. Defaults to 22.'
    )
    authentication: Union[AuthSchema, PrivateKeySchema, VaultSchema, KerberosSchema] = Field(..., discriminator='auth_type')
