import json
import re
import os
from turtle import update

from copy import deepcopy
from enum import Enum
from typing import List, Optional, Dict, Union
from datetime import date, datetime, timedelta
from uuid import uuid4

from utils import Utils
from .base_db_obj import BaseDBObj, BaseDBObjFilter


class Resource(BaseDBObj):
    name: str
    project_uid: str
    acquisition_uids: Optional[List[str]] = None  # Process UID
    desposal_uids: Optional[List[str]] = None  # Process UID
    value_obj_uid: Optional[str] = None  # Resource UID
    value_amount: Optional[float] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def acquisition(self):
        pass

    @property
    def desposal(self):
        pass

    @property
    def value_obj(self):
        pass

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = super().build(dct)
        content.update({
            'name': dct.get('name'),
            'project_uid': dct.get('project_uid'),
            'acquisition_uids': dct.get('acquisition_uids'),
            'desposal_uids': dct.get('desposal_uids'),
            'value_obj_uid': dct.get('value_obj_uid'),
            'value_amount': dct.get('value_amount'),
        })
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = super().put()
        content.update({
            'name': self.name,
            'project_uid': self.project_uid,
            'acquisition_uids': self.acquisition_uids,
            'desposal_uids': self.desposal_uids,
            'value_obj_uid': self.value_obj_uid,
            'value_amount': self.value_amount,
        })
        return content


class ResourceFilter(BaseDBObjFilter):
    name: Optional[List[str]] = None
    project_uid: Optional[List[str]] = None
    acquisition_uids: Optional[List[str]] = None
    desposal_uids: Optional[List[str]] = None
    value_obj_uid: Optional[str] = None

    def filter_results(self, results: List[Resource]):
        results = super().filter_results(results)
        filtered = []
        for result in results:
            if self.name is not None:
                if result.name not in self.name:
                    continue
            if self.project_uid is not None:
                if result.project_uid not in self.project_uid:
                    continue
            if self.acquisition_uids is not None:
                if result.acquisition_uids is None:
                    continue
                if not any([uid in self.acquisition_uids for uid in result.acquisition_uids]):
                    continue
            if self.desposal_uids is not None:
                if result.desposal_uids is None:
                    continue
                if not any([uid in self.desposal_uids for uid in result.desposal_uids]):
                    continue
            if self.value_obj_uid is not None:
                if result.value_obj_uid is None:
                    continue
                if result.value_obj_uid not in self.value_obj_uid:
                    continue
            filtered.append(deepcopy(result))
        return filtered
