from importlib.resources import Resource
import json
from multiprocessing.dummy import Process
import re
import os
from tkinter import W
import requests

from typing import List, Optional, Dict, Union

from handlers import (ProjectHandler,
    ResourceHandler,
    ProcessHandler,
    WorkflowHandler)
from models import (Project,
    ProjectFilter,
    Resource,
    ResourceFilter,
    Process,
    ProcessFilter,
    Workflow,
    ProcessType,
    WorkflowFilter)


class DataHandler:
    def __init__(self):
        self.project_handler = ProjectHandler()
        self.resource_handler = ResourceHandler()
        self.process_handler = ProcessHandler()
        self.workflow_handler = WorkflowHandler()

    # Validate
    def validate_project_exists(self, project_uid: str):
        projects = self.project_handler.filter(ProjectFilter())
        if project_uid not in [p.uid for p in projects]:
            raise ValueError('Project not found')

    # Create
    def create_project(self, project: Project):
        projects = self.project_handler.filter(ProjectFilter())
        if project.name in [p.name for p in projects]:
            raise ValueError('Project name already exists')

        self.project_handler.create(project)

    def create_resource(self, resource: Resource):
        self.validate_project_exists(resource.project_uid)

        resources = self.resource_handler.filter(ResourceFilter(project_uid=[resource.project_uid]))
        if resource.name in [r.name for r in resources]:
            raise ValueError('Resource name already exists')

        resource_uids = [r.uid for r in resources]
        if resource.acquisition_uids is not None:
            if not any([uid in resource_uids for uid in resource.acquisition_uids]):
                raise ValueError('Acquisition Resource not found')
        if resource.desposal_uids is not None:
            if not any([uid in resource_uids for uid in resource.desposal_uids]):
                raise ValueError('Desposal Resource not found')
        if resource.value_obj_uid is not None:
            if resource.value_obj_uid not in resource_uids:
                raise ValueError('Value Object Resource not found')

        self.resource_handler.create(resource)

    def create_process(self, process: Process):
        self.validate_project_exists(process.project_uid)

        processes = self.process_handler.filter(ProcessFilter(project_uid=[process.project_uid]))
        if process.name in [p.name for p in processes]:
            raise ValueError('Process name already exists')

        resources = self.resource_handler.filter(ResourceFilter(project_uid=[process.project_uid]))
        if process.consume_uids is not None:
            for consume_uid in process.consume_uids:
                if consume_uid not in [r.uid for r in resources]:
                    raise ValueError('Consume Resource not found')
        if process.produce_uids is not None:
            for produce_uid in process.produce_uids:
                if produce_uid not in [r.uid for r in resources]:
                    raise ValueError('Produce Resource not found')

        self.process_handler.create(process)

    def create_workflow(self, workflow: Workflow):
        self.validate_project_exists(workflow.project_uid)

        workflows = self.workflow_handler.filter(WorkflowFilter(project_uid=[workflow.project_uid]))
        if workflow.name in [r.name for r in workflows]:
            raise ValueError('Workflow name already exists')

        processes = self.process_handler.filter(ProcessFilter(project_uid=[workflow.project_uid]))
        if workflow.process_uids is not None:
            for process_uid in workflow.process_uids:
                if process_uid not in [p.uid for p in processes]:
                    raise ValueError('Process not found')

        self.workflow_handler.create(workflow)

    # Filter
    def filter_projects(self, project_filter: ProjectFilter):
        return self.project_handler.filter(project_filter)

    def filter_resources(self, resource_filter: ResourceFilter):
        return self.resource_handler.filter(resource_filter)

    def filter_processes(self, process_filter: ProcessFilter):
        return self.process_handler.filter(process_filter)

    def filter_workflows(self, workflow_filter: WorkflowFilter):
        return self.workflow_handler.filter(workflow_filter)

    # Update
    def update_project(self, project: Project):
        saved_projects = self.filter_projects(ProjectFilter(uid=[project.uid]))
        if len(saved_projects) != 1:
            raise ValueError('Project not found, or too many found. Unable to update')
        self.project_handler.update(project)
        return project

    def update_resource(self, resource: Resource):
        saved_resources = self.filter_resources(ResourceFilter(project_uid=[resource.project_uid], uid=[resource.uid]))
        if len(saved_resources) != 1:
            raise ValueError('Resources not found, or too many found. Unable to update')
        self.resource_handler.update(resource)
        return resource

    def update_process(self, process: Process):
        saved_processes = self.filter_processes(ProcessFilter(project_uid=[process.project_uid], uid=[process.uid]))
        if len(saved_processes) != 1:
            raise ValueError('Processes not found, or too many found. Unable to update')
        self.process_handler.update(process)
        return process

    def update_workflow(self, workflow: Workflow):
        saved_workflows = self.filter_workflows(WorkflowFilter(project_uid=[workflow.project_uid], uid=[workflow.uid]))
        if len(saved_workflows) != 1:
            raise ValueError('Workflows not found, or too many found. Unable to update')
        self.workflow_handler.update(workflow)
        return workflow

    # delete
    def delete_project(self, project: Project):
        self.project_handler.delete(project)

    def delete_resource(self, resource: Resource):
        self.resource_handler.delete(resource)

    def delete_process(self, process: Process):
        self.process_handler.delete(process)

    def delete_workflow(self, workflow: Workflow):
        self.workflow_handler.delete(workflow)





"""
a = [
    'create',
    'filter',
    'update',
    'delete',
]

b = [
    'project',
    'resource',
    'process',
    'workflow',
]

for i in a:
  print(f"    # {i}")
  for j in b:
    print(f"    def {i}_{j}(self, {j}: {j.title()}):")
    print(f'        pass')
    print(f'    ')


"""

# class WorkflowHandler(BaseDatabaseInteractor):
#     save_filename: Optional[str] = None
#     _workflows: Optional[List[Workflow]] = None

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.save_filename = 'workflows.json'
#         self._workflows = None

#     @property
#     def workflows(self) -> List[Workflow]:
#         if self._workflows is None:
#             self.load()
#         return self._workflows

#     @property
#     def save_file_path(self) -> str:
#         return os.path.join(self.save_dir, self.save_filename)

#     def load(self) -> None:
#         if os.path.exists(self.save_file_path):
#             data = [Workflow.build(p) for p in self.load_file(self.save_file_path)]
#         else:
#             data = []
#         self._workflows = data

#     def save(self) -> None:
#         os.makedirs(self.save_dir, exist_ok=True)
#         content = [p.put() for p in self.workflows]
#         self.save_file(self.save_file_path, content)

#     def create(self, workflow: Workflow) -> Workflow:
#         workflows = self.workflows
#         workflow.id = len(workflows)
#         workflows.append(workflow)
#         self.save()
#         return workflow

#     def filter(self, workflow_filter: WorkflowFilter) -> List[Workflow]:
#         workflows = self.workflows
#         workflows = workflow_filter.filter_results(workflows)
#         return workflows

#     def update(self, workflow: Workflow) -> None:
#         old_process = self.filter(workflow_filter=WorkflowFilter(uid=[workflow.uid]))[0]
#         self.workflows[old_process.id] = workflow
#         self.save()

#     def delete(self, workflow: Workflow) -> None:
#         workflow.deleted = True
#         self.update(workflow=workflow)
