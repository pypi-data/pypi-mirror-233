##
##  Copyright (c) 2023 unSkript, Inc
##  All rights reserved.
##
from typing import Any
import openai
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.chatgpt import ChatGPTSchema


class ChatGPTConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            chatGPTCredential = ChatGPTSchema(**data)
        except ValidationError as e:
            raise e
        try:
            if chatGPTCredential.organization =='':
                openai.api_key = chatGPTCredential.api_token.get_secret_value()
            else:
                openai.api_key = chatGPTCredential.api_token.get_secret_value()
                openai.organization = chatGPTCredential.organization
        except Exception as e:
            raise e

        return openai