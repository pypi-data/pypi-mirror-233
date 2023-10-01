import logging
from pathlib import Path
from decouple import config
from typing import Any, Text

try:
    from azure.identity import DefaultAzureCredential, AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
except:
    logging.warning("missing azure.identity")

try:
    from azure.keyvault.secrets import SecretClient
except:
    logging.warning("missing azure-keyvault-secrets")

class SecretUtils(object):
    def __init__(self, dbutils = None, keyvault_name: Text = ""):
        self.keyvault_name = keyvault_name
        self.dbutils = dbutils
        self.az_keyvault_utils = AzKeyVaultUtils(keyvault_name=keyvault_name)

    def get_secret(self, key_name: Text):
        try:
            if self.dbutils:
                logging.info(f"SecretUtils::get_secret - dbutils.secrets - scope:{self.keyvault_name} - key: {key_name}")
                return self.dbutils.secrets.get(scope=self.keyvault_name, key=key_name)
            else:
                secret_value = LocalSecretUtils.get_secret(key_name=key_name)
                
                if secret_value is None or len(secret_value) == 0: # checking if secret_value is empty
                    secret_value = self.az_keyvault_utils.get_secret(key_name=key_name)
                    #print(f"AzKeyVaultUtils-{key_name} - {secret_value}")
                    return secret_value
                else:
                    #print(f"LocalSecretUtils-{key_name} - {secret_value}")
                    return secret_value
        except Exception as error:
            #print(error)
            logging.warning('SecretUtils - get_secret() Execution error: %s', error)
        
        return ""

class LocalSecretUtils(object):
    @staticmethod
    def get_secret(key_name: Text):
        contents = ""

        # If there is no key_value in .keyvaults folder, Try to load key_value from system environment
        try:
            # How does it work? - https://pypi.org/project/python-decouple/#toc-entry-12
            contents = config(key_name, default='')
        except Exception as error:
            logging.warning('LocalSecretUtils - get_secret() Execution error: %s', error)
            contents = ""
                
        return contents

class AzKeyVaultUtils(object):
    def __init__(self, keyvault_name: Text = ""):
        self.keyvault_name = keyvault_name
        self.secret_client  = None

        self._init_secret_client()
    
    def _init_secret_client(self):
        try:
            managed_identity = ManagedIdentityCredential()
            azure_cli = AzureCliCredential()
            default_credential = DefaultAzureCredential()

            credential_chain = ChainedTokenCredential(azure_cli, managed_identity, default_credential)

            self.secret_client = SecretClient(vault_url=f"https://{self.keyvault_name}.vault.azure.net", credential=credential_chain)
            
        except Exception as ex:
            #print(ex)
            logging.warning('AzKeyVaultUtils - _init_secret_client() Execution error: %s', ex)

    def get_secret(self, key_name: Text):
        contents = ""
        try:
            if self.secret_client is not None:
                _secret = self.secret_client.get_secret(key_name)
                contents = _secret.value
        except Exception as ex:
            #print(ex)
            logging.warning('AzKeyVaultUtils - get_secret() Execution error: %s', ex)

        return contents