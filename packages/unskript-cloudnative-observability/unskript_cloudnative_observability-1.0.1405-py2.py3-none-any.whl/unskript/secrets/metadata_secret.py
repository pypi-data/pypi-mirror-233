#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
#
#
import os
import json
import configparser

## remove this once elyra is available in the base image
from unskript.secrets.elyra_metadata_manager import MetadataManager
from unskript.secrets.elyra_metadata_storage import FileMetadataStore
from unskript.secrets.elyra_metadata_error import MetadataNotFoundError

from unskript.secrets.interface import SecretInterface

"""
MetadataSecretStore Class is a wrapper around elyra metadata. This
uses metadatamanger and metadatastore internally to get the required
API key. Please make sure you have the unskript-elyra package installed.
"""
class MetadataSecretStore():
    def __init__(self, input_dict):
        self.cred_name = input_dict.get('name')
        self.namespace = 'credential-save'
         

    """
    get_secret takes in the credential name (in string), interfaces with
    elyra metadata to search through the existing credentials stored in
    the credential-store namespace. Returns credential-value once the key
    is found to match an existing record.
    """
    def get_secret(self, key: str) -> dict:
        mdCredMgrStorage = FileMetadataStore(namespace=self.namespace)
        metadata_manager = MetadataManager(namespace=self.namespace,
                                            store=mdCredMgrStorage)

        try:
            runtime_config = metadata_manager.get(key).to_dict()
        except MetadataNotFoundError as e:
                print("DEBUG: No Matching Key Found ", key)
                raise e
        except Exception as e:
            print("DEBUG: No Matching Key Found ", key)
            raise e       

        try:
            # Since elyra has moved from use snake case to camelcase
            # we need to look at connectorData instead of connector_data
            cred_obj = runtime_config['metadata']['connectorData']
            cred_data = json.loads(cred_obj)
            c_type = runtime_config.get('metadata').get('type') 
            if c_type == 'CONNECTOR_TYPE_AWS':
                creds_dir = os.environ.get('HOME').strip() + '/.aws'
                creds_file = creds_dir + '/credentials'
                creds_file = creds_file.strip()
                if not os.path.exists(creds_dir):
                    os.mkdir(creds_dir)
                
                config = configparser.ConfigParser()

                if not os.path.exists(creds_file):
                    data = {}
                    if cred_data.get('authentication').get('auth_type') == 'Access Key':
                        p_name = runtime_config.get('metadata').get('name').strip()
                        config.add_section(p_name)
                        config.set(p_name, 'aws_access_key_id', cred_data.get('authentication').get('access_key'))
                        config.set(p_name, 'aws_secret_access_key', cred_data.get('authentication').get('secret_access_key'))
                        with open(creds_file, 'w') as f:
                            config.write(f)
                else:
                    try:
                        config.read(creds_file)
                        profile_name = runtime_config.get('metadata').get('name')
                        if profile_name not in config.sections():
                            temp_config = configparser.ConfigParser()
                            temp_config.add_section(profile_name)
                            temp_config.set(profile_name, 'aws_access_key_id', cred_data.get('authentication').get('access_key'))
                            temp_config.set(profile_name, 'aws_secret_access_key', cred_data.get('authentication').get('secret_access_key'))
                            with open(creds_file, 'w') as f:
                                temp_config.write(f)
                    except:
                        pass
 
        except Exception as e:
            print("DEBUG: Credential was not set")
            raise e

        return json.loads(cred_obj)
