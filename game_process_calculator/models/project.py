import json

from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from uuid import uuid4

from . import GPCBaseModel, GPCFilter


class Project(GPCBaseModel):
    update_datetime: datetime | None = None
    notes: List[str] | None = None  # Notes more for me than anybody else
    change_log: Dict = {}  # A dict of timestamps and changes

    name: str

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
        return fields


class ProjectDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    creation_datetime: datetime
    update_datetime: datetime | None = None
    notes: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    description: str | None = None
    # change_log: str | None = None
    change_log: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    active: bool
    deleted: bool
    cascade_active: bool
    cascade_deleted: bool

    name: str

    # __table_args__ = (UniqueConstraint('uid', 'name'))

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = fields.dict()
        return fields

    def cast_data_object(self, data_object_class) -> Project:
        """Return a data object based on the data_object_class"""
        content = self.dict()
        if content['change_log'] is not None:
            content['change_log'] = json.loads(content['change_log'])
        data_obj = data_object_class(**content)
        return data_obj


class ProjectDBCreate(ProjectDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        super().validate_fields(fields)
        fields = fields.dict()
        if 'id' in fields:
            del fields['id']
        fields['creation_datetime'] = datetime.utcnow()
        fields['update_datetime'] = fields['creation_datetime']
        # if 'change_log' in fields:
        #     fields['change_log'] = json.dumps(fields['change_log'])
        return fields


class ProjectDBRead(ProjectDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        return fields.dict()

    def return_data_obj(self) -> Project:
        obj = Project(**self.dict())
        return obj


class ProjectDB(ProjectDBBase, table=True):
    __tablename__ = "project"


class ProjectFilter(GPCFilter):
    # uid: List[str] | None = None
    # name: List[str] | None = None
    name: List[str] | str | None = None
    # active: bool | None | str = True
    # deleted: bool | None | str = False
    # cascade_active: bool | None | str = True
    # cascade_deleted: bool | None | str = False

    # creation_datetime_before: datetime | None = None
    # creation_datetime_after: datetime | None = None
    # limit: int = 1000

    # order_by: List[str] = ['creation_datetime']
    # offset: int = 0

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
        # print(f'FILTER FIELDS: {fields}')
        # if isinstance(fields.get('active'), list):
        #     fields['active'] = fields['active'][0]
        # if isinstance(fields.get('deleted'), list):
        #     fields['deleted'] = fields['deleted'][0]
        # if isinstance(fields.get('cascade_active'), list):
        #     fields['cascade_active'] = fields['cascade_active'][0]
        # if isinstance(fields.get('cascade_deleted'), list):
        #     fields['cascade_deleted'] = fields['cascade_deleted'][0]
        # if isinstance(fields.get('creation_datetime_before'), list):
        #     fields['creation_datetime_before'] = fields['creation_datetime_before'][0]
        # if isinstance(fields.get('creation_datetime_after'), list):
        #     fields['creation_datetime_after'] = fields['creation_datetime_after'][0]
        return fields

    def apply_filters(self, database_object_class: ProjectDBBase, query: select) -> select:
        """Apply the filters to the query"""
        query = super().apply_filters(database_object_class, query)
        # if self.uid:
        #     query = query.filter(database_object_class.uid.in_(self.uid))
        if self.name:
            query = query.filter(database_object_class.name.in_(self.name))
        # if self.active is not None:
        #     if not isinstance(self.active, str):
        #         query = query.filter(database_object_class.active == self.active)
        # if self.deleted is not None:
        #     if not isinstance(self.deleted, str):
        #         query = query.filter(database_object_class.deleted == self.deleted)
        # if self.cascade_active is not None:
        #     if not isinstance(self.cascade_active, str):
        #         query = query.filter(database_object_class.cascade_active == self.cascade_active)
        # if self.cascade_deleted is not None:
        #     if not isinstance(self.cascade_deleted, str):
        #         query = query.filter(database_object_class.cascade_deleted == self.cascade_deleted)

        # if self.creation_datetime_before:
        #     query = query.filter(database_object_class.creation_datetime <= self.creation_datetime_before)
        # if self.creation_datetime_after:
        #     query = query.filter(database_object_class.creation_datetime >= self.creation_datetime_after)
        # if self.limit:
        #     query = query.limit(self.limit)

        # for order_by in self.order_by:
        #     query = query.order_by(getattr(database_object_class, order_by))
        # if self.offset:
        #     query = query.offset(self.offset)

        return query
