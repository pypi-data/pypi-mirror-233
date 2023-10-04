##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from unskript.connectors.schema.hadoop import HadoopEmrSchema
from unskript.connectors.interface import ConnectorInterface
import unskript.thirdparty.hadoop as hadoop


class HadoopConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            hadoopCredential = HadoopEmrSchema(**data)
            if hadoopCredential.username and hadoopCredential.password:
                api = hadoop.Client(hadoopCredential.base_url, hadoopCredential.username,
                                    hadoopCredential.password.get_secret_value())
            else:
                api = hadoop.Client(hadoopCredential.base_url)

        except Exception as e:
            raise e

        return api
