# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .api import Api
import json


class Client(object):

    def __init__(self, base_url, username=None, password=None, api_version='v1'):
        self.api = Api(base_url, username, password, api_version)

    def check_dag_status(self, dag_id=None):
        resource = '/dags/%s' % dag_id if dag_id else '/dags'
        res = self.api.send(method='get', resource=resource)
        return res

    def trigger_dag_run(self, dag_id, conf, dag_run_id=None, logical_date=None):
        data = {"conf": conf}
        if dag_run_id:
            data['dag_run_id'] = dag_run_id
        if logical_date:
            data['logical_date'] = logical_date
        resource = '/dags/%s/dagRuns' % dag_id
        res = self.api.send(method='post', resource=resource, data=data)
        return res

    def list_DAG_runs(self, dag_id):
        resource = '/dags/%s/dagRuns' % dag_id if dag_id else '/dags/~/dagRuns'
        res = self.api.send(method='get', resource=resource)
        return res
