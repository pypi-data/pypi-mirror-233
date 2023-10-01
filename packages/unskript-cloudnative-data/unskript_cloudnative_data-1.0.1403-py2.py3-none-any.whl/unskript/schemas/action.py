##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

"""
    this schema describes the Action metadata file
"""


class ActionEnum(str, Enum):
    aws = "LEGO_TYPE_AWS"
    k8s = "LEGO_TYPE_K8S"
    gcp = "LEGO_TYPE_GCP"
    slack = "LEGO_TYPE_SLACK"
    posgresql = "LEGO_TYPE_POSTGRESQL"
    mongodb = "LEGO_TYPE_MONGODB"
    jenkins = "LEGO_TYPE_JENKINS"
    mysql = "LEGO_TYPE_MYSQL"
    jira = "LEGO_TYPE_JIRA"
    rest = "LEGO_TYPE_REST"
    elasticsearch = "LEGO_TYPE_ELASTICSEARCH"
    kafka = "LEGO_TYPE_KAFKA"
    grafana = "LEGO_TYPE_GRAFANA"
    redis = "LEGO_TYPE_REDIS"
    ssh = "LEGO_TYPE_SSH"
    prometheus = "LEGO_TYPE_PROMETHEUS"
    stripe = "LEGO_TYPE_STRIPE"
    datadog = "LEGO_TYPE_DATADOG"
    zabbix = "LEGO_TYPE_ZABBIX"
    pingdom = "LEGO_TYPE_PINGDOM"
    opensearch = "LEGO_TYPE_OPENSEARCH"
    terraform = "LEGO_TYPE_TERRAFORM"
    infra = "LEGO_TYPE_INFRA"
    hadoop = "LEGO_TYPE_HADOOP"
    airflow = "LEGO_TYPE_AIRFLOW"
    mssql = "LEGO_TYPE_MSSQL"
    snowflake = "LEGO_TYPE_SNOWFLAKE"
    splunk = "LEGO_TYPE_SPLUNK"
    salesforce = "LEGO_TYPE_SALESFORCE"
    mantishub = "LEGO_TYPE_MANTISHUB"
    azure = "LEGO_TYPE_AZURE"
    github = "LEGO_TYPE_GITHUB"
    nomad = "LEGO_TYPE_NOMAD"
    netbox = "LEGO_TYPE_NETBOX"
    chatgpt = "LEGO_TYPE_CHATGPT"
    opsgenie = "LEGO_TYPE_OPSGENIE"

class ActionOutputTypeEnum(str, Enum):
    str = "ACTION_OUTPUT_TYPE_STR"
    int = "ACTION_OUTPUT_TYPE_INT"
    bool = "ACTION_OUTPUT_TYPE_BOOL"
    list = "ACTION_OUTPUT_TYPE_LIST"
    dict = "ACTION_OUTPUT_TYPE_DICT"
    bytes = "ACTION_OUTPUT_TYPE_BYTES"
    none = "ACTION_OUTPUT_TYPE_NONE"
    object = "ACTION_OUTPUT_TYPE_OBJECT"


class ActionSchema(BaseModel):
    action_title: str = Field(
        title="Title"
    )
    action_description: str = Field(
        title="Describe the action"
    )
    action_type: ActionEnum = Field(
        title="Connector used by the Action"
    )
    action_version: str = Field(
        default="1.0.0",
        title="Action Version"
    )
    action_entry_function: str = Field(
        title="Name of the function of invoke for this Action",
    )
    action_nouns: Optional[List[str]] = Field(
        title="Nouns indicates the objects that are manipulated by this Action"
    )
    action_verbs: Optional[List[str]] = Field(
        title="Verbs is the list of manipulations accomplished by this Action"
    )
    action_needs_credential: bool = Field(
        title="Does this action need a credential for operation"
    )
    action_supports_poll: bool = Field(
        default=True,
        title="Does this action support poll configuration"
    )
    action_output_type: Optional[ActionOutputTypeEnum] = Field(
        default="ACTION_OUTPUT_TYPE_NONE",
        title="Output type of the lego"
    )
    action_supports_iteration: bool = Field(
        default=True,
        title="Does this action support iteration"
    )
    action_bash_command: Optional[bool] = Field(
        default=False,
        title="Does this action takes bash command as input"
    )
    action_is_check: Optional[bool] = Field(
        default=False,
        title="Does this action for check legos"
    )
    action_categories: Optional[List[str]] = Field(
        title="Categories is the list of manipulations accomplished by this Action"
    )
    action_next_hop: Optional[List[str]] = Field(
        title="Next hop is the list of remediation runbooks accomplished by this Action"
    )
    action_next_hop_parameter_mapping: Optional[dict] = Field(
        title="Next hop parameter mapping is the list of parameters for remediation runbooks"
    )
    action_is_remediation: Optional[bool] = Field(
        default=False,
        title="Does this action takes remediation runbooks"
    )


class CodeSnippet(BaseModel):
    name: str  # stored in the metadata file
    description: str  # stored in the metadata file
    language: str = Field(
        default="python"  # fixed
    )
    type: str  # stored in the metadatafile
    inputschema: List[dict]  # stored in the action file
    code: List[str]  # stored in the action file
    uuid: str
    version: str
    id: int
    tags: List[str]
    orderProperties: List[str]
    metadata: ActionSchema


class CodeSnippets(BaseModel):
    snippets: Optional[List[CodeSnippet]] = Field()
