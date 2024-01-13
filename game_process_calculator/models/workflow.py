import json
import re
import os

from copy import deepcopy
from enum import Enum
from typing import List, Optional, Dict, Union
from datetime import date, datetime, timedelta
from uuid import uuid4

from utils import Utils
from .base_db_obj import BaseDBObj, BaseDBObjFilter


class ProcessType(Enum):
    LINEAR = 'linear'
    PARALLEL = 'parallel'
    WEB = 'web'


class Workflow(BaseDBObj):
    name: str
    project_uid: str
    process_uids: Optional[List[str]]  # Process or Workflow UID
    process_type: ProcessType

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = super().build(dct)
        content.update({
            'name': dct.get('name'),
            'project_uid': dct.get('project_uid'),
            'process_uids': dct.get('process_uids'),
            'process_type': getattr(ProcessType, dct.get('process_type')),
        })
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = super().put()
        content.update({
            'name': self.name,
            'project_uid': self.project_uid,
            'process_uids': self.process_uids,
            'process_type': self.process_type.name,
        })
        return content

    def update(self, project):
        super().update(project)
        self.name = project.name
        self.process_uids = project.process_uids
        self.process_type = project.process_type

class WorkflowFilter(BaseDBObjFilter):
    name: Optional[List[str]] = None
    project_uid: Optional[List[str]] = None
    process_uids: Optional[List[str]] = None

    def filter_results(self, results: List[Workflow]):
        results = super().filter_results(results)
        filtered = []
        for result in results:
            if self.name is not None:
                if result.name not in self.name:
                    continue
            if self.project_uid is not None:
                if result.project_uid not in self.project_uid:
                    continue
            if self.process_uids is not None:
                if result.process_uids is None:
                    continue
                if not any([uid in self.process_uids for uid in result.process_uids]):
                    continue
            filtered.append(deepcopy(result))
        return filtered
