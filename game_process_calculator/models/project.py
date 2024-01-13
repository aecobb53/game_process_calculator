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


class Project(BaseDBObj):
    name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = super().build(dct)
        content.update({
            'name': dct.get('name'),
        })
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = super().put()
        content.update({
            'name': self.name,
        })
        return content

    def update(self, project):
        super().update(project)
        self.name = project.name


class ProjectFilter(BaseDBObjFilter):
    name: Optional[List[str]] = None

    def filter_results(self, results: List[Project]):
        results = super().filter_results(results)
        filtered = []
        for result in results:
            if self.name is not None:
                if result.name not in self.name:
                    continue
            filtered.append(deepcopy(result))
        return filtered
