# pylint: skip-file
#
##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

import json
import time
from typing import Any

import os
from urllib.parse import urlencode

from unskript.connectors.schema.rest import RESTSchema
from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.rest import RESTConnector


UNSKRIPT_REDIS_HOST_ENV_VARIABLE = "UNSKRIPT_REDIS_HOST"

EXECUTION_STATUS_UNSPECIFIED = "EXECUTION_STATUS_UNSPECIFIED"
EXECUTION_STATUS_IN_PROGRESS = "EXECUTION_STATUS_IN_PROGRESS"
EXECUTION_STATUS_SUCCEEDED = "EXECUTION_STATUS_SUCCEEDED"
EXECUTION_STATUS_FAILED = "EXECUTION_STATUS_FAILED"

EXECUTION_STATUS_POLL_INTERVAL = 5


class InfraConnector(ConnectorInterface):
    def __init__(self):
        # Redis host name can be configured via environment variable (for onprem case).
        self.host = os.getenv(UNSKRIPT_REDIS_HOST_ENV_VARIABLE,
                              "redis-master.redis.svc.cluster.local")
        self.db = 0
        self.ss_handle = None
        self.workflow = None
        self.tenant_url = os.environ["TENANT_URL"]
        self.sha_token = os.environ["UNSKRIPT_TOKEN"]

    def infra_create_redis_handle(self) -> Any:
        import redis
        from unskript.connectors.schema.redis import RedisSchema
        redisGreSQLCredential = RedisSchema(
            db=self.db, host=self.host, username=None, password=None, port=6379, use_ssl=False)

        try:
            pool = redis.ConnectionPool(host=redisGreSQLCredential.host,
                                        port=redisGreSQLCredential.port,
                                        db=redisGreSQLCredential.db)
            conn = redis.Redis(connection_pool=pool, ssl=redisGreSQLCredential.use_ssl, socket_connect_timeout=2,
                               decode_responses=True)
            conn.ping()
        except Exception as e:
            print("Exception while connecting to internal Redis")
            raise e

        return conn

    def infra_create_api_handle(self, tenant_id: str, proxy_id: str) -> RESTConnector:
        self.tenant_id = tenant_id
        self.proxy_id = proxy_id
        hdr = {"Authorization": f"unskript-sha {self.sha_token}"}
        restCredential = RESTSchema(
            base_url=self.tenant_url, username="", password="", headers=hdr)

        try:
            s = RESTConnector().get_handle(data={'base_url': self.tenant_url, 'headers': hdr})
        except Exception as e:
            print("Exception while connecting to internal API")
            raise e

        return s

    def infra_execute_runbook(self, runbook_id: str, runbook_params: str) -> str:
        run_workflow_req_body = {
            "tenant_id": self.tenant_id,
            "proxy_id": self.proxy_id,
            "workflow_id": runbook_id,
            "params": runbook_params,
            "user_id": "Bot-user"
        }

        resp = None
        try:
            resp = self.execute_runbook_api_handle.request(method='POST',
                url=f"/v1alpha1/workflows/{runbook_id}/run",
                data=json.dumps(run_workflow_req_body))
            
            resp.raise_for_status()
        except Exception as e :
            raise Exception(f'Execute runbook error: {e}') 
        
        execution_id = ''
        try:
            output = resp.json()
            execution_id = str(output.get('executionIds')[0])
        except Exception as e :
            raise Exception(f'Get execution id from response: {e}')
        
        execution_status = self.infra_poll_execution_status(execution_id=execution_id)
        return execution_status
    
    def infra_poll_execution_status(self, execution_id: str) -> str:
        execution_status = EXECUTION_STATUS_UNSPECIFIED
        while execution_status in [EXECUTION_STATUS_UNSPECIFIED, EXECUTION_STATUS_IN_PROGRESS]:
            resp = None
            try:
                resp = self.execute_runbook_api_handle.request(
                    method='GET',
                    url=f"/v1alpha1/executions/{execution_id}",
                    params=urlencode(dict(tenant_id=self.tenant_id)))
                
                resp.raise_for_status()
            except Exception as e :
                raise Exception(f'Get execution error: {e}') 
            
            try:
                output = resp.json()
                execution_status = str(output.get('execution').get('executionStatus'))
            except Exception as e:
                raise Exception(f'Get execution status from response: {e}')
            
            time.sleep(EXECUTION_STATUS_POLL_INTERVAL)
            
        
        return execution_status

    def get_handle(self, workflow) -> Any:

        self.ss_handle = self.infra_create_redis_handle()
        self.execute_runbook_api_handle = self.infra_create_api_handle(
            workflow.env["TENANT_ID"], workflow.env["PROXY_ID"])
        self.workflow = workflow
        return self

    def get_state_store_handle(self):
        return self.ss_handle

    def done(self, rc):
        self.workflow.Done(rc)

    def get_workflow_uuid(self):
        return self.workflow.get_workflow_uuid()

    def set_workflow_key(self, k, v):
        return self.ss_handle.set(k, v)

    def get_workflow_key(self, k):
        return self.ss_handle.get(k)

    def del_workflow_key(self, k):
        return self.ss_handle.delete(k)

    def upd_workflow_key(self, k, v):
        return self.ss_handle.set(k, v)

    def append_workflow_key(self, k, v):
        return self.ss_handle.append(k, v)

    def rename_workflow_key(self, old_key, new_key):
        return self.ss_handle.rename(old_key, new_key)

    def execute_runbook(self, runbook_id: str, runbook_params: str) -> str:
        return self.infra_execute_runbook(runbook_id=runbook_id, runbook_params=runbook_params)
