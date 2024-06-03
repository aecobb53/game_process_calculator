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
    WorkflowFilter,
    BalanceWorkflowArgs)

from utils import MissingRecordException, DuplicateRecordsException, Utils


class DataHandler:
    def __init__(self):
        self.project_handler = ProjectHandler()
        self.resource_handler = ResourceHandler()
        self.process_handler = ProcessHandler()
        self.workflow_handler = WorkflowHandler()
        self.utils = Utils()

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
        saved_project = self.find_project(project.uid)
        self.project_handler.update(saved_project=saved_project, project=project)
        return project

    def update_resource(self, resource: Resource):
        saved_resource = self.find_resource(resource.uid)
        self.resource_handler.update(saved_resource=saved_resource, resource=resource)
        return resource

    def update_process(self, process: Process):
        saved_process = self.find_process(process.uid)
        self.process_handler.update(saved_process=saved_process, process=process)
        return process

    def update_workflow(self, workflow: Workflow):
        saved_wrokflow = self.find_workflow(workflow.uid)
        self.workflow_handler.update(saved_wrokflow=saved_wrokflow, workflow=workflow)
        return workflow

    # delete
    def delete_project(self, project_uid: str):
        saved_project = self.find_project(project_uid)
        return self.project_handler.delete(saved_project)

    def delete_resource(self, resource_uid: str):
        saved_resource = self.find_resource(resource_uid)
        return self.resource_handler.delete(saved_resource)

    def delete_process(self, process_uid: str):
        saved_process = self.find_process(process_uid)
        return self.process_handler.delete(saved_process)

    def delete_workflow(self, workflow_uid: str):
        saved_wrokflow = self.find_workflow(workflow_uid)
        return self.workflow_handler.delete(saved_wrokflow)

    def export_database(self):
        projects = self.project_handler.export_projects()
        resources = self.resource_handler.export_resources()
        processes = self.process_handler.export_processes()
        workflows = self.workflow_handler.export_workflows()
        content = {
            'projects': projects,
            'resources': resources,
            'processes': processes,
            'workflows': workflows
        }
        return content

    def import_database(self, content):
        self.project_handler.import_projects(content['projects'])
        self.resource_handler.import_resources(content['resources'])
        self.process_handler.import_processes(content['processes'])
        self.workflow_handler.import_workflows(content['workflows'])

    def calculate_workflow_resources(self, workflow_processes):
        """
        Given a series of processes, what are the resulting resources flows
        """
        workflow_resources = {}
        for thing, process_details in workflow_processes.items():
            # print('')
            # print('')
            # print('CALCULATE WORKFLOW RESOURCES WORKFLOW PROCESS DICT')
            # print('')
            # print(thing)
            # print('')
            # print(json.dumps(process_details, indent=2))
            # print('')
            # print('')
            # print('')
            for resource_uid, resource_amount in process_details['consumes_resources'].items():
                resource = self.find_resource(resource_uid=resource_uid)
                if resource_uid not in workflow_resources:
                    workflow_resources[resource_uid] = {
                        "name": self.find_resource(resource_uid=resource_uid).name,  # Just for now
                        "resource_metadata": resource.put(),
                        "consumed_per_second": 0,
                        "produced_per_second": 0,
                    }
                workflow_resources[resource_uid]['consumed_per_second'] += resource_amount / process_details['process_time_seconds'] * process_details['process_count']
            for resource_uid, resource_amount in process_details['produces_resources'].items():
                resource = self.find_resource(resource_uid=resource_uid)
                if resource_uid not in workflow_resources:
                    workflow_resources[resource_uid] = {
                        "name": self.find_resource(resource_uid=resource_uid).name,  # Just for now
                        "resource_metadata": resource.put(),
                        "consumed_per_second": 0,
                        "produced_per_second": 0,
                    }
                workflow_resources[resource_uid]['produced_per_second'] += resource_amount / process_details['process_time_seconds'] * process_details['process_count']
        return workflow_resources

    def adjust_workflow_processes(self, workflow, workflow_processes, workflow_resources, balance_criteria):
        """
        Given a series of resources, adjust the processes to meet the balance criteria
        """
        # print('ADJUSTING WORKFLOW PROCESSES')
        adjusted = False
        for resource_uid, resource_data in workflow_resources.items():
            if resource_uid in workflow.focus_resource_uids:
                net_production = resource_data['produced_per_second'] - resource_data['consumed_per_second']
                if net_production < balance_criteria.extract_units_per_second:
                    for process_uid, processes_dict in workflow_processes.items():
                        if resource_uid in processes_dict['produces_resources']:
                            adjustment = balance_criteria.extract_units_per_second / (
                                processes_dict['produces_resources'][resource_uid] / processes_dict['process_time_seconds']
                            )
                            workflow_processes[process_uid]['process_count'] = adjustment
                            adjusted = True
        if not adjusted:
            for resource_uid, resource_data in workflow_resources.items():
                if resource_data['consumed_per_second'] > 0 and resource_data['produced_per_second'] > 0:
                    # print(resource_uid)
                    # print(json.dumps(resource_data, indent=2))
                    if resource_data['produced_per_second'] < resource_data['consumed_per_second']:
                        # print('NEED TO ADJUST')
                        for process_uid, processes_dict in workflow_processes.items():
                            if resource_uid in processes_dict['produces_resources']:
                                # print(f"FOUND FOR ADJUSTMENT: {process_uid}")
                                # print(json.dumps(processes_dict, indent=2))
                                adjustment = (resource_data['consumed_per_second'] - resource_data['produced_per_second']) / (
                                    processes_dict['produces_resources'][resource_uid] / processes_dict['process_time_seconds']
                                )
                                adjustment = self.utils.round_up(number=adjustment)
                                # print(f"Adjustment: {adjustment}")
                                workflow_processes[process_uid]['process_count'] += adjustment
                                adjusted = True
        return adjusted, workflow_processes

    def balance_workflow(self,
        workflow: Workflow,
        balance_criteria: BalanceWorkflowArgs = None):
        # TODO: Move speed modifier and productivity modifier into the process and apply upon balance
        """
        Create a dict of processes to alter increase the count of processes needed
        """
        workflow_processes = {}
        for process_uid in workflow.process_uids:
            process = self.find_process(process_uid=process_uid)
            process_dict = {
                "name": process.name,  # Just for now
                "process_metadata": process.put(),
                "machine_used": 'N/A',  # TODO: Add machine used
                "process_count": 1,
                "process_time_seconds": process.process_time,
                "consumes_resources": {},
                "produces_resources": {},
            }
            for resource_uid, resource_amount in process.consume_uids.items():
                if resource_uid not in process_dict['consumes_resources']:
                    process_dict['consumes_resources'][resource_uid] = resource_amount
            for resource_uid, resource_amount in process.produce_uids.items():
                if resource_uid not in process_dict['produces_resources']:
                    process_dict['produces_resources'][resource_uid] = resource_amount
            workflow_processes[process_uid] = process_dict

        # Initial calculation of resources
        workflow_resources = self.calculate_workflow_resources(workflow_processes=workflow_processes)
        _, workflow_processes = self.adjust_workflow_processes(workflow=workflow, workflow_processes=workflow_processes, workflow_resources=workflow_resources, balance_criteria=balance_criteria)
        workflow_resources = self.calculate_workflow_resources(workflow_processes=workflow_processes)

        # Adjustment of process counts
        _, workflow_processes = self.adjust_workflow_processes(workflow=workflow, workflow_processes=workflow_processes, workflow_resources=workflow_resources, balance_criteria=balance_criteria)
        workflow_resources = self.calculate_workflow_resources(workflow_processes=workflow_processes)

        return workflow_processes, workflow_resources

    def return_complex_workflow_object(self, workflows: List[Workflow], balance_criteria: BalanceWorkflowArgs = None):
        workflows_dict = []
        for workflow in workflows:
            if workflow.process_uids is not None:
                processes_dict, resources_dict = self.balance_workflow(workflow, balance_criteria=balance_criteria)
            else:
                processes_dict = None
                resources_dict = None
            workflow_dict = workflow.put()
            workflow_dict['processes_dict'] = processes_dict
            workflow_dict['resources_dict'] = resources_dict
            workflows_dict.append(workflow_dict)



        # with open('DELETEME_IM_NOT_NEEDED.json', 'w') as jf:
        #     jf.write(json.dumps(workflows_dict, indent=4))
        # for resource_uid, resource_data in resources_dict.items():
        #     print('')
        #     print(resource_data['name'])
        #     print(resource_data['consumed_per_second'], resource_data['produced_per_second'])
        #     net = resource_data['produced_per_second'] - resource_data['consumed_per_second']
        #     print(f"Net: {net}")




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
