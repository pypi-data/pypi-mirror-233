#
# Copyright 2018-2021 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import io
import json
import os
import re

import uuid

import logging
import configparser

from typing import Any
from typing import List

from jsonschema import draft7_format_checker
from jsonschema import validate
from jsonschema import ValidationError
from traitlets import Type  # noqa H306
from traitlets.config import LoggingConfigurable  # noqa H306
# from pathlib import Path

from unskript.secrets.elyra_metadata_error import SchemaNotFoundError
from unskript.secrets.elyra_metadata_metadata import Metadata
from unskript.secrets.elyra_metadata_schema import SchemaManager

import lazy_import

jupyter_core = lazy_import.lazy_module('jupyter_core')

from unskript.secrets.elyra_metadata_storage import FileMetadataStore
from unskript.secrets.elyra_metadata_storage import MetadataStore
# from unskript.secrets.elyra_metadata_storage import credential_list
# from elyra.metadata.utils import is_aws_profile_present

"""
Private function to create a AWS entry when AWS Credential
is created for OSS Docker. This is to decouple AWS Creds
creation when used in conjunction with kubectl
"""
def create_aws_entry(name: str, metadata: dict):
    connector_data = metadata.get('metadata').get('connectorData')
    if connector_data is None:
        print("Connector Data is Null, nothing to save")
        return
    c_data = json.loads(connector_data)
    home_dir = os.environ.get('HOME')
    if not os.path.exists(home_dir + '/.aws'):
        try:
            os.mkdir(home_dir + '/.aws')
        except OSError as e:
            raise e
    if is_aws_profile_present(name) == True:
        data = {"aws_access_key_id": c_data.get('authentication').get('access_key'),
                "aws_secret_access_key": c_data.get('authentication').get('secret_access_key')}
        replace_aws_creds(name, data)
    else:
        fle = Path(home_dir + '/.aws/credentials')
        f = open(fle, "a")
        f.write(f"\n[{name}]\n")
        f.write(f"aws_access_key_id = %s\n" % c_data.get('authentication').get('access_key'))
        f.write(f"aws_secret_access_key = %s\n" % c_data.get('authentication').get('secret_access_key'))
        f.close()

"""
Private function to search and replace existing AWS credential.
This function is used by create_aws_entry
"""
def replace_aws_creds(profile: str, data: dict):
    # We are called only after confirming profile being present
    # No need to check again, replace the aws creds
    home_dir = os.environ.get('HOME')
    config = configparser.ConfigParser()
    config.read(home_dir + '/.aws/credentials')
    config.set(profile, 'aws_access_key_id', data.get('aws_access_key_id'))
    config.set(profile, 'aws_secret_access_key', data.get('aws_secret_access_key'))
    with open(home_dir + '/.aws/credentials', 'w') as f:
        config.write(f)

    return

