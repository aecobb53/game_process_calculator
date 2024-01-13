import json
import re
import os
import requests

from typing import List, Optional, Dict, Union

from handlers import BaseDatabaseInteractor
from models import Resource, ResourceFilter


class ResourceHandler(BaseDatabaseInteractor):
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
            data = [Resource.build(p) for p in self.load_file(self.save_file_path)]
        else:
            data = []
        self._resources = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [p.put() for p in self.resources]
        self.save_file(self.save_file_path, content)

    def create(self, resource: Resource) -> Resource:
        resources = self.resources
        resource.id = len(resources)
        resources.append(resource)
        self.save()
        return resource

    def filter(self, resource_filter: ResourceFilter) -> List[Resource]:
        resources = self.resources
        resources = resource_filter.filter_results(resources)
        return resources

    def update(self, resource: Resource) -> None:
        old_resource = self.filter(resource_filter=ResourceFilter(uid=[resource.uid]))[0]
        self.resources[old_resource.id] = resource
        self.save()

    def delete(self, resource: Resource) -> None:
        resource.deleted = True
        self.update(resource=resource)
