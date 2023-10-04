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
from abc import ABC
from abc import abstractmethod
from collections import OrderedDict
import copy
from faulthandler import disable
import io
import yaml
import json
import os
from textwrap import indent
import time
import requests
import logging
import uuid
import subprocess
# import persistent
# import transaction

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from pathlib import Path

import lazy_import

# jupyter_core = lazy_import.lazy_module('jupyter_core')

from traitlets import log  # noqa H306
from traitlets.config import LoggingConfigurable  # noqa H306
from traitlets.config import SingletonConfigurable
from traitlets.traitlets import Bool
from traitlets.traitlets import Integer
# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer

from unskript.secrets.elyra_metadata_error import MetadataNotFoundError
from unskript.secrets.elyra_metadata_error import MetadataExistsError
# from elyra.metadata.credential_schema import credential_schemas
from unskript.secrets.elyra_metadata_utils import is_aws_profile_present, read_krb_file, get_tenants_credentials

# Constants used in this file
CREDS_DIR = os.environ.get('HOME') + '/.local/share/jupyter/metadata/credential-save'

class MetadataStore(ABC):
    NAMESPACE_SAVE_AND_CLOSE = "save-and-close"
    NAMESPACE_LEGO_SAVE = "lego-save"
    NAMESPACE_AUDIT_USER_ACTIVITY = "audit-user-activity"
    NAMESPACE_LEGO_DELETE = "delete-lego"
    NAMESPACE_LEGO_LIST = "lego-list"
    NAMESPACE_GET_LEGO = "get-lego"
    NAMESPACE_LEGO_SEARCH = "lego-search"
    NAMESPACE_CREDENTIAL_LIST = "credential-list"
    NAMESPACE_GET_CREDENTIAL_SCHEMA = "get-credential-schema"
    NAMESPACE_GET_ENV_VARIABLE = "get-env-variable"
    NAMESPACE_CREDENTIAL_SAVE = "credential-save"
    NAMESPACE_CREDENTIAL_DELETE = "credential-delete"
    NAMESPACE_CREDENTIAL_EDIT = "credential-edit"
    NAMESPACE_LEGO_GENAI_CHAT = "lego-genai-chat"
    NAMESPACE_LEGO_GENAI_REQUEST_STATUS = "lego-genai-request-status"

    def __init__(self, namespace, parent = None, **kwargs):
        self.namespace = namespace
        self.log = parent.log if parent else log.get_logger()

    @abstractmethod
    def namespace_exists(self) -> bool:
        """Returns True if the namespace for this instance exists"""
        pass

    @abstractmethod
    def fetch_instances(self, name: Optional[str] = None, include_invalid: bool = False) -> List[dict]:
        """Fetch metadata instances"""
        pass

    # @abstractmethod
    # def store_instance(self, name: str, metadata: dict, for_update: bool = False) -> dict:
    #     """Stores the named metadata instance."""
    #     pass

    # @abstractmethod
    # def delete_instance(self, metadata: dict) -> None:
    #     """Deletes the metadata instance corresponding to the given name."""
    #     pass


def caching_enabled(func):
    """Checks if file store cache is enabled.  If not, just return, else perform function."""
    def wrapped(self, *args, **kwargs):
        if not self.enabled:
            return
        return func(self, *args, **kwargs)
    return wrapped


class FileMetadataCache(SingletonConfigurable):
    """FileMetadataCache is used exclusively by FileMetadataStore to cache file-based metadata instances.

    FileMetadataCache utilizes a watchdog handler to monitor directories corresponding to
    any files it contains.  The handler is primarily used to determine which cached entries
    to remove (on delete operations).

    The cache is implemented as a simple LRU cache using an OrderedDict.
    """

    max_size = Integer(min=1, max=1024, default_value=128, config=True,
                       help="The maximum number of entries allowed in the cache.")

    enabled = Bool(default_value=False, config=False,
                   help="Caching is enabled (True) or disabled (False).")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hits: int = 0
        self.misses: int = 0
        self.trims: int = 0
        self._entries: OrderedDict = OrderedDict()
        if self.enabled:  # Only create and start an observer when enabled
            self.observed_dirs = set()  # Tracks which directories are being watched
            self.observer = Observer()
            self.observer.start()

    def __len__(self) -> int:
        """Return the number of running kernels."""
        return len(self._entries)

    def __contains__(self, path: str) -> bool:
        return path in self._entries

    @caching_enabled
    def add_item(self, path: str, entry: Dict[str, Any]) -> None:
        """Adds the named entry and its entry to the cache.

        If this causes the cache to grow beyond its max size, the least recently
        used entry is removed.
        """
        md_dir: str = os.path.dirname(path)
        if md_dir not in self.observed_dirs and os.path.isdir(md_dir):
            self.observer.schedule(FileChangeHandler(self), md_dir, recursive=True)
            self.observed_dirs.add(md_dir)
        self._entries[path] = copy.deepcopy(entry)
        self._entries.move_to_end(path)
        if len(self._entries) > self.max_size:
            self.trims += 1
            self._entries.popitem(last=False)  # pop LRU entry

    @caching_enabled
    def get_item(self, path: str) -> Optional[Dict[str, Any]]:
        """Gets the named entry and returns its value or None if not present."""
        if path in self._entries:
            self.hits += 1
            self._entries.move_to_end(path)
            return copy.deepcopy(self._entries[path])

        self.misses += 1
        return None

    @caching_enabled
    def remove_item(self, path: str) -> Optional[Dict[str, Any]]:
        """Removes the named entry and returns its value or None if not present."""
        if path in self._entries:
            return self._entries.pop(path)

        return None


# class FileChangeHandler(FileSystemEventHandler):
#     """Watchdog handler that filters on .json files within specific metadata directories."""

#     def __init__(self, file_metadata_cache: FileMetadataCache, **kwargs):
#         super(FileChangeHandler, self).__init__(**kwargs)
#         self.file_metadata_cache = file_metadata_cache
#         self.log = file_metadata_cache.log

#     def dispatch(self, event):
#         """Dispatches delete and modification events pertaining to watched metadata instances. """
#         if event.src_path.endswith(".json"):
#             super(FileChangeHandler, self).dispatch(event)

#     def on_deleted(self, event):
#         """Fires when a watched file is deleted, triggering a removal of the corresponding item from the cache."""
#         self.file_metadata_cache.remove_item(event.src_path)

#     def on_modified(self, event):
#         """Fires when a watched file is modified.

#         On updates, go ahead and remove the item from the cache.  It will be reloaded on next fetch.
#         """
#         self.file_metadata_cache.remove_item(event.src_path)