class MetadataManager(LoggingConfigurable):
# class MetadataManager():
    """Manages metadata instances"""

    # System-owned namespaces
    NAMESPACE_RUNTIMES = "runtimes"
    NAMESPACE_CODE_SNIPPETS = "code-snippets"
    NAMESPACE_RUNTIME_IMAGES = "runtime-images"
    NAMESPACE_CREDENTIAL_STORE = "credential-store"
    NAMESPACE_CONNECTOR_TYPE_LIST = "connectors-types-list"
    NAMESPACE_SAVE_AND_CLOSE = "save-and-close"
    NAMESPACE_LEGO_SAVE = "lego-save"
    NAMESPACE_AUDIT_USER_ACTIVITY = "audit-user-activity"
    NAMESPACE_LEGO_SEARCH = "lego-search"
    NAMESPACE_LEGO_LIST = "lego-list"
    NAMESPACE_GET_LEGO = "get-lego"
    NAMESPACE_DELETE_LEGO = "delete-lego"
    NAMESPACE_CREDENTIAL_SAVE = "credential-save"
    NAMESPACE_CREDENTIAL_LIST = "credential-list"
    NAMESPACE_CREDENTIAL_DELETE = "credential-delete"
    NAMESPACE_CREDENTIAL_EDIT = "credential-edit"
    NAMESPACE_CONNECTOR_LABELS_LIST = "connectors-labels-list"
    NAMESPACE_RUNBOOK_LIST = "runbook-list"
    NAMESPACE_GET_RUNBOOK = "get-runbook"

    metadata_store_class = Type(default_value=FileMetadataStore, config=True,
                                klass=MetadataStore,
                                help="""The metadata store class.  This is configurable to allow subclassing of
                                the MetadataStore for customized behavior.""")

    def __init__(self, namespace: str = NAMESPACE_CREDENTIAL_STORE, **kwargs: Any):
        """
        Generic object to manage metadata instances.
        :param namespace (str): the partition where metadata instances are stored
        :param kwargs: additional arguments to be used to instantiate a metadata manager
        Keyword Args:
            metadata_store_class (str): the name of the MetadataStore subclass to use for storing managed instances
        """
        super().__init__(**kwargs)
        # Schemas are stored in the namespaces they create,
        # so instead of changing FE, we just change the namespace here
        self.schema_mgr = SchemaManager.instance()
        self.schema_mgr.validate_namespace(namespace)
        self.namespace = namespace
        self.kwargs = kwargs
        self.metadata_store = self.metadata_store_class(namespace, **kwargs)

    # def namespace_exists(self) -> bool:
    #     """Returns True if the namespace for this instance exists"""
    #     return self.metadata_store.namespace_exists()

    # def get_all(self, query: dict, auth_token: str, include_invalid: bool = False) -> List[Metadata]:
    #     """Returns all metadata instances in summary form (name, display_name, location)"""

    #     if (self.namespace == self.NAMESPACE_CREDENTIAL_STORE) and (os.environ.get('UNSKRIPT_MODE') == None) :
    #         self.namespace = self.NAMESPACE_CREDENTIAL_SAVE
    #         self.metadata_store = self.metadata_store_class(self.namespace, **self.kwargs)

    #     instances = []
    #     instance_list = self.metadata_store.fetch_instances(include_invalid=include_invalid)
    #     for metadata_dict in instance_list:
    #         # validate the instance prior to return, include invalid instances as appropriate
    #         try:
    #             metadata = Metadata.from_dict(self.namespace, metadata_dict)
    #             metadata.post_load()  # Allow class instances to handle loads
    #             # if we're including invalid and there was an issue on retrieval, add it to the list
    #             if include_invalid and metadata.reason:
    #                 # If no schema-name is present, set to '{unknown}' since we can't make that determination.
    #                 if not metadata.schema_name:
    #                     metadata.schema_name = '{unknown}'
    #             else:  # go ahead and validate against the schema
    #                 self.validate(metadata.name, metadata)
    #             instances.append(metadata)
    #         except Exception as ex:  # Ignore ValidationError and others when fetching all instances
    #             # Since we may not have a metadata instance due to a failure during `from_dict()`,
    #             # instantiate a bad instance directly to use in the message and invalid result.
    #             invalid_instance = Metadata(**metadata_dict)
    #             self.log.debug("Fetch of instance '{}' of namespace '{}' encountered an exception: {}".
    #                            format(invalid_instance.name, self.namespace, ex))
    #             if include_invalid:
    #                 invalid_instance.reason = ex.__class__.__name__
    #                 instances.append(invalid_instance)


    #     if (self.namespace == self.NAMESPACE_CREDENTIAL_STORE) and (os.environ.get('UNSKRIPT_MODE') != None) :
    #         # For Credential Store, we want to retrieve the
    #         # List from backend, so reinitialize instances
    #         instances = []
    #         result = get_saas_connectors(query=query)
    #         temp_instance_list = json.loads(result)
    #         for v in temp_instance_list:
    #             m = Metadata()
    #             m.display_name = v['display_name']
    #             m.schema_name = v['schema_name']
    #             m.type = v['type']
    #             m.metadata = v['metadata']
    #             m.id = v['id']
    #             m.name = v['name']
    #             instances.append(m)
    #     elif (self.namespace == self.NAMESPACE_CONNECTOR_TYPE_LIST):
    #         if (os.environ.get('UNSKRIPT_MODE') != None):
    #             # For Credential Store, we want to retrieve the
    #             # List from backend, so reinitialize instances
    #             instances = []
    #             result = get_saas_connectors_types_list(query=query)
    #             connectors_types_list = json.loads(result)
    #             for v in connectors_types_list:
    #                 instances.append(Metadata.from_dict(self.namespace, v))
    #         else:
    #             instances = []
    #             body = {}
    #             result = credential_list(body)
    #             for v in result['metadata']['credentials']:
    #                 instances.append(Metadata.from_dict(self.namespace, v))
    #     elif (self.namespace == self.NAMESPACE_CREDENTIAL_LIST):
    #             instances = []
    #             body = {}
    #             result = credential_list(body)
    #             for v in result['metadata']['credentials']:
    #                 m = Metadata()
    #                 m.display_name = 'credential-list'
    #                 m.schema_name = v['name']
    #                 m.type = v['type']
    #                 m.metadata = v
    #                 instances.append(m)
    #     elif (self.namespace == self.NAMESPACE_CONNECTOR_LABELS_LIST) and (os.environ.get('UNSKRIPT_MODE') != None) :
    #         # For Credential Store, we want to retrieve the connector labels list from backend, so reinitialize instances
    #         instances = []
    #         result = get_saas_connectors_labels_list(query=query)
    #         connectors_labels_list = json.loads(result)
    #         for v in connectors_labels_list:
    #             instances.append(Metadata.from_dict(self.namespace, v))
    #     elif (self.namespace == self.NAMESPACE_RUNBOOK_LIST) and (os.environ.get('UNSKRIPT_MODE') != None):
    #         instances = []
    #         result = runbook_list(query, auth_token)
    #         for r in result['metadata']['runbooks']:
    #             m = Metadata()
    #             m.schema_name = 'runbook'
    #             m.name = r['name']
    #             m.display_name = r['name']
    #             m.id = r['id']
    #             m.metadata = r
    #             instances.append(m)
    #     elif (self.namespace == self.NAMESPACE_GET_RUNBOOK) and (os.environ.get('UNSKRIPT_MODE') != None):
    #         instances = []
    #         result = get_runbook(query, auth_token)
    #         m = Metadata()
    #         m.schema_name = 'get-runbook'
    #         m.name = result['metadata']['name']
    #         m.display_name = result['metadata']['name']
    #         m.id = result['metadata']['id']
    #         m.metadata = result['metadata']
    #         instances.append(m)

    #     return instances

    def get(self, name: str) -> Metadata:
        """Returns the metadata instance corresponding to the given name"""
        if name is None:
            raise ValueError("The 'name' parameter requires a value.")
        instance_list = self.metadata_store.fetch_instances(name=name)
        metadata_dict = instance_list[0]
        metadata = Metadata.from_dict(self.namespace, metadata_dict)

        # Validate the instance on load
        self.validate(name, metadata)

        # Allow class instances to alter instance
        metadata.post_load()

        return metadata

    # def create(self, name: str, metadata: Metadata) -> Metadata:
    #     """Creates the given metadata, returning the created instance"""
    #     return self._save(name, metadata)

    # def update(self, name: str, metadata: Metadata) -> Metadata:
    #     """Updates the given metadata, returning the updated instance"""
    #     return self._save(name, metadata, for_update=True)

    # def remove(self, name: str) -> None:
    #     """Removes the metadata instance corresponding to the given name"""

    #     instance_list = self.metadata_store.fetch_instances(name=name)
    #     metadata_dict = instance_list[0]

    #     self.log.debug("Removing metadata resource '{}' from namespace '{}'.".format(name, self.namespace))

    #     metadata = Metadata.from_dict(self.namespace, metadata_dict)
    #     metadata.pre_delete()  # Allow class instances to handle delete

    #     self.metadata_store.delete_instance(metadata_dict)

    def validate(self, name: str, metadata: Metadata) -> None:
        """Validate metadata against its schema.

        Ensure metadata is valid based on its schema.  If invalid or schema
        is not found, ValidationError will be raised.
        """
        metadata_dict = metadata.to_dict()
        schema_name = metadata_dict.get('schema_name')

        if not schema_name:
            raise ValueError("Instance '{}' in the {} namespace is missing a 'schema_name' field!".
                             format(name, self.namespace))

        schema = self._get_schema(schema_name)  # returns a value or throws
        try:
            validate(instance=metadata_dict, schema=schema, format_checker=draft7_format_checker)
        except ValidationError as ve:
            # Because validation errors are so verbose, only provide the first line.
            first_line = str(ve).partition('\n')[0]
            msg = "Validation failed for instance '{}' using the {} schema with error: {}.".\
                format(name, schema_name, first_line)
            self.log.error(msg)
            raise ValidationError(msg) from ve

    @staticmethod
    def _get_normalized_name(name: str) -> str:
        # lowercase and replaces spaces with underscore
        name = re.sub('\\s+', '_', name.lower())
        # remove all invalid characters
        name = re.sub('[^a-z0-9-_]+', '', name)
        # begin with alpha
        if not name[0].isalpha():
            name = 'a_' + name
        # end with alpha numeric
        if not name[-1].isalnum():
            name = name + '_0'
        return name

    def _get_schema(self, schema_name: str) -> dict:
        """Loads the schema based on the schema_name and returns the loaded schema json.
           Throws ValidationError if schema file is not present.
        """
        schema_json = self.schema_mgr.get_schema(self.namespace, schema_name)
        if schema_json is None:
            schema_file = os.path.join(os.path.dirname(__file__), 'schemas', schema_name + '.json')
            if not os.path.exists(schema_file):
                self.log.error("The file for schema '{}' is missing from its expected location: '{}'".
                               format(schema_name, schema_file))
                raise SchemaNotFoundError("The file for schema '{}' is missing!".format(schema_name))
            with io.open(schema_file, 'r', encoding='utf-8') as f:
                schema_json = json.load(f)
            self.schema_mgr.add_schema(self.namespace, schema_name, schema_json)

        return schema_json

    # def _save(self, name: str, metadata: Metadata, for_update: bool = False) -> Metadata:
        if not metadata:
            raise ValueError("An instance of class 'Metadata' was not provided.")

        if not isinstance(metadata, Metadata):
            raise TypeError("'metadata' is not an instance of class 'Metadata'.")

        if not name and not for_update:  # name is derived from display_name only on creates
            if metadata.display_name:
                name = self._get_normalized_name(metadata.display_name)
                metadata.name = name

        if not name:  # At this point, name must be set
            raise ValueError('Name of metadata was not provided.')

        match = re.search("^[a-z]([a-z0-9-_]*[a-z,0-9])?$", name)
        if match is None:
            raise ValueError("Name of metadata must be lowercase alphanumeric, beginning with alpha and can include "
                             "embedded hyphens ('-') and underscores ('_').")

        # Allow class instances to handle saves
        metadata.pre_save(for_update=for_update)

        temp_metadata = self._apply_defaults(metadata)

        # Validate the metadata prior to storage then store the instance.
        self.validate(name, metadata)

        if (self.namespace == "credential-store"):
            self.namespace = self.NAMESPACE_CREDENTIAL_SAVE

        metadata_dict = self.metadata_store.store_instance(name, metadata.prepare_write(), for_update=for_update)
        if (self.namespace == self.NAMESPACE_SAVE_AND_CLOSE):
            return metadata
        elif (self.namespace == self.NAMESPACE_LEGO_SAVE):
            return metadata
        elif (self.namespace == self.NAMESPACE_AUDIT_USER_ACTIVITY):
            return metadata
        elif (self.namespace == self.NAMESPACE_DELETE_LEGO):
            return metadata
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_SAVE):
            if (os.environ.get('UNSKRIPT_MODE') == None) :
                metadata.id=metadata_dict['id']
                # Code to create the aws directory and file
                if metadata_dict.get('type') == "CONNECTOR_TYPE_AWS":
                    create_aws_entry(name, metadata_dict)

            return metadata
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_DELETE):
            return metadata
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_STORE):
            return metadata
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_EDIT):
            return metadata
        return Metadata.from_dict(self.namespace, metadata_dict)

    # def _apply_defaults(self, metadata: Metadata) -> None:
        """If a given property has a default value defined, and that property is not currently represented,

        assign it the default value.
        """

        # Get the schema and build a dict consisting of properties and their default values (for those
        # properties that have defaults).  Then walk the metadata instance looking for missing properties
        # and assign the corresponding default value.  Note that we do not consider existing properties with
        # values of None for default replacement since that may be intentional (although those values will
        # likely fail subsequent validation).

        schema = self.schema_mgr.get_schema(self.namespace, metadata.schema_name)

        meta_properties = schema['properties']['metadata']['properties']
        property_defaults = {}
        for name, property in meta_properties.items():
            if 'default' in property:
                property_defaults[name] = property['default']

        if property_defaults:  # schema defines defaulted properties
            instance_properties = metadata.metadata
            for name, default in property_defaults.items():
                if name not in instance_properties:
                    instance_properties[name] = default

