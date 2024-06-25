import requests
import json


class RestDataLoader:
    def __init__(self, base_url: str = 'http://localhost:8203'):
        self.base_url = base_url

    def make_call(self, method: str, endpoint: str, **kwargs):
        url = self.base_url
        if not url.endswith('/') and not endpoint.startswith('/'):
            url += '/'
        url += endpoint
        resp = getattr(requests, method)(url, **kwargs)
        return resp

    def get_project(self, project_id: str = None, **kwargs):
        if project_id is None:
            return self.make_call('get', '/project', **kwargs)
        else:
            return self.make_call('get', f'/project/{project_id}', **kwargs)

    def get_resource(self, resource_id: str = None, **kwargs):
        if resource_id is None:
            return self.make_call('get', '/resource', **kwargs)
        else:
            return self.make_call('get', f'/resource/{resource_id}', **kwargs)

    def get_process(self, process_id: str = None, **kwargs):
        if process_id is None:
            return self.make_call('get', '/process', **kwargs)
        else:
            return self.make_call('get', f'/process/{process_id}', **kwargs)

    def get_workflow(self, workflow_id: str = None, **kwargs):
        if workflow_id is None:
            return self.make_call('get', '/workflow', **kwargs)
        else:
            return self.make_call('get', f'/workflow/{workflow_id}', **kwargs)


    def post_project(self, **kwargs):
        return self.make_call('post', '/project', **kwargs)

    def post_resource(self, **kwargs):
        return self.make_call('post', '/resource', **kwargs)

    def post_process(self, **kwargs):
        return self.make_call('post', '/process', **kwargs)

    def post_workflow(self, **kwargs):
        return self.make_call('post', '/workflow', **kwargs)


    def put_project(self, project_uid, **kwargs):
        return self.make_call('put', f'/project/{project_uid}', **kwargs)

    def put_resource(self, resource_uid, **kwargs):
        return self.make_call('put', f'/resource/{resource_uid}', **kwargs)

    def put_process(self, process_uid, **kwargs):
        return self.make_call('put', f'/process/{process_uid}', **kwargs)

    def put_workflow(self, workflow_uid, **kwargs):
        return self.make_call('put', f'/workflow/{workflow_uid}', **kwargs)

