import json
import re
import os
import requests

from copy import deepcopy
from typing import List, Optional, Dict, Union

# from handlers import BaseDatabaseInteractor
from handlers import BaseHandler
from models import Resource, ResourceFilter


class ResourceHandler(BaseHandler):
    save_filename: Optional[str] = None
    _resources: Optional[List[Resource]] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.save_filename = 'resources.json'
        self._resources = None

    @property
    def resources(self) -> List[Resource]:
        if self._resources is None:
            self.load()
        return self._resources

    @property
    def save_file_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)

    def load(self) -> None:
        if os.path.exists(self.save_file_path):
            data = [Resource.build(r) for r in self.load_file(self.save_file_path)]
        else:
            data = []
        self._resources = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [r.put() for r in self.resources]
        self.save_file(self.save_file_path, content)

    def create(self, resource: Resource) -> Resource:
        resources = self.resources
        new_resource = Resource.build(resource.put())
        new_resource.id = len(resources)
        resources.append(new_resource)
        self.save()
        return new_resource

    def filter(self, resource_filter: ResourceFilter) -> List[Resource]:
        resources = self.resources
        resources = resource_filter.filter_results(resources)
        return resources

    def update(self, resource: Resource) -> Resource:
        resources = self.filter(ResourceFilter(uid=[resource.uid]))

        if len(resources) == 0:
            raise IndexError(f"Resource with uid {resource.uid} not found")
        elif len(resources) > 1:
            raise IndexError(f"Resource with uid {resource.uid} returns multiple results")

        updated_resource = self.filter(resource_filter=ResourceFilter(uid=[resource.uid]))[0]
        updated_resource.update(resource)
        self.resources[updated_resource.id] = updated_resource
        self.save()
        return deepcopy(resource)

    def delete(self, resource_uid: int) -> Resource:
        resources = self.filter(ResourceFilter(uid=[resource_uid]))

        if len(resources) == 0:
            raise IndexError(f"Resource with uid {resource_uid} not found")
        elif len(resources) > 1:
            raise IndexError(f"Resource with uid {resource_uid} returns multiple results")

        delete_resource = self.filter(resource_filter=ResourceFilter(uid=[resource_uid]))[0]
        delete_resource.delete()
        self.resources[delete_resource.id] = delete_resource
        self.save()
        return deepcopy(delete_resource)

    def export_resources(self) -> Dict:
        resources = self.filter(ResourceFilter())
        return {'resources': [p.put() for p in resources]}

    def import_resources(self, dct) -> List[Resource]:
        self._resources = []
        resources = self.resources
        output = []
        print(json.dumps(dct, indent=4))
        for resource_dct in dct['resources']:
            resource = Resource.build(resource_dct)
            output.append(resource)
            resources.append(resource)
        
        self.save()
        return output