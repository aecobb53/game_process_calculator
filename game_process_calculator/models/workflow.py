from datetime import datetime
from typing import List, Optional, Dict, Union, Self
from enum import Enum
from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
from pydantic import BaseModel, model_validator
from uuid import uuid4

from . import GPCBaseModel, GPCFilter, Project, Tag, Resource

from models import Tag, Project, Process, Resource

class ProcessType(Enum):
    LINEAR = 'LINEAR'
    PARALLEL = 'PARALLEL'
#     WEB = 'web'


class Workflow(GPCBaseModel):
    # uid: str
    # creation_datetime: datetime
    # notes: List[str] | None = None  # Notes more for me than anybody else
    # description: str | None = None  # Description to be displayed
    # active: bool  # If the record is not currently active
    # deleted: bool  # If the record is marked as deleted
    # cascade_active: bool  # Links a project to an active toggle
    # cascade_deleted: bool  # If a cascade delete is called for, this gets set so the record is unchanged

    update_datetime: datetime | None = None
    notes: List[str] | None = None  # Notes more for me than anybody else
    change_log: Dict = {}  # A dict of timestamps and changes

    name: str
    project: Project | None = None
    project_uid: str | None = None
    tags: List[Tag] = []  # The actual list of tag objects after being loaded from the table
    tag_uids: List[str] = []  # The actual list of tag objects after being loaded from the table
    process_type: ProcessType
    processes: List[Process] | None = None
    process_uids: List[str] | None = None
    focus_resource: Resource | None = None
    focus_resource_uid: str | None = None

    parallel_processes_counter: Dict[str, int] | None = None
    resource_throughputs_per_second: Dict[str, float] | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
        # if fields.get('uid') is None:
        #     fields['uid'] = str(uuid4())
        # if fields.get('creation_datetime') is None:
        #     fields['creation_datetime'] = datetime.now()
        if not fields.get('project') and not fields.get('project_uid'):
            raise ValueError("A project or project_uid must be provided to create a resource")
        return fields

    # @model_validator(mode='after')
    # def validate_fields(cls, fields):
    #     fields.parallel_processes_counter = [{i: 1} for i in fields.process_uids]
    #     return fields

class WorkflowDBBase(SQLModel):
    id: int | None = Field(primary_key=True, default=None)
    uid: str = Field(unique=True)
    creation_datetime: datetime
    update_datetime: datetime | None = None
    notes: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    description: str | None = None
    tag_uids: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    change_log: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
    active: bool
    deleted: bool
    cascade_active: bool
    cascade_deleted: bool

    name: str
    project_uid: str = Field(foreign_key="project.uid")
    process_type: str
    process_uids: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    focus_resource_uid: str | None = None

    def cast_data_object(self, data_object_class) -> Workflow:
        """Return a data object based on the data_object_class"""
        content = self.dict()
        data_obj = data_object_class(**content)
        return data_obj

    def return_data_obj(self) -> Workflow:
        print('IN RETURN DATA')
        obj = Workflow(**self.dict())
        return obj

class WorkflowDBCreate(WorkflowDBBase):
    @model_validator(mode='before')
    def validate_fields(cls, fields):
        if 'id' in fields:
            del fields['id']
        if 'creation_datetime' in fields:
            del fields['creation_datetime']
        return fields


class WorkflowDBRead(WorkflowDBBase):
    pass


class WorkflowDB(WorkflowDBBase, table=True):
    __tablename__ = "workflow"


class WorkflowFilter(GPCFilter):
    # uid: List[str] | None = None
    name: List[str] | None = None
    project_uid: List[str] | None = None
    # tag_uids

    process_type: List[str] | None = None
    process_uids: List[str] | None = None
    focus_resource: List[str] | None = None

    @model_validator(mode='before')
    def validate_fields(cls, fields):
        fields = super().validate_fields(fields)
        if isinstance(fields.get('process_time_seconds_above'), list):
            fields['process_time_seconds_above'] = fields['process_time_seconds_above'][0]
        if isinstance(fields.get('process_time_seconds_below'), list):
            fields['process_time_seconds_below'] = fields['process_time_seconds_below'][0]
        if isinstance(fields.get('rest_time_seconds_above'), list):
            fields['rest_time_seconds_above'] = fields['rest_time_seconds_above'][0]
        if isinstance(fields.get('rest_time_seconds_below'), list):
            fields['rest_time_seconds_below'] = fields['rest_time_seconds_below'][0]
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

    def apply_filters(self, database_object_class: WorkflowDBBase, query: select) -> select:
        """Apply the filters to the query"""
        query = super().apply_filters(database_object_class, query)
        # if self.uid:
        #     query = query.filter(database_object_class.uid.in_(self.uid))
        if self.name:
            query = query.filter(database_object_class.name.in_(self.name))
        if self.project_uid:
            query = query.filter(database_object_class.project_uid.in_(self.project_uid))

        if self.process_type:
            query = query.filter(database_object_class.process_type.in_(self.process_type))
        if self.process_uids:
            query = query.filter(database_object_class.process_uids.in_(self.process_uids))
        if self.focus_resource:
            query = query.filter(database_object_class.focus_resource_uid.in_(self.focus_resource))

        return query










# from datetime import datetime
# from enum import Enum
# from typing import List, Optional, Dict, Union, Self
# from sqlmodel import Field, SQLModel, JSON, ARRAY, String, Column, UniqueConstraint, select
# from pydantic import BaseModel, model_validator
# from uuid import uuid4

