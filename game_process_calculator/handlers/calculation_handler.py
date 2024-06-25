from datetime import datetime
from sqlmodel import Session, select
import math

from .base_handler import BaseHandler
from .workflow_handler import WorkflowHandler
from copy import deepcopy
from models import (ProcessType,
    WorkflowFilter,
    BalanceWorkflowArgs,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException
from . import ProjectHandler, TagHandler


class CalculationHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def calculate_workflow(self, workflow_filter: WorkflowFilter, balance_criteria: BalanceWorkflowArgs):
        wh = WorkflowHandler()
        workflows = await wh.filter_workflows(workflow_filter=workflow_filter, detailed_output=True)
        for workflow in workflows:
            workflow.parallel_processes_counter = {p.uid: 1 for p in workflow.processes}
            if workflow.process_type == ProcessType.LINEAR:
                resources = self.calculate_resource_throughput(workflow=workflow)
                while not self.is_parrallel_processes_enough(workflow=workflow, balance_criteria=balance_criteria, resources=resources):
                    self.adjust_parallel_processes(workflow=workflow, balance_criteria=balance_criteria, resources=resources)
                    resources = self.calculate_resource_throughput(workflow=workflow)
            workflow.resource_throughputs_per_second = {}
            for resource, resource_details in resources.items():
                workflow.resource_throughputs_per_second[resource] = round(resource_details['total_throughput_per_second'], 2)
        return workflows

    def calculate_resource_throughput(self, workflow):
        resources = {}
        for process in workflow.processes:
            parallel_processes_counter = workflow.parallel_processes_counter[process.uid]
            for resource in process.consume_resources:
                if resource.uid not in resources:
                    resources[resource.uid] = {
                        'resource': resource,
                        'processes': [],
                        'total_consumed_per_second': 0,
                        'total_produced_per_second': 0,
                        'total_throughput_per_second': 0,
                    }
                resources[resource.uid]['processes'].append(process)
                units = process.consume_resource_uids[resource.uid] * parallel_processes_counter
                process_time_seconds = process.process_time_seconds or 0 + process.rest_time_seconds or 0
                units_per_second = units / process_time_seconds

                resources[resource.uid]['total_consumed_per_second'] += units_per_second
                resources[resource.uid]['total_throughput_per_second']  = \
                    resources[resource.uid]['total_produced_per_second'] - \
                    resources[resource.uid]['total_consumed_per_second']
            for resource in process.produce_resources:
                if resource.uid not in resources:
                    resources[resource.uid] = {
                        'resource': resource,
                        'processes': [],
                        'total_consumed_per_second': 0,
                        'total_produced_per_second': 0,
                        'total_throughput_per_second': 0,
                    }
                resources[resource.uid]['processes'].append(process)
                units = process.produce_resource_uids[resource.uid] * parallel_processes_counter
                process_time_seconds = process.process_time_seconds or 0 + process.rest_time_seconds or 0
                units_per_second = units / process_time_seconds

                resources[resource.uid]['total_produced_per_second'] += units_per_second
                resources[resource.uid]['total_throughput_per_second']  = \
                    resources[resource.uid]['total_produced_per_second'] - \
                    resources[resource.uid]['total_consumed_per_second']
        return resources

    def adjust_parallel_processes(self, workflow, balance_criteria, resources):
        resources = self.calculate_resource_throughput(workflow=workflow)
        for resource, resource_details in resources.items():
            if resource == workflow.focus_resource_uid:
                if resource_details['total_throughput_per_second'] < balance_criteria.units_per_second[0]:
                    for process in resource_details['processes']:
                        if workflow.focus_resource.uid in process.produce_resource_uids.keys():
                            workflow.parallel_processes_counter[process.uid] += 1

    def is_parrallel_processes_enough(self, workflow, balance_criteria, resources):
        resources = self.calculate_resource_throughput(workflow=workflow)
        for resource, resource_details in resources.items():
            if resource == workflow.focus_resource_uid:
                if resource_details['total_throughput_per_second'] < balance_criteria.units_per_second[0]:
                    return False
        return True
