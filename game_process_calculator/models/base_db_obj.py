import json
import re
import os

from copy import deepcopy
from pydantic import BaseModel, field_validator, FieldValidationInfo
from enum import Enum
from typing import List, Optional, Dict, Union
from datetime import date, datetime, timedelta
from uuid import uuid4

from utils import Utils


class BaseDBObj(BaseModel):
    internal_id: Optional[int] = None
    internal_uid: Optional[str] = None
    creation_datetime: Optional[datetime] = None
    update_datetime: Optional[datetime] = None
    description: Optional[str] = None
    notes: Optional[List[str]] = None
    metadata: Optional[Dict] = None
    active: Optional[bool] = None
    deleted: Optional[bool] = False

    @field_validator('internal_uid')
    # @classmethod
    def validate_internal_uid(cls, v: str, info: FieldValidationInfo):
        if v is None:
            uid = str(uuid4())
        else:
            uid = v
        return uid

    @field_validator('creation_datetime')
    # @classmethod
    def validate_creation_datetime(cls, v: str, info: FieldValidationInfo):
        if v is None:
            uid = datetime.utcnow()
        else:
            uid = v
        return uid

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    @property
    def id(self):
        return self.internal_id

    @id.setter
    def id(self, value):
        if self.internal_id is not None:
            raise ValueError('ID already set')
        self.internal_id = value

    @property
    def uid(self):
        return self.internal_uid

    @uid.setter
    def uid(self, value):
        if self.internal_uid is not None:
            raise ValueError('UID already set')
        self.internal_uid = value

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = {
            'internal_id': dct.get('id'),
            'internal_uid': dct.get('uid'),
            'creation_datetime': utils.time_str_to_obj(dct.get('creation_datetime'), allow_none=True),
            'update_datetime': utils.time_str_to_obj(dct.get('update_datetime'), allow_none=True),
            'description': dct.get('description'),
            'notes': dct.get('notes'),
            'metadata': dct.get('metadata'),
            'active': dct.get('active'),
            'deleted': dct.get('deleted'),
        }
        return content

    def put(self):
        utils = Utils()
        content = {
            'id': self.id,
            'uid': self.uid,
            'creation_datetime': utils.time_obj_to_str(self.creation_datetime, allow_none=True),
            'update_datetime': utils.time_obj_to_str(self.update_datetime, allow_none=True),
            'description': self.description,
            'notes': self.notes,
            'metadata': self.metadata,
            'active': self.active,
            'deleted': self.deleted,
        }
        return content

    def update(self, obj) -> None:
        self.description = obj.description
        self.notes = obj.notes
        self.name = obj.name
        self.active = obj.active
        self.deleted = obj.deleted
        self.metadata = obj.metadata

        self.update_datetime = datetime.utcnow()

    def delete(self) -> None:
        self.deleted = True
        self.update_datetime = datetime.utcnow()


class BaseDBObjFilter(BaseModel):
    uid: Optional[List[str]] = None
    description: Optional[List[str]] = None
    active: Optional[bool] = None
    deleted: Optional[bool] = None

    def filter_results(self, results: List[BaseDBObj]):
        filtered = []
        for result in results:
            if self.deleted is not None:
                if result.deleted != self.deleted:
                    continue
            else:
                if result.deleted:
                    continue

            if self.uid is not None:
                if result.uid not in self.uid:
                    continue
            if self.description is not None:
                if result.description not in self.description:
                    continue
            if self.active is not None:
                if result.active != self.active:
                    continue
            filtered.append(deepcopy(result))
        return filtered
