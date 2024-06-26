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


class Process(BaseDBObj):
    name: str
    project_uid: str
    consume_uids: Optional[Dict[str, float]] = None  # Resource UID
    produce_uids: Optional[Dict[str, float]] = None  # Resource UID
    machine_uid: Optional[str] = None  # Machine UID
    process_time_seconds: Optional[float] = None
    rest_time_seconds: Optional[float] = None
    # modifiers_multiplier: Optional[List[float]] = None
    # modifiers_sum: Optional[List[float]] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def process_time(self):
        time = self.process_time_seconds or 0
        time += self.rest_time_seconds or 0
        return time

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = super().build(dct)
        content.update({
            'name': dct.get('name'),
            'project_uid': dct.get('project_uid'),
            'consume_uids': dct.get('consume_uids'),
            'produce_uids': dct.get('produce_uids'),
            'machine_uid': dct.get('machine_uid'),
            'process_time_seconds': dct.get('process_time_seconds'),
            'rest_time_seconds': dct.get('rest_time_seconds'),
            # 'modifiers_multiplier': dct.get('modifiers_multiplier'),
            # 'modifiers_sum': dct.get('modifiers_sum'),
        })
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = super().put()
        content.update({
            'name': self.name,
            'project_uid': self.project_uid,
            'consume_uids': self.consume_uids,
            'produce_uids': self.produce_uids,
            'machine_uid': self.machine_uid,
            'process_time_seconds': self.process_time_seconds,
            'rest_time_seconds': self.rest_time_seconds,
            # 'productivity_modifier': self.modifiers_multiplier,
            # 'speed_modifier': self.modifiers_sum,
        })
        return content

    def update(self, project):
        super().update(project)
        self.name = project.name
        self.consume_uids = project.consume_uids
        self.produce_uids = project.produce_uids
        self.machine_uid = project.machine_uid
        # self.modifiers_multiplier = project.modifiers_multiplier
        # self.modifiers_sum = project.modifiers_sum


class ProcessFilter(BaseDBObjFilter):
    name: Optional[List[str]] = None
    project_uid: Optional[List[str]] = None
    consume_uids: Optional[List[str]] = None
    produce_uids: Optional[List[str]] = None
    machine_uids: Optional[List[str]] = None
    value_obj_uid: Optional[str] = None

    def filter_results(self, results: List[Process]):
        results = super().filter_results(results)
        filtered = []
        for result in results:
            if self.name is not None:
                if result.name not in self.name:
                    continue
            if self.project_uid is not None:
                if result.project_uid not in self.project_uid:
                    continue
            if self.consume_uids is not None:
                if result.consume_uids is None:
                    continue
                if not any([uid in self.consume_uids for uid in result.consume_uids]):
                    continue
            if self.produce_uids is not None:
                if result.produce_uids is None:
                    continue
                if not any([uid in self.produce_uids for uid in result.produce_uids]):
                    continue
            if self.machine_uids is not None:
                if result.machine_uid not in self.machine_uids:
                    continue
            if self.value_obj_uid is not None:
                if result.value_obj_uid is None:
                    continue
                if not any([uid in self.value_obj_uid for uid in result.value_obj_uid]):
                    continue
            filtered.append(deepcopy(result))
        return filtered