class TenantCredentials:
    tenant_url: str
    tenant_id: str
    proxy_id: str
    authorization_token: str

def get_tenants_credentials(query:dict) -> TenantCredentials:
    tenants_creds = TenantCredentials()
    tenants_creds.tenant_url = ''
    tenants_creds.tenant_id = ''
    tenants_creds.proxy_id = ''
    tenants_creds.authorization_token = ''

    globalENVNeeded = True
    if 'tenant_url' in query:
      tenants_creds.tenant_url = query['tenant_url'][0].decode("utf-8")
      globalENVNeeded = False
    if 'tenant_id' in query:
      tenants_creds.tenant_id  = query['tenant_id'][0].decode("utf-8")
      globalENVNeeded = False
    if 'proxy_id' in query:
      tenants_creds.proxy_id = query['proxy_id'][0].decode("utf-8")
      globalENVNeeded = False
    if 'authorization_token' in query:
      tenants_creds.authorization_token = query['authorization_token'][0].decode("utf-8")
      globalENVNeeded = False
    if globalENVNeeded:
      tenants_creds.tenant_url = os.environ.get('UNSKRIPT_TENANT_URL', 'https://app.unskript.io')
      tenants_creds.tenant_id  = os.environ.get('UNSKRIPT_TENANT_ID', '')
      tenants_creds.proxy_id = os.environ.get('UNSKRIPT_PROXY_ID', '')

    tenants_creds.authorization_token = os.environ.get('UNSKRIPT_CONNECTOR_TOKEN', '')
    unskript_mode = os.environ.get('UNSKRIPT_MODE', '')
    if unskript_mode != '':
        if tenants_creds.tenant_url == '':
            raise Exception("Tenant URL is Required!")
        if tenants_creds.tenant_id == '':
            raise Exception("Tenant ID is Required!")
        if tenants_creds.proxy_id == '':
            raise Exception("Proxy ID is Required!")
        if tenants_creds.authorization_token == '':
            raise Exception("Connector Token is Required!")

    return tenants_creds

