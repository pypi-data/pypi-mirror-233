##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError
from pyzabbix import ZabbixAPI

from unskript.connectors.schema.zabbix import ZabbixSearchSchema
from unskript.connectors.interface import ConnectorInterface

class ZabbixConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            zabbixCredential = ZabbixSearchSchema(**data)
        except ValidationError as e:
            raise e

        zabbix = ZabbixAPI(zabbixCredential.url)

        try:
            zabbix.login(api_token=zabbixCredential.api_token.get_secret_value())

        except Exception as e:
            raise e
        return zabbix