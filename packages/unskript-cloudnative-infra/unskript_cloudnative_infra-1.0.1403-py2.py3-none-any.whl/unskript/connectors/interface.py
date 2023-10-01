##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from abc import ABC, abstractmethod


class ConnectorInterface(ABC):
    @abstractmethod
    def get_handle(self, **kwargs):
        pass
