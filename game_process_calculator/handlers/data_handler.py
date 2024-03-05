import json
import re
import os
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

from utils import MissingRecordException, DuplicateRecordsException


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
            raise MissingRecordException(f'Missing Project [{project_uid}]')
        return True

    # Create
    def create_project(self, project: Project):
        projects = self.project_handler.filter(ProjectFilter())
        if project.name in [p.name for p in projects]:
            raise DuplicateRecordsException(f'Project [{project.name}] already exists and must be unique')
        return self.project_handler.create(project)

    def create_resource(self, resource: Resource):
        self.validate_project_exists(resource.project_uid)

        resources = self.resource_handler.filter(ResourceFilter(project_uid=[resource.project_uid]))
        if resource.name in [r.name for r in resources]:
            raise DuplicateRecordsException(f'Resource [{resource.name}] already exists and must be unique')

        resource_uids = [r.uid for r in resources]
        if resource.acquisition_uids is not None:
            if not any([uid in resource_uids for uid in resource.acquisition_uids]):
                raise MissingRecordException(f'Acquisition Resource [{resource.acquisition_uids}] not found')
        if resource.desposal_uids is not None:
            if not any([uid in resource_uids for uid in resource.desposal_uids]):
                raise MissingRecordException(f'Desposal Resource [{resource.desposal_uids}] not found')
        if resource.value_obj_uid is not None:
            if resource.value_obj_uid not in resource_uids:
                raise MissingRecordException(f'Value Resource [{resource.value_obj_uid}] not found')

        return self.resource_handler.create(resource)

    def create_process(self, process: Process):
        self.validate_project_exists(process.project_uid)

        processes = self.process_handler.filter(ProcessFilter(project_uid=[process.project_uid]))
        if process.name in [p.name for p in processes]:
            raise DuplicateRecordsException(f'Process [{process.name}] already exists and must be unique')

        resources = self.resource_handler.filter(ResourceFilter(project_uid=[process.project_uid]))
        if process.consume_uids is not None:
            for consume_uid in process.consume_uids:
                if consume_uid not in [r.uid for r in resources]:
                    raise MissingRecordException(f'Consume Resource [{consume_uid}] not found')
        if process.produce_uids is not None:
            for produce_uid in process.produce_uids:
                if produce_uid not in [r.uid for r in resources]:
                    raise MissingRecordException(f'Produce Resource [{produce_uid}] not found')

        return self.process_handler.create(process)

    def create_workflow(self, workflow: Workflow):
        self.validate_project_exists(workflow.project_uid)

        workflows = self.workflow_handler.filter(WorkflowFilter(project_uid=[workflow.project_uid]))
        if workflow.name in [r.name for r in workflows]:
            raise DuplicateRecordsException(f'Workflow [{workflow.name}] already exists and must be unique')

        processes = self.process_handler.filter(ProcessFilter(project_uid=[workflow.project_uid]))
        if workflow.process_uids is not None:
            for process_uid in workflow.process_uids:
                if process_uid not in [p.uid for p in processes]:
                    raise MissingRecordException(f'Process [{process_uid}] not found')

        return self.workflow_handler.create(workflow)

    # Filter
    def filter_projects(self, project_filter: ProjectFilter):
        return self.project_handler.filter(project_filter)

    def filter_resources(self, resource_filter: ResourceFilter):
        return self.resource_handler.filter(resource_filter)

    def filter_processes(self, process_filter: ProcessFilter):
        return self.process_handler.filter(process_filter)

    def filter_workflows(self, workflow_filter: WorkflowFilter):
        return self.workflow_handler.filter(workflow_filter)

    # Find
    def find_project(self, project_uid: str):
        project_filter = ProjectFilter(uid=[project_uid])
        projects = self.project_handler.filter(project_filter=project_filter)
        if len(projects) == 0:
            raise MissingRecordException(f'Project not found for uid [{project_uid}]')
        if len(projects) > 1:
            raise DuplicateRecordsException(f'Too many projects found for uid [{project_uid}]')
        return projects[0]

    def find_resource(self, resource_uid: str):
        resource_filter = ResourceFilter(uid=[resource_uid])
        resources = self.resource_handler.filter(resource_filter=resource_filter)
        if len(resources) == 0:
            raise MissingRecordException(f'Resource not found for uid [{resource_uid}]')
        if len(resources) > 1:
            raise DuplicateRecordsException(f'Too many resources found for uid [{resource_uid}]')
        return resources[0]

    def find_process(self, process_uid: str):
        process_filter = ProcessFilter(uid=[process_uid])
        processes = self.process_handler.filter(process_filter=process_filter)
        if len(processes) == 0:
            raise MissingRecordException(f'Process not found for uid [{process_uid}]')
        if len(processes) > 1:
            raise DuplicateRecordsException(f'Too many processes found for uid [{process_uid}]')
        return processes[0]

    def find_workflow(self, workflow_uid: str):
        workflow_filter = WorkflowFilter(uid=[workflow_uid])
        workflows = self.workflow_handler.filter(workflow_filter=workflow_filter)
        if len(workflows) == 0:
            raise MissingRecordException(f'Workflow not found for uid [{workflow_uid}]')
        if len(workflows) > 1:
            raise DuplicateRecordsException(f'Too many workflows found for uid [{workflow_uid}]')
        return workflows[0]

    # Update
    def update_project(self, project: Project):
        self.find_project(project.uid)  # This may not be needed, but it ensures there is a project with this ID
        self.project_handler.update(project)
        return project

    def update_resource(self, resource: Resource):
        self.find_resource(resource.uid)  # This may not be needed, but it ensures there is a resource with this ID
        self.resource_handler.update(resource)
        return resource

    def update_process(self, process: Process):
        self.find_process(process.uid)  # This may not be needed, but it ensures there is a process with this ID
        self.process_handler.update(process)
        return process

    def update_workflow(self, workflow: Workflow):
        self.find_workflow(workflow.uid)  # This may not be needed, but it ensures there is a workflow with this ID
        self.workflow_handler.update(workflow)
        return workflow

    # delete
    def delete_project(self, project: Project):
        return self.project_handler.delete(project)

    def delete_resource(self, resource: Resource):
        return self.resource_handler.delete(resource)

    def delete_process(self, process: Process):
        return self.process_handler.delete(process)

    def delete_workflow(self, workflow: Workflow):
        return self.workflow_handler.delete(workflow)

    def balance_workflow(self,
        workflow: Workflow,
        units_per_second: float = None,
        speed_modifier: float = 1,
        productivity_modifier: float = 1):
        processes = []
        for process_uid in workflow.process_uids:
            process = self.filter_processes(ProcessFilter(uid=[process_uid]))
            assert len(process) == 1  # This needs better error handling
            process = process[0]
            consumes_resources = []
            produces_resources = []
            if process.consume_uids is not None:
                for resource_uid in process.consume_uids:
                    resource = self.filter_resources(ResourceFilter(uid=[resource_uid]))
                    assert len(resource) == 1  # This needs better error handling
                    consumes_resources.append(resource[0].put())
            if process.produce_uids is not None:
                for resource_uid in process.produce_uids:
                    resource = self.filter_resources(ResourceFilter(uid=[resource_uid]))
                    assert len(resource) == 1
                    produces_resources.append(resource[0].put())
            process_dict = process.put()
            process_dict['consumes_resources'] = consumes_resources
            process_dict['produces_resources'] = produces_resources
            process_dict['machine_used'] = 'N/A'  # Fix this eventually
            process_dict['machine_count'] = 1  # Fix this eventually
            processes.append(process_dict)
        return processes

    def return_complex_workflow_object(self, workflows: List[Workflow]):
        workflows_dict = []
        for workflow in workflows:
            if workflow.process_uids is not None:
                processes = self.balance_workflow(workflow)
            else:
                processes = []
            # processes = []
            # if workflow.process_uids is not None:
            #     for process_uid in workflow.process_uids:
            #         process = self.filter_processes(ProcessFilter(uid=[process_uid]))
            #         assert len(process) == 1  # This needs better error handling
            #         process = process[0]
            #         consumes_resources = []
            #         produces_resources = []
            #         if process.consume_uids is not None:
            #             for resource_uid in process.consume_uids:
            #                 resource = self.filter_resources(ResourceFilter(uid=[resource_uid]))
            #                 assert len(resource) == 1  # This needs better error handling
            #                 consumes_resources.append(resource[0].put())
            #         if process.produce_uids is not None:
            #             for resource_uid in process.produce_uids:
            #                 resource = self.filter_resources(ResourceFilter(uid=[resource_uid]))
            #                 assert len(resource) == 1
            #                 produces_resources.append(resource[0].put())
            #         process_dict = process.put()
            #         process_dict['consumes_resources'] = consumes_resources
            #         process_dict['produces_resources'] = produces_resources
            #         processes.append(process_dict)
            workflow_dict = workflow.put()
            workflow_dict['processes'] = processes
            workflows_dict.append(workflow_dict)
        return workflows_dict





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