# unSkript: To Handle SaaS Side Calling to get Credential Listing
def get_saas_connectors(query:dict) -> str:
    """
    get Method will fetch the list of connectors from unSkript SaaS side
    and returns back in the form of JSON the list of all available connectors.
    Sample output would be -
    {
        "respHdr": {
            "tid": "bc28e417-6ace-4e3d-a2d8-6c03ec8c98c0",
            "requestTid": "1234"
        },
        "connectors": [
            {
                "name": "new-name",
                "type": "CONNECTOR_TYPE_UNSPECIFIED",
                "environmentId": [
                    "5c5e810d-032e-4103-a7c3-317b922bf171"
                ],
                "id": "b3ce5dea-ca76-46d4-8732-897715960857",
                "tags": [
                    "aws-dev",
                    "stage"
                ],
                "createTime": "1970-01-01T00:00:00Z"
            },
            {
                "name": "aws-dev-connector",
                "type": "CONNECTOR_TYPE_AWS",
                "environmentId": [
                    "5c5e810d-032e-4103-a7c3-317b922bf171"
                ],
                "id": "1caaaeb4-d8ea-4ead-b692-a06ee529ddf3",
                "tags": [
                    "aws-dev",
                    "stage"
                ],
                "createTime": "1970-01-01T00:00:00Z"
            },
        // part of the response is hidden for readability
        ],
        "nextPageToken": "2"
    }
    """
    tenants_credentials = get_tenants_credentials(query)
    connector_path = 'v1alpha1/connectors'
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id': tenants_credentials.tenant_id, 'proxy_id': tenants_credentials.proxy_id}
    if query.get('user_id') != None:
        urldict['user_id'] = query.get('user_id')
    if query.get('filter') != None:
        urldict['filter'] = query.get('filter')
    url = '/'.join([tenants_credentials.tenant_url, connector_path])
    hdrtoken = "Unskript-SHA " + tenants_credentials.authorization_token
    hdr = {'Authorization': hdrtoken}
    result = []
    try:
        response = requests.get(url, headers=hdr, params=urldict)
    except requests.exceptions.RequestException as err:
        logging.error("Connect Request Exception: ",err)
        reason = {"reason": err}
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: ",errh)
        reason = {"reason": errh}
        return result
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: ",errc)
        reason = {"reason": errc}
        return result
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: ",errt)
        reason = {"reason": errt}
        return result
    except:
        # Default exception case, when nothing matches
        # Throw server error message
        logging.error("Server Error")
        reason = {"reason": "Server Error"}
        return result


    """
    response.json() should have the list of all connectors.
    Need to parse it and retrieve only relavant fields for
    the UI
    """
    data_text = response.json()
    for connector in data_text['connectors']:
        t = {}
        t['name'] = connector['name']
        connector.pop('name')
        t['type'] = connector['type']
        connector.pop('type')
        t['id'] = connector['id']
        connector.pop('id')
        t["metadata"] = {}
        for key in connector.keys():
            t["metadata"][key   ] = connector[key]
        t['schema_name'] = "credential-store"
        t['display_name'] = "Credential-store"
        result.append(t)

    return json.dumps(result)






