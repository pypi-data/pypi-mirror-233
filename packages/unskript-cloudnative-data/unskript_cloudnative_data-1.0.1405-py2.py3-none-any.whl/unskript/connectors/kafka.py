##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##
import re
from kafka import KafkaProducer, KafkaConsumer
from kafka_utils.util.config import ClusterConfig
from pydantic import ValidationError
from subprocess import PIPE, run
from typing import Type
from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.kafka import KafkaSchema

class KafkaConnector(ConnectorInterface):

    def kafka_cli_cmd(self, cmd: str, broker: str=None):
        if cmd.startswith("kafka") is False:
            return None
        #Check if bootstrap server is already provided in the command
        regexp = re.compile("--bootstrap-server(.*)$")
        m = regexp.search(cmd)
        if m is None:
            # suffix the bootstrap command
            cmd = f'{cmd.strip()} --bootstrap-server {broker}'

        return f"{cmd.strip()}"

    def get_handle(self, data):
        try:
            kafkaCredential = KafkaSchema(**data)

            if len(kafkaCredential.sasl_username) == 0:
                sasl_username = None
            else:
                sasl_username = kafkaCredential.sasl_username

            if len(kafkaCredential.sasl_password) == 0:
                sasl_password = None
            else:
                sasl_password = kafkaCredential.sasl_password.get_secret_value()

        except ValidationError as e:
            raise e

        kafkaHandle = KafkaProducer(bootstrap_servers=kafkaCredential.broker,
                                    sasl_plain_username=sasl_username,
                                    sasl_plain_password=sasl_password)

        kafkaHandle.run_native_cmd = lambda cmd: run(self.kafka_cli_cmd(
            cmd, kafkaCredential.broker), stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

        if len(kafkaCredential.zookeeper) != 0:
            kafkaHandle.cluster_config = self.get_cluster_config(kafkaCredential.broker, kafkaCredential.zookeeper)

        kafkaHandle.consumer_handle = self.get_consumer_handle(data)
        return kafkaHandle

    def get_consumer_handle(self, data):
        try:
            kafkaCredential = KafkaSchema(**data)

            if len(kafkaCredential.sasl_username) == 0:
                sasl_username = None
            else:
                sasl_username = kafkaCredential.sasl_username

            if len(kafkaCredential.sasl_password) == 0:
                sasl_password = None
            else:
                sasl_password = kafkaCredential.sasl_password.get_secret_value()

        except ValidationError as e:
            raise e

        kafkaHandle = KafkaConsumer(bootstrap_servers=kafkaCredential.broker,
                                    sasl_plain_username=sasl_username,
                                    sasl_plain_password=sasl_password)
        return kafkaHandle

    def get_cluster_config(self, broker, zookeeper) -> Type[ClusterConfig]:
        config = ClusterConfig
        config.broker_list = [broker]
        config.zookeeper = zookeeper
        return config
