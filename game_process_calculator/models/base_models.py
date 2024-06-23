from datetime import datetime
from typing import List, Optional, Dict, Union
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from uuid import uuid4


class GPCBaseModel(BaseModel):
    uid: str
    creation_datetime: datetime
    # update_datetime: datetime | None = None
    # notes: List[str] | None = None  # Notes more for me than anybody else
    description: str | None = None  # Description to be displayed
    # change_log: Dict = {}  # A dict of timestamps and changes
    active: bool  # If the record is not currently active
    deleted: bool  # If the record is marked as deleted
    cascade_active: bool  # Links a project to an active toggle
    cascade_deleted: bool  # If a cascade delete is called for, this gets set so the record is unchanged

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if fields.get('uid') is None:
            fields['uid'] = str(uuid4())
        if fields.get('creation_datetime') is None:
            fields['creation_datetime'] = datetime.now()

        if fields.get('active') is None:
            fields['active'] = True
        if fields.get('deleted') is None:
            fields['deleted'] = False
        if fields.get('cascade_active') is None:
            fields['cascade_active'] = True
        if fields.get('cascade_deleted') is None:
            fields['cascade_deleted'] = False

        return fields


# class GPCDBBase(SQLModel):
#     id: int = Field(primary_key=True)
#     uid: str = Field(unique=True)
#     creation_datetime: datetime
#     update_datetime: datetime | None = None
#     notes: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
#     description: str | None = None
#     change_log: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
#     active: bool
#     deleted: bool
#     cascade_active: bool
#     cascade_delete: bool

#     # __table_args__ = (UniqueConstraint('uid', 'name'))

#     def cast_data_object(self, data_object_class) -> GPCBaseModel:
#         """Return a data object based on the data_object_class"""
#         content = self.dict()
#         data_obj = data_object_class(**content)
#         return data_obj


# class GPCDBCreate(GPCDBBase):
#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         if 'id' in fields:
#             del fields['id']
#         if 'creation_datetime' in fields:
#             del fields['creation_datetime']
#         return fields


# class GPCDBRead(GPCDBBase):
#     pass


# class GPCDB(GPCDBBase):
#     pass

class GPCFilter(BaseModel):
    uid: List[str] | None = None
    active: bool | None | str = True
    deleted: bool | None | str = False
    cascade_active: bool | None | str = True
    cascade_deleted: bool | None | str = False

    creation_datetime_before: datetime | None = None
    creation_datetime_after: datetime | None = None
    limit: int = 1000

    order_by: List[str] = ['creation_datetime']
    offset: int = 0

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if isinstance(fields.get('active'), list):
            fields['active'] = fields['active'][0]
        if isinstance(fields.get('deleted'), list):
            fields['deleted'] = fields['deleted'][0]
        if isinstance(fields.get('cascade_active'), list):
            fields['cascade_active'] = fields['cascade_active'][0]
        if isinstance(fields.get('cascade_deleted'), list):
            fields['cascade_deleted'] = fields['cascade_deleted'][0]
        if isinstance(fields.get('creation_datetime_before'), list):
            fields['creation_datetime_before'] = fields['creation_datetime_before'][0]
        if isinstance(fields.get('creation_datetime_after'), list):
            fields['creation_datetime_after'] = fields['creation_datetime_after'][0]
        if isinstance(fields.get('limit'), list):
            fields['limit'] = fields['limit'][0]
        if isinstance(fields.get('offset'), list):
            fields['offset'] = fields['offset'][0]
        return fields

    def apply_filters(self, database_object_class, query: select) -> select:
        """Apply the filters to the query"""
        if self.uid:
            query = query.filter(database_object_class.uid.in_(self.uid))
        # if self.project_uid:
        #     query = query.filter(database_object_class.project_uid.in_(self.project_uid))
        # if self.name:
        #     query = query.filter(database_object_class.name.in_(self.name))
        if self.active is not None:
            if not isinstance(self.active, str):
                query = query.filter(database_object_class.active == self.active)
        if self.deleted is not None:
            if not isinstance(self.deleted, str):
                query = query.filter(database_object_class.deleted == self.deleted)
        if self.cascade_active is not None:
            if not isinstance(self.cascade_active, str):
                query = query.filter(database_object_class.cascade_active == self.cascade_active)
        if self.cascade_deleted is not None:
            if not isinstance(self.cascade_deleted, str):
                query = query.filter(database_object_class.cascade_deleted == self.cascade_deleted)

        if self.creation_datetime_before:
            query = query.filter(database_object_class.creation_datetime <= self.creation_datetime_before)
        if self.creation_datetime_after:
            query = query.filter(database_object_class.creation_datetime >= self.creation_datetime_after)
        if self.limit:
            query = query.limit(self.limit)

        for order_by in self.order_by:
            query = query.order_by(getattr(database_object_class, order_by))
        if self.offset:
            query = query.offset(self.offset)

        return query