# unSkript: To Handle SaaS Side Calling to get Connector Types List
def get_saas_connectors_types_list(query:dict) -> str:
    """
    get Method will fetch the list of connectors types from unSkript SaaS side
    and returns back in the form of JSON the list of all available connectors types.
    Sample output would be -
    {
    "respHdr": {
        "tid": "72455faf-7821-45c7-8049-2a536e118124",
        "requestTid": "1234"
    },
    "types": [
        "CONNECTOR_TYPE_JENKINS",
        "CONNECTOR_TYPE_KAFKA",
        "CONNECTOR_TYPE_MONGODB",
        "CONNECTOR_TYPE_GCP",
        "CONNECTOR_TYPE_POSTGRESQL",
        "CONNECTOR_TYPE_JIRA",
        "CONNECTOR_TYPE_K8S",
        "CONNECTOR_TYPE_MYSQL",
        "CONNECTOR_TYPE_GRAFANA",
        "CONNECTOR_TYPE_AWS",
        "CONNECTOR_TYPE_SLACK",
        "CONNECTOR_TYPE_REST",
        "CONNECTOR_TYPE_ELASTICSEARCH",
        "CONNECTOR_TYPE_GITHUB",
        "CONNECTOR_TYPE_NETBOX",
        "CONNECTOR_TYPE_NOMAD",
        "CONNECTOR_TYPE_CHATGPT",
        "CONNECTOR_TYPE_OPSGENIE"
    ]
}

    """

    tenants_credentials = get_tenants_credentials(query)
    connector_path = 'v1alpha1/connector-types'
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id': tenants_credentials.tenant_id, 'proxy_id': tenants_credentials.proxy_id}
    if "genai_supported" in list(query.keys()):
        urldict['genai_supported'] = True
    url = '/'.join([tenants_credentials.tenant_url, connector_path])
    hdrtoken = "Unskript-SHA " + tenants_credentials.authorization_token
    hdr = {'Authorization': hdrtoken}
    result = []

    try:
        response = requests.get(url, headers=hdr, params=urldict)
    except requests.exceptions.RequestException as err:
        logging.error("Connect Request Exception: ",err)
        reason = {"reason": err}
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: ",errh)
        reason = {"reason": errh}
        return result
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: ",errc)
        reason = {"reason": errc}
        return result
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: ",errt)
        reason = {"reason": errt}
        return result
    except:
        # Default exception case, when nothing matches
        # Throw server error message
        logging.error("Server Error")
        reason = {"reason": "Server Error"}
        return result


    """
    response.json() should have the list of all connectors types.
    Need to parse it and retrieve only relavant fields for
    the UI
    """
    data_text = response.json()
    for type in data_text['types']:
        t = {}
        t['schema_name'] = "connectors-types-list"
        t['type'] = type
        result.append(t)

    return json.dumps(result)

