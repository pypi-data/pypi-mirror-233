##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from pydantic import BaseModel, Field, SecretStr
from typing import Optional

class NomadSchema(BaseModel):
    host: str =Field(
        title='Nomad IP address',
        description='IP address of Nomad host'
    )
    timeout: Optional[int] = Field(
        default=5,
        title='Timeout(seconds)',
        description='Timeout in seconds to retry connection'
    )
    token: Optional[SecretStr] = Field(
        '',
        title='Token',
        description='Token value to authenticate requests to the cluster when using namespace'
    )
    verify_certs: Optional[bool] = Field(
        title='Verify certs',
        description='Verify server ssl certs. This can be set to true when working with private certs.'
    )
    secure: Optional[bool] = Field(
        title='Secure',
        description='HTTPS enabled?'
    )
    namespace: Optional[str] = Field(
        title='Namespace',
        description='Name of Nomad Namespace. By default, the default namespace will be considered.'
    )