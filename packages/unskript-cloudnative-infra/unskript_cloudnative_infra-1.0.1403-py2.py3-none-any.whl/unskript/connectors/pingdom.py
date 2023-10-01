##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any

from unskript.connectors.schema.pingdom import PingdomSchema

from unskript.connectors.interface import ConnectorInterface
from unskript.thirdparty.pingdom import swagger_client as pingdom_client


class PingdomConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            pingdomCredential = PingdomSchema(**data)
            handle = pingdom_client.ApiClient(header_name='Authorization',
                                              header_value='Bearer %s' % pingdomCredential.apikey.get_secret_value())

        except Exception as e:
            raise e

        return handle