# Lego Search

# unSkript: To Handle SaaS Side Calling to get Connector Labels List
def get_saas_connectors_labels_list(query:dict) -> str:
    """
    get Method will fetch the list of connectors labels from unSkript SaaS side
    and returns back in the form of JSON the list of all the labels of service ID.
    Sample output would be -
    {
    "respHdr": {
        "tid": "72455faf-7821-45c7-8049-2a536e118124",
        "requestTid": "1234"
    },
    "values": [
        "service_id1",
        "service_id2",
        "service_id3"
    ]
}

    """
    tenants_credentials = get_tenants_credentials(query)
    connector_path = 'v1alpha1/connectors/labels'
    key = "service_id"
    if "label_type" in list(query.keys()):
        key = query['label_type'][0].decode("utf-8")
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id': tenants_credentials.tenant_id, 'proxy_id': tenants_credentials.proxy_id, "key": key}
    if query.get('filter') != None:
        urldict['filter'] = query.get('filter')
    if "type" in list(query.keys()):
        connecter_type_query = query.get("type")[0].decode('utf-8')
        urldict['type'] = connecter_type_query
    url = '/'.join([tenants_credentials.tenant_url, connector_path])
    hdrtoken = "Unskript-SHA " + tenants_credentials.authorization_token
    hdr = {'Authorization': hdrtoken}
    result = []
    try:
        response = requests.get(url, headers=hdr, params=urldict)
    except requests.exceptions.RequestException as err:
        logging.error("Connect Request Exception: ",err)
        reason = {"reason": err}
        return result
    except requests.exceptions.HTTPError as errh:
        logging.error("Http Error: ",errh)
        reason = {"reason": errh}
        return result
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting: ",errc)
        reason = {"reason": errc}
        return result
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error: ",errt)
        reason = {"reason": errt}
        return result
    except:
        # Default exception case, when nothing matches
        # Throw server error message
        logging.error("Server Error")
        reason = {"reason": "Server Error"}
        return result


    """
    response.json() should have the list of all connectors labels of service ID.
    Need to parse it and retrieve only relavant fields for
    the UI
    """
    data_text = response.json()
    for value in data_text['values']:
        t = {}
        t['schema_name'] = "connectors-labels-list"
        t["metadata"] = {}
        t["metadata"]["value"] = value
        t['display_name'] = "Connectors-Labels-List"
        result.append(t)

    return json.dumps(result)