class FileMetadataStore(MetadataStore):

    def __init__(self, namespace: str, **kwargs):
        super().__init__(namespace, **kwargs)
        self.cache = FileMetadataCache.instance()
        # if (self.namespace == self.NAMESPACE_CREDENTIAL_DELETE and (os.environ.get('UNSKRIPT_MODE') == None)):
        self.metadata_paths = FileMetadataStore.metadata_path()
        # self.metadata_paths = FileMetadataStore.metadata_path(self.NAMESPACE_CREDENTIAL_SAVE)
        # else:
        #     self.metadata_paths = FileMetadataStore.metadata_path(self.namespace)
        self.preferred_metadata_dir = self.metadata_paths[0]
        self.log.debug(f"Namespace '{self.namespace}' is using metadata directory: "
                       f"{self.preferred_metadata_dir} from list: {self.metadata_paths}")

    def namespace_exists(self) -> bool:
        """Does the namespace exist in any of the dir paths?"""
        namespace_dir_exists = False
        for d in self.metadata_paths:
            if os.path.isdir(d):
                namespace_dir_exists = True
                break
        return namespace_dir_exists

    def fetch_instances(self, name: Optional[str] = None, include_invalid: bool = False) -> List[dict]:
        """Returns a list of metadata instances.

        If name is provided, the single instance will be returned in a list of one item.
        """
        if not self.namespace_exists():  # namespace doesn't exist - return empty list
            print(f"DEBUG: Namespace '{self.namespace}' does not exist.")
            return []

        resources = {}
        all_metadata_dirs = reversed(self.metadata_paths)
        for metadata_dir in all_metadata_dirs:
            if os.path.isdir(metadata_dir):
                for f in os.listdir(metadata_dir):
                    path = os.path.join(metadata_dir, f)
                    if path.endswith(".json"):
                        if name:  # if looking for a specific instance, and this is not it, continue
                            if os.path.splitext(os.path.basename(path))[0] != name:
                                continue
                        try:
                            metadata = self._load_resource(path)
                        except Exception as ex:
                            if name:  # if we're looking for this instance, re-raise exception
                                raise ex from ex
                            # else create a dictionary from what we have if including invalid, else continue
                            if include_invalid:
                                metadata = {'name': os.path.splitext(os.path.basename(path))[0],
                                            'resource': path,
                                            'reason': ex.__class__.__name__}
                            else:
                                continue

                        if metadata.get('name') in resources.keys():
                            # If we're replacing an instance, let that be known via debug
                            self.log.debug("Replacing metadata instance '{}' from '{}' with '{}'."
                                           .format(metadata.get('name'),
                                                   resources[metadata.get('name')].get('resource'),
                                                   metadata.get('resource')))
                        resources[metadata.get('name')] = metadata

        if name:
            if name in resources.keys():  # check if we have a match.
                return [resources[name]]

            # If we're looking for a single metadata and we're here, then its not found
            raise MetadataNotFoundError(self.namespace, name)

        # We're here only if loading all resources, so only return list of values.
        return list(resources.values())

    # def store_instance(self, name: str, metadata: dict, for_update: bool = False) -> dict:
        """Store the named metadata instance

        Create is the default behavior, while updates are performed when for_update is True.
        """
        metadata_resource_name = '{}.json'.format(name)
        resource = os.path.join(self.preferred_metadata_dir, metadata_resource_name)

        # If the preferred metadata directory is not present, create it and note it.
        if not os.path.exists(self.preferred_metadata_dir):
            self.log.debug("Creating metadata directory: {}".format(self.preferred_metadata_dir))
            os.makedirs(self.preferred_metadata_dir, mode=0o700, exist_ok=True)
        # Prepare for persistence, check existence, etc.
        renamed_resource = None
        if (self.namespace == self.NAMESPACE_SAVE_AND_CLOSE) and (os.environ.get('UNSKRIPT_MODE') != None):
            try:
                result = saas_close(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_LEGO_SAVE):
            if (os.environ.get('UNSKRIPT_MODE') != None):
                try:
                    result = lego_save(metadata)
                except Exception as ex:
                    raise ex
                else:
                    return result
            else:
                result = lego_local_save(metadata)
                return result

        elif (self.namespace == self.NAMESPACE_AUDIT_USER_ACTIVITY and (os.environ.get('UNSKRIPT_MODE') != None)):
            try:
                result = audit_user_activity(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_LEGO_DELETE):
            try:
                result = delete_lego(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_LEGO_LIST and (os.environ.get('UNSKRIPT_MODE') != None)):
            try:
                result = legos_list(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_GET_LEGO) and (os.environ.get('UNSKRIPT_MODE') != None):
            try:
                result = get_lego(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_LEGO_SEARCH):
            if  (os.environ.get('UNSKRIPT_MODE') != None):
                try:
                    result = search_legos(metadata)
                except Exception as ex:
                    raise ex
                else:
                    return result
            else:
                # Opensource Docker version
                try:
                    result = db_search_legos(metadata)
                except Exception as ex:
                    raise ex
                else:
                    return result
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_LIST and (os.environ.get('UNSKRIPT_MODE') != None)):
            try:
                result = credential_list(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_GET_CREDENTIAL_SCHEMA):
            try:
                unskript_mode = False
                if os.environ.get('UNSKRIPT_MODE') != None:
                      unskript_mode = True
                result = credential_schema_get(metadata, unskript_mode=unskript_mode)
            except Exception as ex:
                raise ex
            else:
                return result
        elif (self.namespace == self.NAMESPACE_GET_ENV_VARIABLE):
            try:
                result = get_env_list(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif self.namespace == self.NAMESPACE_CREDENTIAL_SAVE:
            # If Configuring Kerberos schema for SSH then we need to make sure
            # krb5.conf should be updated
            # This should be done for both SaaS and Docker.
            if metadata.get('metadata').get('type') == 'CONNECTOR_TYPE_SSH':
                c_data = metadata.get('metadata').get('connectorData')
                c_data = json.loads(c_data)
                if c_data.get('authentication') and c_data.get('authentication').get('auth_type') == 'Kerberos':
                    try:
                        add_host_entries([c_data.get('authentication').get('kdc_server'),
                                         c_data.get('authentication').get('admin_server'),
                                         c_data.get('proxy_host')])
                        cfg = read_krb_file()
                        r = c_data.get('authentication').get('user_with_realm')
                        r = r.split('@')[-1]
                        add_new_realm(cfg,
                                    r,
                                    c_data.get('authentication').get('kdc_server'),
                                    c_data.get('authentication').get('admin_server'))
                        write_krb_file(cfg)
                    except Exception as e:
                        raise e

            if os.environ.get('UNSKRIPT_MODE') != None:
              try:
                 result = credential_save(metadata)
              except Exception as ex:
                  raise ex
              else:
                  return result
            else:
                # If credential type is K8S and EKS cluster is being used
                # we need to do the following checks
                #   1. If cluster is based of EKS and no AWS profile provided, then raise exception
                #   2. If AWS profile is provided and cluster is EKS based, but does not match
                #      existing credential profiles in ~/.aws/credentials, then raise an exception
                if metadata.get('metadata').get('type') == 'CONNECTOR_TYPE_K8S':
                    try:
                        check_yaml_file(metadata.get('metadata').get('connectorData'))
                    except Exception as e:
                        raise e

                metadata['display_name'] = metadata['metadata']['name']
                metadata['type'] = metadata['metadata']['type']
                metadata['id'] = str(uuid.uuid4())

        elif self.namespace == self.NAMESPACE_CREDENTIAL_DELETE:
            # If Configuring Kerberos schema for SSH then we need to make sure
            # krb5.conf should be updated
            if metadata.get('metadata').get('type') == 'CONNECTOR_TYPE_SSH':
                c_data = metadata.get('metadata').get('connectorData')
                c_data = json.loads(c_data)
                if c_data.get('authentication') and c_data.get('authentication').get('auth_type') == 'Kerberos':
                    try:
                        cfg = read_krb_file()
                        del_realm(cfg, c_data.get('authentication').get('realm'))
                        write_krb_file(cfg)
                    except Exception as e:
                        raise e
            if os.environ.get('UNSKRIPT_MODE') != None:
                try:
                    result = delete_credential(metadata)
                except Exception as ex:
                    raise ex
                else:
                    return result
            else:
                # Opensource Docker version
                try:
                    metadata['resource'] = resource
                    metadata['name']=name
                    result = self.delete_instance(metadata)
                except Exception as ex:
                    raise ex
                else:
                    return result
        elif (self.namespace == self.NAMESPACE_CREDENTIAL_EDIT and (os.environ.get('UNSKRIPT_MODE') != None)):
            try:
                result = edit_credential(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif self.namespace == self.NAMESPACE_LEGO_GENAI_CHAT:
            try:
                result = create_genai_chat_request(metadata)
            except Exception as ex:
                raise ex
            else:
                return result
        elif self.namespace == self.NAMESPACE_LEGO_GENAI_REQUEST_STATUS:
            result = {}
            result['schema_name'] = "lego-genai-request-status"
            result['display_name'] = "Lego GenAI Request Status"
            result['name'] = "lego-genai-request-status"
            result["metadata"] = {}
            response = get_genai_request_status(metadata)
            result['metadata'] = response
            return result
        else:
            if for_update:
                renamed_resource = self._prepare_update(name, resource)
            else:  # create
                self._prepare_create(name, resource)

        # Write out the instance
        try:
            self.log.debug("WRITE Resource is {resource}".format(resource=resource))
            with jupyter_core.paths.secure_write(resource) as f:
                f.write(json.dumps(metadata, indent=2))  # Only persist necessary items
        except Exception as ex:
            self._rollback(resource, renamed_resource)
            raise ex from ex
        else:
            self.log.debug("{action} metadata instance: {resource}".
                           format(action="Updated" if for_update else "Created", resource=resource))

        # Confirm persistence so in case there are issues, we can rollback
        metadata = self._confirm_persistence(resource, renamed_resource)

        return metadata

    # def delete_instance(self, metadata: dict) -> None:
        """Delete the named instance"""
        name = metadata.get('name')
        resource = metadata.get('resource')
        if resource and os.path.exists(resource):
            # Since multiple folders are in play, we only allow removal if the resource is in
            # the first directory in the list (i.e., most "near" the user)
            if not self._remove_allowed(metadata):
                self.log.error("Removal of instance '{}' from the {} namespace is not permitted!  "
                               "Resource conflict at '{}' ".format(name, self.namespace, resource))
                raise PermissionError("Removal of instance '{}' from the {} namespace is not permitted!".
                                      format(name, self.namespace))
            os.remove(resource)
            self.cache.remove_item(resource)

    # def _prepare_create(self, name: str, resource: str) -> None:
        """Prepare to create resource, ensure it doesn't exist in the hierarchy."""
        if os.path.exists(resource):
            self.log.error("An instance named '{}' already exists in the {} namespace at {}.".
                           format(name, self.namespace, resource))
            raise MetadataExistsError(self.namespace, name)

        # Although the resource doesn't exist in the preferred dir, it may exist at other levels.
        # If creating, then existence at other levels should also prevent the operation.
        try:
            resources = self.fetch_instances(name)
            # Instance exists at other (protected) level and this is a create - throw exception
            self.log.error("An instance named '{}' already exists in the {} namespace at {}.".
                           format(name, self.namespace, resources[0].get('resource')))
            raise MetadataExistsError(self.namespace, name)
        except MetadataNotFoundError:  # doesn't exist elsewhere, so we're good.
            pass

    # def _prepare_update(self, name: str, resource: str) -> str:
        """Prepare to update resource, rename current."""
        renamed_resource = None
        if os.path.exists(resource):
            # We're updating so we need to rename the current file to allow restore on errs
            renamed_resource = resource + str(time.time())
            os.rename(resource, renamed_resource)
            self.log.debug("Renamed resource for instance '{}' to: '{}'".format(name, renamed_resource))
        return renamed_resource

    # def _rollback(self, resource: str, renamed_resource: str) -> None:
        """Rollback changes made during persistence (typically updates) and exceptions are encountered """
        self.cache.remove_item(resource)  # Clear the item from the cache, let it be re-added naturally
        if os.path.exists(resource):
            os.remove(resource)
        if renamed_resource:  # Restore the renamed file
            os.rename(renamed_resource, resource)

    # def _confirm_persistence(self, resource: str, renamed_resource: str) -> dict:
        """Confirms persistence by loading the instance and cleans up renamed instance, if applicable."""

        # Prior to loading from the filesystem, REMOVE any associated cache entry (likely on updates)
        # so that _load_resource() hits the filesystem - then adds the item to the cache.
        self.cache.remove_item(resource)
        try:
            metadata = self._load_resource(resource)
        except Exception as ex:
            self.log.error("Removing metadata instance '{}' due to previous error.".format(resource))
            self._rollback(resource, renamed_resource)
            raise ex from ex

        if renamed_resource:  # Remove the renamed file
            os.remove(renamed_resource)
        return metadata

    # def _remove_allowed(self, metadata: dict) -> bool:
        """Determines if the resource of the given instance is allowed to be removed. """
        allowed_resource = os.path.join(self.preferred_metadata_dir, metadata.get('name'))
        current_resource = os.path.splitext(metadata.get('resource'))[0]
        return allowed_resource == current_resource

    def _load_resource(self, resource: str) -> Dict[str, Any]:
        # This is always called with an existing resource (path) so no need to check existence.

        metadata_json: Dict[str, Any] = self.cache.get_item(resource)
        if metadata_json is not None:
            self.log.debug(f"Loading metadata instance from cache: '{metadata_json['name']}'")
            return metadata_json

        # Always take name from resource so resources can be copied w/o having to change content
        name = os.path.splitext(os.path.basename(resource))[0]

        self.log.debug(f"Loading metadata instance from: '{resource}'")
        with io.open(resource, 'r', encoding='utf-8') as f:
            try:
                metadata_json = json.load(f)
            except ValueError as jde:  # JSONDecodeError is raised, but it derives from ValueError
                # If the JSON file cannot load, there's nothing we can do other than log and raise since
                # we aren't able to even instantiate an instance of Metadata.  Because errors are ignored
                # when getting multiple items, it's okay to raise.  The singleton searches (by handlers)
                # already catch ValueError and map to 400, so we're good there as well.
                self.log.error(f"JSON failed to load for resource '{resource}' in the "
                               f"{self.namespace} namespace with error: {jde}.")
                raise ValueError(f"JSON failed to load for instance '{name}' in the "
                                 f"{self.namespace} namespace with error: {jde}.") from jde

            metadata_json['name'] = name
            metadata_json['resource'] = resource
            self.cache.add_item(resource, metadata_json)

        return metadata_json

    @staticmethod
    def metadata_path(*subdirs):
        """Return a list of directories to search for metadata files.

        ELYRA_METADATA_PATH environment variable has highest priority.

        This is based on jupyter_core.paths.jupyter_path, but where the python
        env-based directory is last in the list, preceded by the system shared
        locations with the user's home-based directory still first in the list.

        The first directory in the list (data_dir, if env is not set) is where files
        will be written, although files can reside at other levels as well, with
        SYSTEM_JUPYTER_PATH representing shared data and ENV_JUPYTER_PATH representing
        the location of factory data (created during installation).

        If ``*subdirs`` are given, that subdirectory will be added to each element.
        """

        paths = [ CREDS_DIR, 
                 os.environ.get('HOME') + '/.unskript/credentials/.local/share/jupyter/metadata',
                 os.environ.get('HOME') + '/.unskript/credentials/.local/share/jupyter/metadata/credential-save' ]
        # highest priority is env
        if os.environ.get('ELYRA_METADATA_PATH'):
            paths.extend(
                p.rstrip(os.sep)
                for p in os.environ['ELYRA_METADATA_PATH'].split(os.pathsep)
            )
        # then user dir
        # paths.append(jupyter_core.paths.jupyter_data_dir())

        # system_path = jupyter_core.paths.SYSTEM_JUPYTER_PATH
        # paths.extend(system_path)

        # then sys.prefix, where installed files will reside (factory data)
        # env_path = jupyter_core.paths.ENV_JUPYTER_PATH
        # for p in env_path:
        #     if p not in system_path:
        #         paths.append(p)


        # add subdir, if requested.
        # Note, the 'metadata' parent dir is automatically added.
        if subdirs:
            paths = [os.path.join(p, 'metadata', *subdirs) for p in paths]

        return paths



# unSkript: To Handle SaaS Side Calling to save execution.
def saas_close(metadata:dict) -> dict:
    """
    close method makes a workflow save of saveAs request.
    Sample output would be -
    {
        "respHdr": {
            "tid": "942ae17e-785b-485b-aaf2-74f9ae030dd9",
            "requestTid": "1234"
        }
    }
    """
    tenants_creds = get_tenants_credentials(metadata, disable_token_check=False)

    workflow_path = 'v1alpha1/workflows'

    workflow_id = metadata['metadata']["workflow_id"]
    execution_id = ''
    url = metadata['metadata']["notebook_id"]

    if "execution_id" in metadata['metadata']:
        execution_id = metadata['metadata']["execution_id"]

    cancel = False
    if "cancel" in metadata['metadata']:
        cancel = metadata['metadata']["cancel"]

    if metadata['metadata'].__contains__("workflow_name"):
        workflow_name = metadata['metadata']["workflow_name"]
        workflow_description = metadata['metadata']["workflow_description"]
        urldict = {'req_hdr.tid': str(uuid.uuid4()), 'cancel':cancel, 'proxy_id': tenants_creds.proxy_id,'workflow_id':workflow_id , "execution_id":execution_id,'url':url,'workflow':{"name":workflow_name, "description":workflow_description, "proxy_id":tenants_creds.proxy_id}}
    else:
        urldict = {'req_hdr.tid': str(uuid.uuid4()), 'cancel':cancel,'proxy_id': tenants_creds.proxy_id,'workflow_id':workflow_id , "execution_id":execution_id,'url':url}

    params = {'tenant_id': tenants_creds.tenant_id}

    close = 'close'
    url = '/'.join([tenants_creds.tenant_url, workflow_path,  workflow_id , close])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    data = json.dumps(urldict)
    response = requests.post(url, headers=hdr, params=params, data=data)

    if response.ok == False:
        logging.error("Close xRunbook Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    result = json.loads(response._content.decode('utf-8'))
    return result



# unSkript: To Handle SaaS Side Calling to save lego.
def lego_save(body:dict) -> dict:
    """
    lego_save create lego.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    legos_path = 'v1alpha1/legos'

    lego = {}
    json_body = dict()
    for key in body['metadata'].keys():
        # because of lack of the standartization it happens that in dict could be camel and snake cases
        parts = key.split('_')
        camelKey = parts[0] + ''.join(x.title() for x in parts[1:])
        # should override value only when key is snake cased as extensions using it as source of truth
        if camelKey not in lego or key != camelKey:
            lego[camelKey] = body['metadata'][key]
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id}
    url = '/'.join([tenants_creds.tenant_url, legos_path])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    # If the lego is to be updated
    if "uuid" in body['metadata'].keys():
        urldict['proxy_id'] = tenants_creds.proxy_id
        urldict['lego'] = lego
        data = json.dumps(urldict)
        url += "/" + body['metadata']['uuid']
        response = requests.patch(url, headers=hdr, data=data)
        if response.ok == False:
            logging.error("Update Lego Error: " + response.text)
            reason = "reason: {}".format(response.raise_for_status())
            return reason
    # If the lego is to be created
    else:
        urldict['proxy_id'] = tenants_creds.proxy_id
        urldict['lego'] = lego
        data = json.dumps(urldict)
        response = requests.post(url, headers=hdr, data=data)
        if response.ok == False:
            logging.error("Create Lego Error: " + response.text)
            reason = "reason: {}".format(response.raise_for_status())
            return reason

    result = json.loads(response._content.decode('utf-8'))
    return result

# For local save of Legos for OSS Docker
def lego_local_save(body:dict) -> dict:
   import random
   """
   lego_local_save will create a new lego and respective
   json file for the lego
   """

   lego = {}

   # The Jupyter cell toolbar extension sends us the Snippet that was
   # Saved (using the lego->Three dots->Save-As) in the following format
   #
   #    {
   #      "display_name": "lego-save",
   #      "metadata": {
   #        "proxy_id": "",
   #        "tenant_id": "982dba5f-d9df-48ae-a5bf-ec1fc94d4882",
   #        "tenant_url": "https://tenant-staging.alpha.unskript.io",
   #        "actionBashCommand": false,
   #        "actionNeedsCredential": true,
   #        "actionOutputType": null,
   #        "actionRequiredLinesInCode": [],
   #        "actionSupportsIteration": false,
   #        "actionSupportsPoll": false,
   #        "action_modified": true,
   #        "name": "Custom Kubectl delete a pod4",
   #        "description": "Custom Lego 4",
   #        "language": "Python",
   #        "order_properties": [
   #          "k8s_cli_string",
   #          "pod_name",
   #          "namespace",
   #          "period"
   #        ],
   #        "action_is_check": true,
   #        "action_output_type": "ACTION_OUTPUT_TYPE_INT",
   #        "action_needs_credential": true,
   #        "action_supports_poll": true,
   #        "action_supports_iterator": true,
   #        "input_schema": "[{\"properties\":{\"k8s_cli_string\":{\"default\":\"kubectl delete pod {pod_name} -n {namespace}\",\"description\":\"kubectl delete a pod\",\"title\":\"Kubectl Command\",\"type\":\"string\"},\"namespace\":{\"default\":\"\",\"description\":\"Namespace\",\"title\":\"Namespace\",\"type\":\"string\"},\"period\":{\"default\":60,\"description\":\"Timeout\",\"title\":\"period\",\"type\":\"number\"},\"pod_name\":{\"default\":\"\",\"description\":\"Pod Name\",\"title\":\"Pod Name\",\"type\":\"string\"}},\"required\":[\"pod_name\",\"namespace\"],\"title\":\"custom_k8s_kubectl_delete_pod4\",\"type\":\"object\"}]",
   #        "code": [
   #          "from pydantic import BaseModel, Field",
   #          "",
   #          "from beartype import beartype",
   #          "@beartype",
   #          "def custom_k8s_kubectl_delete_pod4_printer(data: str):",
   #          "    if data is None:",
   #          "        print(\"Error while executing command\")",
   #          "        return",
   #          "",
   #          "    print (data)",
   #          "",
   #          "@beartype",
   #          "def custom_k8s_kubectl_delete_pod4(handle, k8s_cli_string: str, pod_name: str, namespace: str) -> str:",
   #          "    \"\"\"custom_k8s_kubectl_delete_pod4 executes the given kubectl command",
   #          "",
   #          "        :type handle: object",
   #          "        :param handle: Object returned from the Task validate method",
   #          "",
   #          "        :type k8s_cli_string: str",
   #          "        :param k8s_cli_string: kubectl delete pod {pod_name} -n {namespace}.",
   #          "",
   #          "        :type pod_name: str",
   #          "        :param pod_name: Pod Name.",
   #          "",
   #          "        :type namespace: str",
   #          "        :param namespace: Namespace.",
   #          "",
   #          "        :rtype: String, Output of the command in python string format or Empty String in case of Error.",
   #          "    \"\"\"",
   #          "    k8s_cli_string = k8s_cli_string.format(pod_name, namespace)",
   #          "    result = handle.run_native_cmd(k8s_cli_string)",
   #          "    if result is None or hasattr(result, \"stderr\") is False or result.stderr is None:",
   #          "        return None",
   #          "    return result.stdout",
   #          "",
   #          "",
   #          "task = Task(Workflow())",
   #          "(err, hdl, args) = task.validate(vars=vars())",
   #          "if err is None:",
   #          "    task.execute(custom_k8s_kubectl_delete_pod4, lego_printer=custom_k8s_kubectl_delete_pod4_printer, hdl=hdl, args=args)"
   #        ],
   #        "id": "89a8fa98-5367-4cda-88d8-361f07e8f93e",
   #        "type": "LEGO_TYPE_K8S",
   #        "tags": [],
   #        "input": [],
   #        "custom_cell": true
   #      },
   #      "schema_name": "lego-save",
   #      "type": null,
   #      "id": null
   #    }
   #  we need to traslate this into the code-snippet format. The lego dictionary is
   #  used to modify this tranlsation. In future we need to replace this with
   #  unskript Codesnippet & ActionSchema class Here is the JIRA ticket
   #  https://unskript.atlassian.net/browse/EN-4015

   try:
       lego['name'] = body.get('metadata').get('name')
       lego['description'] = body.get('metadata').get('description')
       lego['language'] = 'python'
       lego['type'] = body.get('metadata').get('type')
       lego['inputschema'] = json.loads(body.get('metadata').get('input_schema'))
       lego['code'] = body.get('metadata').get('code')
       lego['uuid'] = body.get('metadata').get('id')
       # Version is hardcoded
       lego['version'] = '1.0.0'
       # ID is generated as a random number between 10K and 10M
       lego['id'] = random.randrange(10000, 10000000)
       lego['tags'] = body.get('metadata').get('tags')
       lego['custom_cell'] = body.get('metadata').get('custom_cell')
       lego['orderProperties'] = body.get('metadata').get('order_properties')
       lego['metadata'] = {}
       lego['metadata']['action_title'] = body.get('metadata').get('name')
       lego['metadata']['action_description'] = body.get('metadata').get('description')
       lego['metadata']['action_type'] = body.get('metadata').get('type')
       lego['metadata']['action_version'] = lego['version']

       if body.get('metadata').get('action_main_function') != None:
           lego['metadata']['action_entry_function'] = str(body.get('metadata').get('action_main_function'))
       lego['metadata']['action_needs_credential'] = json.dumps(body.get('metadata').get('actionNeedsCredential'))
       lego['metadata']['action_supports_poll'] = json.dumps(body.get('metadata').get('actionSupportsPoll'))
       lego['metadata']['action_output_type'] = str(body.get('metadata').get('action_output_type'))
       lego['metadata']['action_supports_iteration'] = json.dumps(body.get('metadata').get('actionSupportsIteration'))
       lego['metadata']['action_bash_command'] = "false"
       # Handle both case if Json serializes, it would be True, if not it would be string value true
       if body.get('action_is_check') in (True, "true"):
            lego['metadata']['action_is_check'] = "true"
       else:
            lego['metadata']['action_is_check'] = "false"

   except Exception as e:
       print(f"Error when Updating Local LEGO {e}")
       pass

   # Now that we have snippet in place, lets add that to the database so it gets
   # visible in the Action->Search
   add_new_snippet(lego)

   json_data = {}
   try:
        json_data['action_title'] = body.get('metadata').get('name')
        json_data['action_description'] = body.get('metadata').get('description')
        json_data['action_type'] = body.get('metadata').get('type')
        json_data['action_entry_function'] = str(body.get('metadata').get('action_main_function'))
        if body.get('metadata').get('actionNeedsCredential') == True:
            json_data['action_needs_credential'] = True
        else:
            json_data['action_needs_credential'] = False
        json_data['action_output_type'] = str(body.get('metadata').get('action_output_type'))
        if body.get('metadata').get('action_is_check') == True:
            json_data['action_is_check'] = True
            json_data['action_next_hop']= [""]
            json_data['action_next_hop_parameter_mapping']= {}
        else:
            json_data['action_is_check'] = False
        json_data['action_supports_iteration'] = True
        json_data['action_supports_poll'] = True
   except:
        pass
   result = {}

   main_func = json_data.get('action_entry_function').replace("-","_")
   if main_func in ('', None):
       main_func = "awesome_custom_lego"

   # Custom directory path is now relative to /unskript directory
   custom_dir = "/unskript/data/custom/contrib/unskript/legos/" + main_func
   Path(custom_dir).mkdir(parents=True, exist_ok=True)

   # Generate .json file
   try:
      with open(custom_dir + "/" + main_func + ".json", "w") as f:
          f.write(json.dumps(json_data, indent=2))
   except Exception as e:
      print(f"Unable to create JSON File {e}")

    # Generate __init__.py file
   try:
      file = open( custom_dir + "/" + "__init__.py","w")
      file.close()
      # Make use of f string that will automatically format the input before
      # logging
      logging.info(f"Init file created {custom_dir}")
   except Exception as e:
      print(f"Unable to create __init__.py File {e}")

   # /tmp/ic.py - This file is where we store the Code from the code-snippet schema
   # /tmp/test.json - This file is where we convert the InputSchema JSON to python class
   #                all thanks to the datamodel-codegen utility
   # /tmp/schema.py - This is the Python file that is generated by running the datamodel-codegen
   #                utility.

   # Find out if the code snippet has InputSchema defined
   file_content = ''
   with open("/tmp/ic.py", "w") as f:
       for line in body.get('metadata').get('code'):
           file_content += line + '\n'
           f.write(line + '\n')
   input_schema = ''
   try:
       ischema = json.loads(body.get('metadata').get('input_schema'))[0]
       ischema['title'] = "InputSchema"
       input_schema = json.dumps(ischema, indent=2)
   except:
       pass


   if input_schema == '':
       print("DBG: Input Schema is not found in this Snippet")
   else:
       with open("/tmp/test.json", "w") as f:
           f.write(input_schema)

   # Generating Python class from a JSON is not a trivial task
   # Pydantic does not have a built in method that can be used to
   # get the class out. The recommend way of using it using
   # the utility called datamodel-codegen. As part of EN-3911 this
   # utility is already installed in the Docker builds. So we will

   # use this utility to generate the inputclass out of the json schema
   if os.path.exists("/tmp/test.json") == True:
       import subprocess
       cmd = ["datamodel-codegen", "--input", "/tmp/test.json", "--output", "/tmp/schema.py"]
       try:
           subprocess.check_output(cmd)
           print("Created Schema File")
       except Exception as e:
           print(f"DBG: Exception {e}")

   # Logic is simple:
   # 1. Create a temp file (/tmp/ic.py) to store the code from the code-snippet schema
   # 2. Dump the inputschema json to a file (/tmp/test.json)
   # 3. Run the datamodel-codegen utility to generate the python class (/tmp/schema.py)
   # 4. Create a new Code snippet py file from concatinating Schema.py and IC.py

   if os.path.exists("/tmp/schema.py") == True:
       print("Successfully Created Input Class")
       #Get copyright and import statements if any
       comments_and_imports = ''
       with open("/tmp/ic.py", "r") as f:
           for line in f.readlines():
               if line.startswith("#") == True:
                   comments_and_imports = comments_and_imports + line
               elif line.startswith("from beartype") == True:
                   pass
               elif line.startswith("import") == True or line.startswith("from") == True:
                   comments_and_imports = comments_and_imports + line
               else:
                   pass
               f.close()
       scontent = ''
       scontent = comments_and_imports+'\n'
       future_line_present = False
       future_line = ""
       #Get InputClass
       with open("/tmp/schema.py", "r") as k:
           for line in k.readlines():
               if line.startswith("#") == True:
                   pass
               elif line.startswith("from __future__") == True:
                   # This check is essential because datamodel-codegen inserts __future__
                   # line when it creates the file. We need to take notice of that and
                   # ensure we insert the future line at the begining of the file.
                   future_line_present = True
                   future_line = line
               else:
                   scontent = scontent + line
       fcontent = scontent + '\n'
       #Get code
       with open("/tmp/ic.py", "r") as f:
           for line in f.readlines():
               if line.startswith("#") == True:
                   pass
               elif line.startswith("import") == True or line.startswith("from") == True:
                   pass
               elif line.startswith("@beartype") == True:
                   pass
               elif line.startswith("task = Task") == True:
                   # If snippet has some task...lines, we need to remove it
                   # as the packaging will automatically add it.
                   break
               else:
                   fcontent = fcontent + line
               f.close()
       #Fetch the names and type of the input parameters to add to the README.md file
       with open("/tmp/ic.py", "r") as f:
           for line in f.readlines():
               if line.startswith("def ") == True:
                   check_for_parameters = re.findall(r'\((handle.*?)\)',line)
                   for param in check_for_parameters:
                    parameters = param
               else:
                   pass
       # Generate README.md file
       connector_type = json_data['action_type'].split("_")
       handle_type_value = connector_type[-1]
       try:
          with open(custom_dir + "/" + "README.md", "w") as r:
            r.write(f'[<img align="left" src="https://unskript.com/assets/favicon.png" width="100" height="100" style="padding-right: 5px">]\n(https://unskript.com/assets/favicon.png)\n<h1>{json_data["action_title"]}</h1>\n\n## Description\n{json_data["action_description"]}\n\n## Lego Details\n\t{main_func}({parameters})\n\t\thandle: Object of type unSkript {handle_type_value} Connector.\n\n\tPlease refer to README.md file of any existing lego and similarly add the description for your input parameters.\n\n\n## Lego Input\nThis Lego takes inputs handle,\n\n## Lego Output\nHere is a sample output.\n<img src="./1.png">\n\n## See it in Action\n\nYou can see this Lego in action following this link [unSkript Live](https://us.app.unskript.io)')
            r.close()
       except Exception as e:
          print(f"Unable to create README.md File {e}")
       try:
          with open(custom_dir + "/" + main_func + ".py", "w") as f:
              # If there is a __future__ line then python requires it to be the first line
              # in the python script. If we had a match of future_line, viz. future_line_present
              # then we just append it to the begining  of the snippet.
              if future_line_present == True:
                  new_content = future_line + '\n' + fcontent
                  fcontent = new_content
              f.write(fcontent)
       except Exception as e:
          print(f"Unable to create Py File {e}")

   else:
       print("Was not able to create Input Class")

   return result

# unSkript: To Handle SaaS Side Calling to audit user activity.
def audit_user_activity(body:dict) -> dict:
    """
    audit_user_activity audits user activity.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    audit_path = "v1alpha1/audit"
    audit = {}
    for key in body['metadata'].keys():
      audit[key] = body['metadata'][key]

    urldict = {}
    urldict["tenant_id"] = tenants_creds.tenant_id
    urldict["audit"] = audit
    url = '/'.join([tenants_creds.tenant_url, audit_path])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    data = json.dumps(urldict)
    response = requests.post(url, headers=hdr, data=data)

    if response.ok == False:
        logging.error("Audit User Activity Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    result = json.loads(response._content.decode('utf-8'))
    return result


# unSkript: To Handle SaaS Side Calling to save credential.
def credential_save(body:dict) -> dict:
    """
    credential_save create credential.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    connector_path = 'v1alpha1/connectors'

    splitted_string = tenants_creds.tenant_url.split("/")
    tenant_name = ""

    if len(splitted_string) == 3:
      tenant_name = splitted_string[2].split(".")[0]

    connector = {}
    for key in body['metadata'].keys():
        connector[key] = body['metadata'][key]
    connector["proxy_id"] = [tenants_creds.proxy_id]
    urldict = {'req_hdr.tid': str(uuid.uuid4()),'tenant_name': tenant_name,'tenant_id':tenants_creds.tenant_id, 'connector':connector}

    url = '/'.join([tenants_creds.tenant_url, connector_path])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    data = json.dumps(urldict)
    response = requests.post(url, headers=hdr, data=data)
    if response.ok == False:
        logging.error("Create Connector Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    result = json.loads(response._content.decode('utf-8'))
    return result


def delete_lego(body:dict) -> str:
    """
    delete_lego deletes a particular lego.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    legos_path = 'v1alpha1/legos'

    # TODO: FIX: UUID is id on SaaS  index is index in SaaS
    legos_id =body['metadata']['lego_id']
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id}

    url = '/'.join([tenants_creds.tenant_url, legos_path, legos_id])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.delete(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Delete Lego Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    return


def delete_credential(body:dict) -> str:
    """
    delete_credential deletes a particular credential.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    connectors_path = 'v1alpha1/connectors'

    credential_id =body['metadata']['id']
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id}

    url = '/'.join([tenants_creds.tenant_url, connectors_path, credential_id])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.delete(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Delete Credential Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    return


def edit_credential(body:dict) -> str:
    """
    edit_credential edits a particular credential.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    connectors_path = 'v1alpha1/connectors'

    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id}
    credential_id =body['metadata']['id']
    json_body = dict()

    if body['metadata'].get("connector_data"):
        json_body['connector_data'] = body['metadata']['connector_data']
    if body['metadata'].get("env"):
        json_body['env'] = body['metadata']['env']
    if body['metadata'].get("service_id"):
        json_body['service_id'] = body['metadata']['service_id']

    url = '/'.join([tenants_creds.tenant_url, connectors_path, credential_id])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.patch(url, headers=hdr,json=json_body, params=urldict)

    if response.ok == False:
        logging.error("Edit Credential Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    result = json.loads(response._content.decode('utf-8'))
    return result


def legos_list(body:dict) -> dict:
    """
    legos_list method returns list of the legos.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    legos_path = 'v1alpha1/legos'
    is_unskript =body['metadata']["is_unskript"]
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id, 'is_unskript':is_unskript}

    url = '/'.join([tenants_creds.tenant_url, legos_path])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.get(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("List Lego Error: " + response.text)
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    data_text = response.json()
    legos = {}
    legos['schema_name'] = "lego-list"
    metadata = {}
    metadata['legos'] = []
    for lego in data_text['legos']:
        legos_data = {}
        # SaaS Returns both Index (integer) and ID (string)
        # For Code-Snippet to work, we need to translate Index to ID
        # And skip ID.
        # SaaS Index == Code Snippet id
        lego['id'] = lego['index']
        for key in lego.keys():
            legos_data[key] = lego[key]

        metadata['legos'].append(legos_data)

    legos['metadata'] = metadata
    return  legos


def get_lego(body:dict) -> dict:
    """
    get_lego gets the details about a particular lego.

    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    legos_path = 'v1alpha1/legos'
    legos_id =body['id']
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id}

    url = '/'.join([tenants_creds.tenant_url, legos_path, legos_id])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.get(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Get Lego Error: " + response.text)
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    data_text = response.json()

    lego = {}
    metadata = {}
    lego['schema_name'] = "get-lego"

    # SaaS Index == Code Snippet id
    data_text['lego']['id'] = data_text['lego']['index']
    for key in data_text['lego'].keys():
        if key == 'id' or key == 'type' or key == 'name':
            lego[key] = data_text['lego'][key]
        else:
            metadata[key] = data_text['lego'][key]

    lego['metadata'] = metadata

    return lego

def search_legos(body:dict) -> dict:
    """
    search_legos method returns list of the legos matching searching text.
    """
    tenants_creds = get_tenants_credentials(body, disable_token_check=False)

    legos_path = 'v1alpha1/legos'
    search_text =body['metadata']["search_text"]
    spell_check_disabled=False
    if "spell_check_disabled" in body['metadata']:
        spell_check_disabled =body['metadata']["spell_check_disabled"]
    urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id, 'filter':search_text,'spell_check_disabled':spell_check_disabled}
    url = '/'.join([tenants_creds.tenant_url, legos_path])
    hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
    hdr = {'Authorization': hdrtoken}
    response = requests.get(url, headers=hdr, params=urldict)

    if response.ok == False:
        logging.error("Search Lego Error")
        reason = "reason: {}".format(response.raise_for_status())
        return reason

    data_text = response.json()

    legos = {}
    legos['schema_name'] = "lego-search"
    metadata = {}
    metadata['legos'] = []
    for lego in data_text['legos']:
        legos_data = {}
        # SaaS Index == Code Snippet id
        lego['action_uuid'] = lego['id']
        lego['id'] = lego['index']
        for key in lego.keys():
            if key in "inputSchema":
                if lego['inputSchema'] != "":
                    try:
                        legos_data['inputschema'] = json.loads(lego['inputSchema'])
                    except Exception as e:
                        logging.error(f"EXCEPTION ERROR: Invalid Input Schema {str(e)} {lego}")
                        legos_data['inputschema'] = []
            else:
                legos_data[key] = lego[key]
        metadata['legos'].append(legos_data)
    metadata['suggested']=data_text['suggested'] if 'suggested' in data_text else []
    legos['metadata'] = metadata
    return legos

def read_code_snippets() -> list:
    f = open("/var/unskript/code_snippets.json")
    cs = json.load(f)
    try:
        ret = cs.get('properties').get('snippets').get('default')
    except Exception:
        ret = []

    # Lets look for custom_snippets
    custom_snippets = []

    # Custom Legos directory is now relative to /unskript directory
    custom_snippets_file = "/unskript/data/custom/custom_snippets.json"

    if os.path.exists(custom_snippets_file) == True:
        custom_cs = {}
        with open(custom_snippets_file, "r") as f:
            custom_cs = json.load(f)
        try:
            custom_snippets = custom_cs.get('properties').get('snippets').get('default')
        except:
            pass

    if len(custom_snippets) > 0:
        ret = ret + custom_snippets

    return ret

def add_new_snippet(snippet):
    """
    When User has opened an existing runbook that already has the Legos created
    in it, We want to make sure our ZoDB is updated before we start adding
    the new snippet. Lets make sure ZoDB is properly initialized.
    """
    if not os.path.exists('/var/unskript/snippets.db'):
        if not os.path.exists('/var/unskript/code_snippets.json'):
            raise Exception("Code Snippets are Missing")
        snippets = read_code_snippets()
        if len(snippets) == 0:
            raise Exception("Error in  Code Snippets Packaging")
        storage = ZODB.FileStorage.FileStorage('/var/unskript/snippets.db')
        db = ZODB.DB(storage)
        store_snippets(db, snippets)
        print("Code Snippets Packaged")
    else:
        db =ZODB.DB('/var/unskript/snippets.db')
        print("Loading Packaged Snippets")

    connection = db.open()
    root = connection.root()
    all_snippets = root.get('unskript_cs')
    all_snippets.append(snippet)
    root['unskript_cs'] = all_snippets
    # transaction.commit()
    del root
    connection.close()
    db.close()

def store_snippets(db, snippets: List):
    connection = db.open()
    root = connection.root()
    # STORING AS TEXT INSTEAD OF OBJECT
    root['unskript_cs'] = snippets
    # transaction.commit()
    connection.close()

def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


# def get_search_rules():
    """get_search_rules is an abstraction used by reorder_results_per_rules
       This function reads the rule list and returns it back
    """
    # Static list as first step. These are the Names of the Legos
    # If the name changes, please make sure to update this list below.
    # Next enhancement would be to read it from a file rather than here.
    retval = ["k8s", "kubectl command", "run command via aws cli"]
    return retval

# def reorder_result_per_rules(result: list) -> list:
    rules = get_search_rules()
    matched_result = []
    unmatched_result = []
    for r in result:
        if r.get("name").lower().startswith(tuple(rules)):
            matched_result.append(r)
        else:
            unmatched_result.append(r)

    # Lets return Results that matched At the top and
    # unmatched to bottom of the list
    new_result = matched_result + unmatched_result

    return new_result

# def get_alias_words() -> dict:
    retval = {}
    # Right now this is a static list, next step is to make it to read
    # from yaml or json file
    retval["k8s"] = "kubectl"
    retval["kubernetes"] = "kubectl"
    retval["eks"] = "kubectl"

    return retval

# def db_search_legos(body:dict) -> dict:
    """
    db_search_legos method returns list of the legos matching searching text.
    """
    import os.path
    legos = {}
    search_text =body['metadata']["search_text"]
    search_text = search_text.lower()

    if not os.path.exists('/var/unskript/snippets.db'):
        if not os.path.exists('/var/unskript/code_snippets.json'):
            raise Exception("Code Snippets are Missing")
        snippets = read_code_snippets()
        if len(snippets) == 0:
            raise Exception("Error in  Code Snippets Packaging")
        storage = ZODB.FileStorage.FileStorage('/var/unskript/snippets.db')
        db = DB(storage)
        store_snippets(db, snippets)
        print("Code Snippets Packaged")
    else:
        db = DB('/var/unskript/snippets.db')

    connection = db.open()
    root = connection.root()
    cs = root.get('unskript_cs')

    data_text = {}
    ret = []

    # If short form search is used, like k8s or kubernetes
    # lets get alias words and then append keywords from known rules
    alias_words = {}
    alias_words = get_alias_words()
    if alias_words != {}:
        for k,v in alias_words.items():
            if k in search_text:
                search_text.replace(k, v)

    for s in cs:
        d = s
        # The Logic is very simple. First we create a word list comprised of
        # snippet name and description. Then we use the built-in all() function
        # and a list comprehension to perform a partial string search for each word
        # in the search text against the pre-existing string.
        #
        # The all() function in Python returns True if all elements of an iterable are true
        # (or if the iterable is empty), and False otherwise.
        snippet_texts =  d.get('name').lower() + ' ' + d.get('description').lower()
        if all(word in snippet_texts for word in search_text.split()) == True:
            # Append to List only if it is not present in ret
            if d not in ret:
                ret.append(d)

    ret = reorder_result_per_rules(ret)
    data_text['legos'] = ret


    legos['schema_name'] = "lego-search"
    metadata = {}
    metadata['legos'] = []
    lego_index = 1
    for lego in data_text['legos']:
        legos_data = {}
        # SaaS Index == Code Snippet id
        lego['action_uuid'] = lego.get('uuid') or str(lego_index)
        lego['id'] = lego_index
        lego['index'] = lego_index
        lego_index += 1
        for key in lego.keys():
            if key == "inputSchema":
                if lego['inputSchema'] != "":
                    try:
                        legos_data['inputschema'] = json.loads(lego['inputSchema'])
                    except Exception as e:
                        logging.error(f"EXCEPTION ERROR: Invalid Input Schema {str(e)} {lego}")
                        legos_data['inputschema'] = []
            #Special handling for metadata key. Metadata key content should be flattened out
            # and snake case should be converted to camelcase, as thats how payload from SaaS looks like.
            elif key == 'metadata':
                for key in lego.get('metadata').keys():
                    legos_data[to_camel_case(key)] = lego.get('metadata').get(key)
            else:
                legos_data[key] = lego[key]
        metadata['legos'].append(legos_data)
    legos['metadata'] = metadata

    del root
    connection.close()
    db.close()
    return legos

# For Credential Schema. This is a static list. If any new connector or credential is
# Added we will have to add that here.
cred_to_connector_mapping = {
  "AWS"              : "CONNECTOR_TYPE_AWS",
  "ElasticSearch"    : "CONNECTOR_TYPE_ELASTICSEARCH",
  "GCP"              : "CONNECTOR_TYPE_GCP",
  "Jenkins"          : "CONNECTOR_TYPE_JENKINS",
  "Jira"             : "CONNECTOR_TYPE_JIRA",
  "K8S"              : "CONNECTOR_TYPE_K8S",
  "Kafka"            : "CONNECTOR_TYPE_KAFKA",
  "MongoDB"          : "CONNECTOR_TYPE_MONGODB",
  "MySQL"            : "CONNECTOR_TYPE_MYSQL",
  "PostgreSQL"       : "CONNECTOR_TYPE_POSTGRESQL",
  "REST"             : "CONNECTOR_TYPE_REST",
  "SSH"              : "CONNECTOR_TYPE_SSH",
  "Slack"            : "CONNECTOR_TYPE_SLACK",
  "Datadog"          : "CONNECTOR_TYPE_DATADOG",
  "Github"           : "CONNECTOR_TYPE_GITHUB",
  "Grafana"          : "CONNECTOR_TYPE_GRAFANA",
  "Hadoop"           : "CONNECTOR_TYPE_HADOOP",
  "Kafka"            : "CONNECTOR_TYPE_KAFKA",
  "MSSql"            : "CONNECTOR_TYPE_MSSQL",
  "OpenSearch"       : "CONNECTOR_TYPE_OPENSEARCH",
  "Pingdom"          : "CONNECTOR_TYPE_PINGDOM",
  "Prometheus"       : "CONNECTOR_TYPE_PROMETHEUS",
  "Redis"            : "CONNECTOR_TYPE_REDIS",
  "Snowflake"        : "CONNECTOR_TYPE_SNOWFLAKE",
  "Splunk"           : "CONNECTOR_TYPE_SPLUNK",
  "Stripe"           : "CONNECTOR_TYPE_STRIPE",
  "Salesforce"       : "CONNECTOR_TYPE_SALESFORCE",
  "Zabbix"           : "CONNECTOR_TYPE_ZABBIX",
  "Netbox"           : "CONNECTOR_TYPE_NETBOX",
  "Nomad"            : "CONNECTOR_TYPE_NOMAD",
  "ChatGPT"          : "CONNECTOR_TYPE_CHATGPT",
  "Opsgenie"         : "CONNECTOR_TYPE_OPSGENIE"
}

# Credential List
# def credential_list(body:dict) -> dict:
#     """
#     credential_list method returns list of the known credentials.

#     """
#     result = {}

#     result['schema_name'] = "credential-list"
#     result['display_name'] = "Credential List"

#     metadata = {}
#     metadata['credentials'] = []

#     data = json.loads(credential_schemas)
#     schema_list = []
#     for entry in data:
#         schema_list.append(entry['title'])

#     for index in range(len(schema_list)):
#         cred = {}
#         cred['name'] = schema_list[index]
#         cred['type'] = cred_to_connector_mapping[schema_list[index].replace("Schema","")]
#         cred['schema'] = data[index]
#         metadata['credentials'].append(cred)

#     result['metadata'] = metadata
#     return  result


# Get Environment variable with value
def get_env_list(body:dict) -> dict:
    """
    get_env_list method will return value of a env variable if it is
    set. Else returns All UNSKRIPT* env variables that are set.
    """
    result = {}
    result['schema_name'] = "get-env-variable"
    result['display_name'] = "Get Environment List"

    try:
        env_search_name = body['metadata']["env_name"]
    except:
        env_search_name = ''


    metadata = {}
    metadata['environments'] = []

    if env_search_name == '':
        data = os.environ
        for i in data:
          if "UNSKRIPT" in i:
              metadata['environments'].append([i, data[i]])
    else:
        data = os.environ.get(env_search_name)
        metadata['environments'].append([env_search_name, data])

    result['metadata'] = metadata
    return result


# Credential Schema Get
def credential_schema_get(body:dict, unskript_mode:bool) -> dict:
    result = {}
    tenants_creds = {}
    disable_token_check = False
    if unskript_mode == False:
        disable_token_check = True

    tenants_creds = get_tenants_credentials(body,disable_token_check=disable_token_check)
    schema = Any
    connectors_path = 'v1alpha1/connectors/schemas'
    credential_type = body['metadata']['connector_type']
    if unskript_mode:
      urldict = {'req_hdr.tid': str(uuid.uuid4()), 'tenant_id':tenants_creds.tenant_id, 'connector_type': credential_type}
      url = '/'.join([tenants_creds.tenant_url, connectors_path])
      hdrtoken = "Unskript-SHA " + tenants_creds.authorization_token
      hdr = {'Authorization': hdrtoken}

      response = requests.get(url, headers=hdr, params=urldict)

      if response.ok == False:
          logging.error("Get Credential Schema Error")
          reason = "reason: {}".format(response.raise_for_status())
          return reason
      data_text = response.json()
      schema = data_text["schema"]
    else:
        data = json.loads(credential_schemas)
        connector_type_exist = False

        for connector_schema in data:
              title = ""
              title = connector_schema["title"]
              title = title.replace('Schema', '')
              title = title.upper()
              if "CONNECTOR_TYPE_"+title==credential_type:
                schema = json.dumps(connector_schema)
                connector_type_exist = True
                break

        if connector_type_exist == False:
          raise Exception("reason: connector type {} not exist".format(credential_type))

    result['schema_name'] = "get-credential-schema"
    result['display_name'] = "Credential Schema Get"
    result['name'] = "get-credential-schema"
    result['metadata'] = json.loads(schema)
    return result

# Private function to check if the given K8S YAML file
# We need to raise exception if AWS EKS is used and
#   1. If AWS Profile is missing from the K8S YAML file
#   2. If AWS Profile not matching existing aws credentials
# Or
# If we find out GKE is used then we raise exception
#   1. If GCP credentials are not configured prior to configuring K8S config
def check_yaml_file(file_content):
    content_dict = {}
    try:
        content_dict = yaml.safe_load(file_content)
    except Exception as e:
        raise e

    eks_in_use = False
    gke_in_use = False

    t = {}
    try:
        t = yaml.safe_load(content_dict.get('kubeconfig'))
        # We determine that the kubeconfig is using EKS by checking if the server
        # name ends eks.amazonaws.com. This is by default added by AWS. So if
        # EKS cluster is in use, we can assume this DNS entry to be present
        # for the server.
        for c in t.get('clusters'):
            if 'eks.amazonaws.com' in c.get('cluster').get('server'):
                eks_in_use = True
                break
        # One sure shot way of ensure the kubeconfig is of GKE origin is to check
        # command or the cmd-path. In case of command, there would be
        # google in it, in case of cmd-path, we would look for keyword
        # gke. cmd-path would be in user->auth-provider->cmd-path.
        # command would be in user->exec->command. We match only the
        # Data relavant to current-context
        # Here is a sample kubeconfig that shows both
        #
        # -- FOR cmd-path --
        # - name: gke_unskript-dev_us-west1-b_test-cluster
        # user:
        #   auth-provider:
        #      config:
        #      access-token: <ACCESS TOKEN>
        #      cmd-args: config config-helper --format=json
        #      cmd-path: /Users/jayasimharaghavan/Downloads/google-cloud-sdk/bin/gcloud
        #
        # -- FOR command --
        # - name: gke_unskript-dev_us-west1_trace
        # user:
        #   exec:
        #     apiVersion: client.authentication.k8s.io/v1beta1
        #     command: gke-gcloud-auth-plugin
        #     installHint: Install gke-gcloud-auth-plugin for use with kubectl by following
        #         https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke
        #     provideClusterInfo: true

        for u in  t.get('users'):
            if u.get('name') == t.get('current-context'):
                if u.get('user') and u.get('user').get('auth-provider') and \
                        u.get('user').get('auth-provider').get('cmd-path'):
                    if "google" in u.get('user').get('auth-provider').get('cmd-path'):
                        gke_in_use = True
                        break
                elif u.get('user') and u.get('user').get('exec') and \
                        u.get('user').get('exec').get('command'):
                    if "gke" in u.get('user').get('exec').get('command'):
                        gke_in_use = True
                        break

    except Exception as e:
        raise e

    profile = ''
    found = False
    if eks_in_use:
        if t.get('users') == None:
            # We dont find users section, flag it as error
            raise Exception("User section is missing in eks")
        for u in t.get('users'):
            try:
                exec_dict = {}
                # Lets make sure we have `user` section defined first
                if u.get('user') != None:
                    exec_dict = u.get('user').get('exec')

                # Next, Check if exec section exists
                if exec_dict != {}:
                    for k,v in exec_dict.items():
                        # It may happen no env line exist in the exec
                        # section, in that case profile will not be set
                        # Which will cause to raise an Exception later
                        # in the code
                        if k == 'env':
                            env_list = exec_dict.get('env')
                            # Lets check if env section is defined
                            if env_list != None:
                                for e in env_list:
                                    if e.get('name') == 'AWS_PROFILE':
                                        profile = e.get('value')
                                        break
                else:
                    # This is the case when other user configuration may be defined
                    # under the `users` sections. In that case we just dont interpret it
                    pass

            except Exception as e:
                raise e

        if profile != '':
            found =  is_aws_profile_present(profile)

            if found == False:
                raise Exception("AWS Profile used in Kubeconfig does not match the credentials configured")
        else:
            raise Exception("Kube Config for EKS Environment should have AWS_PROFILE defined")
    elif gke_in_use:
        gcp_creds_file = CREDS_DIR + '/gcpcreds.json'
        if os.path.exists(gcp_creds_file) is False:
            raise Exception("Since you are using GKE, please program the GCP credentials first")
        with open(gcp_creds_file, 'r', encoding='utf-8') as f:
            c = json.loads(f.read())
            if c.get('metadata') and c.get('metadata').get('connectorData') == "{}":
                raise Exception("GCP Credential is not configured. Please configure it before configure K8S Credentials")

        with open('/tmp/gcpcreds.json', 'w', encoding='utf-8') as f:
            cc_data = c.get('metadata').get('connectorData')
            cc_data = json.loads(cc_data).get('credentials')
            f.write(cc_data)

        auth_cmd = ['gcloud', 'auth', 'login', '--cred-file=/tmp/gcpcreds.json', "--quiet"]
        result = subprocess.run(auth_cmd, text=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            found = True
        else:
            raise Exception("Unable to Authenticate with please check gcp credentials.")

    return found
