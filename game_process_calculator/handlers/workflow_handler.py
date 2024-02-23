import json
import re
import os
import requests

from copy import deepcopy
from typing import List, Optional, Dict, Union

# from handlers import BaseDatabaseInteractor
from handlers import BaseHandler
from models import Workflow, WorkflowFilter


class WorkflowHandler(BaseHandler):
    save_filename: Optional[str] = None
    _workflows: Optional[List[Workflow]] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.save_filename = 'workflows.json'
        self._workflows = None

    @property
    def workflows(self) -> List[Workflow]:
        if self._workflows is None:
            self.load()
        return self._workflows

    @property
    def save_file_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)

    def load(self) -> None:
        if os.path.exists(self.save_file_path):
            data = [Workflow.build(w) for w in self.load_file(self.save_file_path)]
        else:
            data = []
        self._workflows = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [p.put() for p in self.workflows]
        self.save_file(self.save_file_path, content)

    def create(self, workflow: Workflow) -> Workflow:
        workflows = self.workflows
        new_workflow = Workflow.build(workflow.put())
        new_workflow.id = len(workflows)
        workflows.append(new_workflow)
        self.save()
        return new_workflow

    def filter(self, workflow_filter: WorkflowFilter) -> List[Workflow]:
        workflows = self.workflows
        workflows = workflow_filter.filter_results(workflows)
        return workflows

    def update(self, workflow: Workflow) -> Workflow:
        workflows = self.filter(WorkflowFilter(uid=[workflow.uid]))

        if len(workflows) == 0:
            raise IndexError(f"Workflow with uid {workflow.uid} not found")
        elif len(workflows) > 1:
            raise IndexError(f"Workflow with uid {workflow.uid} returns multiple results")

        updated_workflow = self.filter(workflow_filter=WorkflowFilter(uid=[workflow.uid]))[0]
        updated_workflow.update(workflow)
        self.workflows[updated_workflow.id] = updated_workflow
        self.save()
        return deepcopy(workflow)

    def delete(self, workflow_uid: int) -> Workflow:
        workflows = self.filter(WorkflowFilter(uid=[workflow_uid]))

        if len(workflows) == 0:
            raise IndexError(f"Workflow with uid {workflow_uid} not found")
        elif len(workflows) > 1:
            raise IndexError(f"Workflow with uid {workflow_uid} returns multiple results")

        delete_workflow = self.filter(workflow_filter=WorkflowFilter(uid=[workflow_uid]))[0]
        delete_workflow.delete()
        self.workflows[delete_workflow.id] = delete_workflow
        self.save()
        return deepcopy(delete_workflow)

    def export_workflows(self) -> Dict:
        workflows = self.filter(WorkflowFilter())
        return {'workflows': [p.put() for p in workflows]}

    def import_workflows(self, dct) -> List[Workflow]:
        self._workflows = []
        workflows = self.workflows
        output = []
        print(json.dumps(dct, indent=4))
        for workflow_dct in dct['workflows']:
            workflow = Workflow.build(workflow_dct)
            output.append(workflow)
            workflows.append(workflow)

        self.save()
        return output

    def export_google_sheet(self) -> List[str]:
        workflows = self.filter(WorkflowFilter())
        output = []
        for workflow in workflows:
            output.append(f"{workflow.uid},{workflow.name},=SUM(1,2)")
        return output
