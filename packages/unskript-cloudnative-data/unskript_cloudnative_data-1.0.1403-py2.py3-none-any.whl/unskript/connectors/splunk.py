##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Any
from pydantic import ValidationError
import splunklib.client as client
import splunklib.results as results


from unskript.connectors.schema.splunk import SplunkSchema
from unskript.connectors.interface import ConnectorInterface

class SplunkConnector(ConnectorInterface):
    def get_handle(self, data)->Any:
        try:
            splunkCredential = SplunkSchema(**data)
        except ValidationError as e:
            raise e

        try:
            service = client.connect(host=splunkCredential.hostname, port=splunkCredential.port,
            token=splunkCredential.token)
        except Exception as e:
            raise e
        return service
