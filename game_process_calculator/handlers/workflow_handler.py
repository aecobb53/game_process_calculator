import json
import re
import os
import requests

from typing import List, Optional, Dict, Union

from handlers import BaseDatabaseInteractor
from models import Workflow, WorkflowFilter


class WorkflowHandler(BaseDatabaseInteractor):
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
            data = [Workflow.build(p) for p in self.load_file(self.save_file_path)]
        else:
            data = []
        self._workflows = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [p.put() for p in self.workflows]
        self.save_file(self.save_file_path, content)

    def create(self, workflow: Workflow) -> Workflow:
        workflows = self.workflows
        workflow.id = len(workflows)
        workflows.append(workflow)
        self.save()
        return workflow

    def filter(self, workflow_filter: WorkflowFilter) -> List[Workflow]:
        workflows = self.workflows
        workflows = workflow_filter.filter_results(workflows)
        return workflows

    def update(self, workflow: Workflow) -> None:
        old_process = self.filter(workflow_filter=WorkflowFilter(uid=[workflow.uid]))[0]
        self.workflows[old_process.id] = workflow
        self.save()

    def delete(self, workflow: Workflow) -> None:
        workflow.deleted = True
        self.update(workflow=workflow)
