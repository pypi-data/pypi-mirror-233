##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import hvac
import base64
import json
import os

from unskript.legos.utils import UnskriptClient
from unskript.secrets.interface import SecretInterface

VAULT_SECRET_PREFIX = "VAULT_SECRET_PREFIX"
VAULT_HOST = "VAULT_HOST"
VAULT_TOKEN = "VAULT_TOKEN"
VAULT_MOUNT_DIR = "VAULT_MOUNT_DIR"
VAULT_KV_VERSION = "VAULT_KV_VERSION"

class VaultSecret(SecretInterface):
    def __init__(self, input_dict):
        if input_dict[VAULT_TOKEN] == "" or input_dict[VAULT_TOKEN] is None:
            try:
                client = UnskriptClient(os.environ['TENANT_URL'], os.environ['UNSKRIPT_TOKEN'])
                input_dict[VAULT_TOKEN] = client.fetch_vault_token()
            except Exception as e:
                print(f'Failed to fetch vault token: {str(e)}')
                raise Exception(f"unable to fetch vault token: {str(e)}")

        kv_version = input_dict.get(VAULT_KV_VERSION)
        if kv_version == "VAULT_KV_VERSION_1":
            self.vault_secret = VaultV1(input_dict)
        else:
            self.vault_secret = VaultV2(input_dict)

    def get_secret(self, connectorType:str, key:str)->str:
        return self.vault_secret.get_secret(connectorType, key)

class VaultV1(SecretInterface):
    def __init__(self, input_dict):
        host = input_dict.get(VAULT_HOST)
        token = input_dict.get(VAULT_TOKEN)
        self.client = hvac.Client(url=host, token=token)
        self.secretPrefix = input_dict.get(VAULT_SECRET_PREFIX)
        self.mountPoint = input_dict.get(VAULT_MOUNT_DIR)

    def get_secret(self, connectorType:str, key:str)->str:
        """
            Create the key based on how its stored in the secret store.
        """
        key = self.create_key(connectorType, key)
        try:
            secret_response = self.client.secrets.kv.v1.read_secret(
                path=key,
                mount_point=self.mountPoint,
            )
        except Exception as e:
            print(f'Get secret {key} failed')
            raise e
        if secret_response['data']['value'] is None:
            print(f'Secret {key} invalid format')
            raise Exception(f'Secret {key} invalid format')
        value = secret_response['data']['value']
        #Secrets are base64 encoded
        message_bytes = base64.b64decode(value)
        text_secret_data = json.loads(message_bytes.decode('ascii'))
        return text_secret_data
    """
    Creates the key based
    """
    def create_key(self, connectorType:str, key:str)->str:
        separator = "/"
        secretKeys = (self.secretPrefix, connectorType, key)
        return separator.join(secretKeys)

class VaultV2(SecretInterface):
    def __init__(self, input_dict):
        host = input_dict.get(VAULT_HOST)
        token = input_dict.get(VAULT_TOKEN)
        self.client = hvac.Client(url=host, token=token)
        self.secretPrefix = input_dict.get(VAULT_SECRET_PREFIX)
        self.mountPoint = input_dict.get(VAULT_MOUNT_DIR)

    def get_secret(self, connectorType:str, key:str)->str:
        """
            Create the key based on how its stored in the secret store.
        """
        key = self.create_key(connectorType, key)
        try:
            secret_response = self.client.secrets.kv.v2.read_secret_version(
                path=key,
                mount_point=self.mountPoint,
            )
        except Exception as e:
            print(f'Get secret {key} failed')
            raise e
        if secret_response['data']['data']['value'] is None:
            print(f'Secret {key} invalid format')
            raise Exception(f'Secret {key} invalid format')
        value = secret_response['data']['data']['value']
        #Secrets are base64 encoded
        message_bytes = base64.b64decode(value)
        text_secret_data = json.loads(message_bytes.decode('ascii'))
        return text_secret_data
    """
    Creates the key based
    """
    def create_key(self, connectorType:str, key:str)->str:
        separator = "/"
        secretKeys = (self.secretPrefix, connectorType, key)
        return separator.join(secretKeys)
