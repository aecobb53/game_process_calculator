from datetime import datetime
from copy import deepcopy
from typing import List, Optional, Dict, Union
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from uuid import uuid4

from . import GPCBaseModel, GPCFilter, Project


class Tag(GPCBaseModel):
    # uid: str
    # creation_datetime: datetime
    # description: str | None = None  # Description to be displayed
    # active: bool  # If the record is not currently active
    # deleted: bool  # If the record is marked as deleted
    # cascade_active: bool  # Links a project to an active toggle
    # cascade_deleted: bool  # If a cascade delete is called for, this gets set so the record is unchanged

    name: str
    project: Project | None = None
    project_uid: str | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
        # if fields.get('uid') is None:
        #     fields['uid'] = str(uuid4())
        # if fields.get('creation_datetime') is None:
        #     fields['creation_datetime'] = datetime.now()
        # if fields.get('active') is None:
        #     fields['active'] = True
        # if fields.get('deleted') is None:
        #     fields['deleted'] = False
        # if fields.get('cascade_active') is None:
        #     fields['cascade_active'] = True
        # if fields.get('cascade_deleted') is None:
        #     fields['cascade_deleted'] = False

        if not fields.get('project') and not fields.get('project_uid'):
            raise ValueError("A project or project_uid must be provided to create a resource")
        return fields


class TagDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    creation_datetime: datetime
    description: str | None = None
    active: bool
    deleted: bool
    cascade_active: bool
    cascade_deleted: bool

    name: str
    project_uid: str = Field(foreign_key='project.uid')

    def cast_data_object(self, data_object_class) -> Tag:
        """Return a data object based on the data_object_class"""
        content = self.dict()
        data_obj = data_object_class(**content)
        return data_obj


class TagDBCreate(TagDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if 'id' in fields:
            del fields['id']
        if 'creation_datetime' in fields:
            del fields['creation_datetime']
        return fields


class TagDBRead(TagDBBase):
    def return_data_obj(self) -> Tag:
        obj = Tag(**self.dict())
        return obj


class TagDB(TagDBBase, table=True):
    __tablename__ = "tag"


class TagFilter(GPCFilter):
    # uid: List[str] | None = None
    project_uid: List[str] | None = None
    name: List[str] | None = None
    # active: bool | None | str = True
    # deleted: bool | None | str = False
    # cascade_active: bool | None | str = True
    # cascade_deleted: bool | None | str = False

    # creation_datetime_before: datetime | None = None
    # creation_datetime_after: datetime | None = None
    # limit: int = 1000

    # order_by: List[str] = ['creation_datetime']

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
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

    def apply_filters(self, database_object_class: TagDBBase, query: select) -> select:
        """Apply the filters to the query"""
        query = super().apply_filters(database_object_class, query)
        # if self.uid:
        #     query = query.filter(database_object_class.uid.in_(self.uid))
        if self.project_uid:
            query = query.filter(database_object_class.project_uid.in_(self.project_uid))
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

        return query

