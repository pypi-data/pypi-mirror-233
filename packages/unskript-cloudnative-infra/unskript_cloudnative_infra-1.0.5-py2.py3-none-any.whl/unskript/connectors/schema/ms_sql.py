##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from pydantic import BaseModel, Field, SecretStr
from typing import Optional


class MSSQLSchema(BaseModel):
    Server: str = Field(
        title='Server',
        description='''Servername of the MSSQL In format: [Servername], [Port Number configured to allow remote connections] \ [SQL Server instance name]
        eg: DESKTOP-0AB9P2O,5068\sqlexpress'''
    )
    User: Optional[str] = Field(
        '',
        title='Username',
        description='Username to authenticate to MSSQL.'
    )
    Password: Optional[SecretStr] = Field(
        '',
        title='Password',
        description='Password to authenticate to MSSQL.'
    )
    DBName: str = Field(
        title='Database name',
        description='Name of the database.'
    )
