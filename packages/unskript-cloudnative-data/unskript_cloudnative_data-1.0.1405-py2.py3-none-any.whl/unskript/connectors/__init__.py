# pylint: skip-file
#
##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from json import loads as json_loads
from json import dumps as json_dumps
from pydantic import ValidationError
from unskript.secrets import SecretsStore

from unskript.schemas.credentials import TaskCredentialValueSchema
import os


class SecretStoreApi():

    def __init__(self, mode, store_type, cfg):
        self.mode = mode
        self.cfg = cfg
        self.handle_cache = {}

        try:
            secret_store = SecretsStore(mode, store_type, cfg)
        except Exception as e:
            raise e

        self.secret_store = secret_store
        return None

    def get_handle(self, credentials_str: str, load_default: bool = False):

        c = json_loads(credentials_str)
        try:
            connectorObject = TaskCredentialValueSchema(**c)

            # default to file credentials if this fails
            # only applicable to AWS and k8s
        except ValidationError as e:
            raise e

        if os.environ.get('UNSKRIPT_MODE') != None:
            secretValue = self.secret_store.get_secret(
                connectorObject.credential_type, connectorObject.credential_id)
        else:
            if load_default is True and connectorObject.credential_name is None:
                # try to load default credentials from file in specific cases
                if connectorObject.credential_type != "CONNECTOR_TYPE_K8S":
                    raise Exception("No default credentials found for %s",
                                    connectorObject.credential_type)

                # if the file ~/.kube/config exists, then use it
                if connectorObject.credential_type == "CONNECTOR_TYPE_K8S":
                    if os.path.exists(os.environ.get('HOME').strip() + '/.kube/config'):
                        with open(os.environ.get('HOME').strip() + '/.kube/config', 'r') as f:
                            from unskript.connectors.k8 import K8Connector, K8Schema
                            k8sSecretValue = f.read()
                            k8sDict = {"kubeconfig": k8sSecretValue}
                            secretValue = json_loads(json_dumps(k8sDict))
                    else:
                        raise Exception("No default credentials found for %s",
                                        connectorObject.credential_type)
            else:

                secretValue = self.secret_store.get_secret_by_name(
                    connectorObject.credential_name)

        if self.handle_cache.get(connectorObject.credential_id) is not None:
            handle = self.handle_cache.get(connectorObject.credential_id)
            return handle

        if connectorObject.credential_type == "CONNECTOR_TYPE_AWS":
            # Connector for RoleARN type handle
            try:
                from unskript.connectors.aws import AWSConnector
                handle = AWSConnector().get_handle(
                    data=secretValue, credential_id=connectorObject.credential_id)
            # Connector for AccessID type handle
            except ValidationError:
                from unskript.connectors.awsv2 import AwsV2Connector
                handle = AwsV2Connector().get_handle(data=secretValue)
            except Exception as e:
                raise e
        elif connectorObject.credential_type in ["CONNECTOR_TYPE_K8S", "CONNECTOR_TYPE_K8"]:
            from unskript.connectors.k8 import K8Connector
            handle = K8Connector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_GCP":
            from unskript.connectors.gcp import GCPConnector
            handle = GCPConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_SLACK":
            from unskript.connectors.slack import SlackConnector
            handle = SlackConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_POSTGRESQL":
            from unskript.connectors.postgresql import PostgreSQLConnector
            handle = PostgreSQLConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_MONGODB":
            from unskript.connectors.mongodb import MongoDBConnector
            handle = MongoDBConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_JENKINS":
            from unskript.connectors.jenkins import JenkinsConnector
            handle = JenkinsConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_MYSQL":
            from unskript.connectors.mysql import MySQLConnector
            handle = MySQLConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_JIRA":
            from unskript.connectors.jira import JiraConnector
            handle = JiraConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_REST":
            from unskript.connectors.rest import RESTConnector
            handle = RESTConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_ELASTICSEARCH":
            from unskript.connectors.elasticsearch import ElasticSearchConnector
            handle = ElasticSearchConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_KAFKA":
            from unskript.connectors.kafka import KafkaConnector
            handle = KafkaConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_GRAFANA":
            from unskript.connectors.grafana import GrafanaConnector
            handle = GrafanaConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_REDIS":
            from unskript.connectors.redis import RedisConnector
            handle = RedisConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_SSH":
            from unskript.connectors.ssh import SSHConnector
            handle = SSHConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_PROMETHEUS":
            from unskript.connectors.prometheus import PrometheusConnector
            handle = PrometheusConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_STRIPE":
            from unskript.connectors.stripe import StripeConnector
            handle = StripeConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_DATADOG":
            from unskript.connectors.datadog import DatadogConnector
            handle = DatadogConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_ZABBIX":
            from unskript.connectors.zabbix import ZabbixConnector
            handle = ZabbixConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_PINGDOM":
            from unskript.connectors.pingdom import PingdomConnector
            handle = PingdomConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_OPENSEARCH":
            from unskript.connectors.opensearch import OpenSearchConnector
            return OpenSearchConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_HADOOP":
            from unskript.connectors.hadoop import HadoopConnector
            handle = HadoopConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_AIRFLOW":
            from unskript.connectors.airflow import AirflowConnector
            handle = AirflowConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_MSSQL":
            from unskript.connectors.ms_sql import MSSQLConnector
            handle = MSSQLConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_SPLUNK":
            from unskript.connectors.splunk import SplunkConnector
            handle = SplunkConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_SNOWFLAKE":
            from unskript.connectors.snowflake import SnowflakeConnector
            handle = SnowflakeConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_SALESFORCE":
            from unskript.connectors.salesforce import SalesforceConnector
            handle = SalesforceConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_MANTISHUB":
            from unskript.connectors.mantishub import MantishubConnector
            handle = MantishubConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_AZURE":
            from unskript.connectors.azure import AzureConnector
            handle = AzureConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_GITHUB":
            from unskript.connectors.github import GithubConnector
            handle = GithubConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_NETBOX":
            from unskript.connectors.netbox import NetboxConnector
            handle = NetboxConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_NOMAD":
            from unskript.connectors.nomad import NomadConnector
            handle = NomadConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_CHATGPT":
            from unskript.connectors.chatgpt import ChatGPTConnector
            handle = ChatGPTConnector().get_handle(data=secretValue)
        elif connectorObject.credential_type == "CONNECTOR_TYPE_OPSGENIE":
            from unskript.connectors.opsgenie import OpsgenieConnector
            handle = OpsgenieConnector().get_handle(data=secretValue)
        else:
            raise Exception("Unsupported Connector Type %s",
                            connectorObject.credential_type)

        # self.handle_cache[connectorObject.credential_id] = handle
        return handle