# from . import Project, Tag, Resource, Process


# class WorkflowType(Enum):
#     LINEAR = 'linear'
#     PARALLEL = 'parallel'
#     WEB = 'web'


# class Workflow(BaseModel):
#     uid: str
#     creation_datetime: datetime
#     update_datetime: datetime | None = None
#     notes: List[str] | None = None  # Notes more for me than anybody else
#     description: str | None = None  # Description to be displayed
#     tags: List[Tag]  # The actual list of tag objects after being loaded from the table
#     change_log: Dict = {}  # A dict of timestamps and changes
#     active: bool  # If the record is not currently active
#     deleted: bool  # If the record is marked as deleted
#     cascade_active: bool  # Links a project to an active toggle
#     cascade_delete: bool  # If a cascade delete is called for, this gets set so the record is unchanged

#     name: str
#     project: Project
#     process_type: ProcessType
#     processes: Process
#     focus_resource: Resource

#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         if fields.get('uid') is None:
#             fields['uid'] = str(uuid4())
#         if fields.get('creation_datetime') is None:
#             fields['creation_datetime'] = datetime.now()
#         return fields


# class WorkflowDBBase(SQLModel):
#     id: int = Field(primary_key=True)
#     uid: str = Field(unique=True)
#     creation_datetime: datetime
#     update_datetime: datetime | None = None
#     notes: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
#     description: str | None = None
#     tag_uids: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
#     change_log: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
#     active: bool
#     deleted: bool
#     cascade_active: bool
#     cascade_delete: bool

#     name: str
#     project_uid: str = Field(foreign_key="project.uid")
#     process_type: str
#     process_uids: List[str] | None = Field(default_factory=list, sa_column=Column(ARRAY(String)))
#     focus_resource_uid: str

#     def cast_data_object(self, data_object_class) -> Workflow:
#         """Return a data object based on the data_object_class"""
#         content = self.dict()
#         data_obj = data_object_class(**content)
#         return data_obj


# class WorkflowDBCreate(WorkflowDBBase):
#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         if 'id' in fields:
#             del fields['id']
#         if 'creation_datetime' in fields:
#             del fields['creation_datetime']
#         return fields


# class WorkflowDBRead(WorkflowDBBase):
#     pass


# class WorkflowDB(WorkflowDBBase, table=True):
#     __tablename__ = "workflow"


# class WorkflowFilter(BaseModel):
#     uid: List[str] | None = None
#     name: List[str] | None = None
#     project_uid: List[str] | None = None
#     process_type: List[str] | None = None
#     process_uid: List[str] | None = None
#     focus_resource_uid: List[str] | None = None
#     active: bool | None = None
#     deleted: bool | None = None
#     cascade_active: bool | None = None
#     cascade_delete: bool | None = None

#     creation_datetime_before: datetime | None = None
#     creation_datetime_after: datetime | None = None
#     limit: int = 1000

#     order_by: List[str] = ['creation_datetime']

#     @model_validator(mode='before')
#     def validate_fields(cls, fields):
#         if isinstance(fields.get('active'), list):
#             fields['active'] = fields['active'][0]
#         if isinstance(fields.get('deleted'), list):
#             fields['deleted'] = fields['deleted'][0]
#         if isinstance(fields.get('cascade_active'), list):
#             fields['cascade_active'] = fields['cascade_active'][0]
#         if isinstance(fields.get('cascade_delete'), list):
#             fields['cascade_delete'] = fields['cascade_delete'][0]
#         if isinstance(fields.get('creation_datetime_before'), list):
#             fields['creation_datetime_before'] = fields['creation_datetime_before'][0]
#         if isinstance(fields.get('creation_datetime_after'), list):
#             fields['creation_datetime_after'] = fields['creation_datetime_after'][0]
#         return fields

#     def apply_filters(self, database_object_class: WorkflowDBBase, query: select) -> select:
#         """Apply the filters to the query"""
#         if self.uid:
#             query = query.filter(database_object_class.uid.in_(self.uid))
#         if self.name:
#             query = query.filter(database_object_class.name.in_(self.name))
#         if self.project_uid:
#             query = query.filter(database_object_class.project_uid.in_(self.project_uid))
#         if self.process_type:
#             query = query.filter(database_object_class.process_type.in_(self.process_type))
#         if self.process_uid:
#             query = query.filter(database_object_class.process_uid.in_(self.process_uid))
#         if self.focus_resource_uid:
#             query = query.filter(database_object_class.focus_resource_uid.in_(self.focus_resource_uid))
#         if self.active is not None:
#             query = query.filter(database_object_class.active == self.active)
#         if self.deleted is not None:
#             query = query.filter(database_object_class.deleted == self.deleted)
#         if self.cascade_active is not None:
#             query = query.filter(database_object_class.cascade_active == self.cascade_active)
#         if self.cascade_delete is not None:
#             query = query.filter(database_object_class.cascade_delete == self.cascade_delete)

#         if self.creation_datetime_before:
#             query = query.filter(database_object_class.creation_datetime <= self.creation_datetime_before)
#         if self.creation_datetime_after:
#             query = query.filter(database_object_class.creation_datetime >= self.creation_datetime_after)
#         if self.limit:
#             query = query.limit(self.limit)

#         for order_by in self.order_by:
#             query = query.order_by(getattr(database_object_class, order_by))

#         return query