def runbook_list(query:dict, auth_token: str) -> dict:
    """
    runbook_list method returns list of the runbooks.

    """
    tenants_creds = get_tenants_credentials(query)

    runbook_path = 'v1alpha1/workflows'
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'is_unskript':False}

    url = '/'.join([tenants_creds.tenant_url, runbook_path])
    hdr = {'Authorization': auth_token}
    response = requests.get(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Get Runbook List")
        reason = "reason: {}".format(response.raise_for_status())
        raise Exception(reason)

    data_text = response.json()

    runbooks = {}
    runbooks['schema_name'] = "runbook-list"
    metadata = {}
    metadata['runbooks'] = []
    for runbook in data_text['workflows']:
        runbooks_data = {}
        for key in runbook.keys():
            runbooks_data[key] = runbook[key]

        metadata['runbooks'].append(runbooks_data)

    runbooks['metadata'] = metadata
    return runbooks

def get_runbook(query:dict, auth_token: str) -> dict:
    """
    get_runbook method returns specific runbook.

    """
    tenants_creds = get_tenants_credentials(query)

    workflow_id = query['runbook_id'][0].decode("utf-8")
    runbook_path = 'v1alpha1/workflows/' + workflow_id
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenantId': tenants_creds.tenant_id}

    url = '/'.join([tenants_creds.tenant_url, runbook_path])
    hdr = {'Authorization': auth_token}
    response = requests.get(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Get Runbook", response.text)
        reason = "reason: {}".format(response.raise_for_status())
        raise Exception(reason)

    data_text = response.json()

    runbook = {}
    runbook['schema_name'] = "get-runbook"
    metadata = {}
    for key in data_text['workflow'].keys():
        metadata[key] = data_text['workflow'][key]

    runbook['metadata'] = metadata
    return runbook
