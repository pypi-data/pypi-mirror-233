import os

from urllib import request, parse

from datetime import datetime
from typing import (
    Text,
    Any,
    Sequence,
)

import logging
import uuid

import json

from abc import ABC, abstractmethod

from wells_data_pipeline_cores.services.cores import AzAuthzService

from wells_data_pipeline_cores.commons import EnvVariables, Utils


# Abstract class
#
# https://learn.microsoft.com/en-us/azure/databricks/dev-tools/service-principals
# https://learn.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/service-principals
# https://docs.databricks.com/api/azure/workspace/tokens/create
# https://realpython.com/urllib-request/
# 
class DbxTokenService(ABC):
    
    def __init__(self, env_vars:EnvVariables, conf_name:str="default"):
        self.env_vars = env_vars
        self.dbutils = env_vars.secret_utils.dbutils

        self.az_auth = AzAuthzService(env_vars=self.env_vars)

    def get_dbx_token(self, dbx_url:str, client_id:str=None, client_secret:str=None):
        """
        
        """
        try:
            #ID for Azure Databricks
            az_databricks_scope = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

            _client_id = self.env_vars.az_app_conf.get_client_id()
            _client_secret = self.env_vars.az_app_conf.get_client_secret()
            _tenant_name = self.env_vars.az_app_conf.get_tenant_name()

            az_auth_token = self.az_auth.get_sp_access_token(
                client_id=str(client_id or _client_id),
                client_credential=str(client_secret or _client_secret),
                tenant_name=_tenant_name,
                scopes=[az_databricks_scope]
            )

            print(az_auth_token)

            dbx_token_url = dbx_url + "/api/2.0/token/create"
            logging.warning("DbxTokenService() - dbx_token_url: ", dbx_token_url)

            headers = {
                'Authorization': 'Bearer ' + az_auth_token,
                'Content-Type': 'application/json'
            }

            data = {
                "lifetime_seconds": 0,
                "comment": "dbx token"
            }

            data = parse.urlencode(data).encode()
            req = request.Request(url=dbx_token_url, data=data, headers=headers)

            response = request.urlopen(req)

            return response.json()
        except Exception as ex:
            logging.warning("DbxTokenService() - get_dbx_token - error: %s", ex)

        return {}



