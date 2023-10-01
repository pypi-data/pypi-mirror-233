##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from abc import ABC, abstractmethod


class SecretInterface(ABC):
    @abstractmethod
    def get_secret(self, connectorType:str, key:str)->str:
        pass
