##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
import boto3
from pydantic import ValidationError
import psycopg2

from unskript.connectors.schema.postgresql import PostgreSQLSchema
from unskript.connectors.interface import ConnectorInterface

class PostgreSQLConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            postGreSQLCredential = PostgreSQLSchema(**data)
        except ValidationError as e:
            raise e

        try:
            conn = psycopg2.connect(dbname=postGreSQLCredential.DBName,
                user=postGreSQLCredential.User,
                password=postGreSQLCredential.Password.get_secret_value(),
                host=postGreSQLCredential.Host,
                port=postGreSQLCredential.Port)
        except psycopg2.Error as e:
            errString = 'Not able to connect to PostGreSQL, error {}, code {}'.format(e.pgerror, e.pgcode)
            print(errString)
            raise Exception(errString)
        return conn