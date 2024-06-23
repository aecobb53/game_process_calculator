from datetime import datetime
from enum import Enum
from sqlmodel import Session, select

from .base_handler import BaseHandler
from copy import deepcopy
from models import (TagFilter,
    ProcessFilter,
    Workflow,
    WorkflowDBCreate,
    WorkflowDBRead,
    WorkflowDB,
    WorkflowFilter,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException
from . import ProjectHandler, TagHandler, ResourceHandler, ProcessHandler


class WorkflowHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_workflow(self, workflow: Workflow) -> Workflow:
        self.context.logger.debug(f"Creating workflow: [{workflow.uid}] for project: [{workflow.project_uid}]")

        # Validate allowed create Workflow
        await self.validate_can_create_workflow(workflow=workflow)
        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()
        prh = ProcessHandler()

        with Session(self.context.database.engine) as session:
            create_obj = WorkflowDBCreate.model_validate(workflow)
            create_obj = WorkflowDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = WorkflowDBRead.model_validate(create_obj)
            workflow = read_obj.return_data_obj()

            workflow.project = await ph.find_project(workflow.project_uid)
            if workflow.tag_uids:
                workflow.tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
            if workflow.focus_resource_uid:
                workflow.focus_resource = await rh.find_resource(workflow.focus_resource_uid)
            if workflow.process_uids:
                workflow.processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))

        self.context.logger.info(f"Created workflow: [{workflow.uid}]")
        return workflow

    async def filter_workflows(self, workflow_filter: WorkflowFilter) -> list[Workflow]:
        self.context.logger.debug(f"Filtering workflows")

        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()
        prh = ProcessHandler()

        with Session(self.context.database.engine) as session:
            query = select(WorkflowDB)
            query = workflow_filter.apply_filters(WorkflowDB, query)
            rows = session.exec(query).all()
            workflows = []
            for row in rows:
                read_obj = WorkflowDBRead.model_validate(row)
                workflow = read_obj.return_data_obj()

                workflow.project = await ph.find_project(workflow.project_uid)
                if workflow.tag_uids:
                    workflow.tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
                if workflow.focus_resource_uid:
                    workflow.focus_resource = await rh.find_resource(workflow.focus_resource_uid)
                if workflow.process_uids:
                    workflow.processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))

                workflows.append(workflow)
        self.context.logger.debug(f"Filter workflows found [{len(workflows)}]")
        return workflows

    async def find_workflow(self, workflow_uid: str) -> Workflow:
        self.context.logger.debug(f"Find workflow: [{workflow_uid}]")

        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()
        prh = ProcessHandler()

        with Session(self.context.database.engine) as session:
            query = select(WorkflowDB)
            query = query.where(WorkflowDB.uid == workflow_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No workflow found with uid: {workflow_uid}")
            read_obj = WorkflowDBRead.model_validate(row)
            workflow = read_obj.return_data_obj()

            workflow.project = await ph.find_project(workflow.project_uid)
            if workflow.tag_uids:
                workflow.tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
            if workflow.focus_resource_uid:
                workflow.focus_resource = await rh.find_resource(workflow.focus_resource_uid)
            if workflow.process_uids:
                workflow.processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))

        self.context.logger.debug(f"Created workflow: [{workflow.uid}]")
        return workflow

    async def update_workflow(self, workflow_uid: str, workflow: Workflow) -> Workflow:
        self.context.logger.debug(f"Updating workflow: [{workflow_uid}]")

        # Validate allowed update Workflow
        await self.validate_can_update_workflow(workflow_uid=workflow_uid, workflow=workflow)
        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()
        prh = ProcessHandler()

        with Session(self.context.database.engine) as session:
            query = select(WorkflowDB)
            query = query.where(WorkflowDB.uid == workflow_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No workflow found with uid: {workflow_uid}")

            # Verify data integrity
            immutable_fields = [
                'uid',
                'creation_datetime',
            ]
            immutable_modification_detected = []
            for key in immutable_fields:
                if getattr(row, key) != getattr(workflow, key):
                    immutable_modification_detected.append(key)
            if len(immutable_modification_detected) > 0:
                raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

            change_log = deepcopy(row.change_log)

            # Track changes
            changes = []
            for key in Workflow.__fields__.keys():
                try:
                    workflow_value = getattr(workflow, key)
                    if isinstance(workflow_value, Enum):
                        workflow_value = workflow_value.value
                    if getattr(row, key) != workflow_value:
                        changes.append(key)
                        setattr(row, key, getattr(workflow, key))
                except AttributeError:
                    pass

            change_log_strs = []
            for change in changes:
                change_log_str = f"{change}: {getattr(row, change)} -> {getattr(workflow, change)}"
                change_log_strs.append(change_log_str)
            change_log[datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")] = ';'.join(change_log_strs)
            row.change_log = change_log

            row.update_datetime = datetime.utcnow()
            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = WorkflowDBRead.model_validate(row)
            workflow = read_obj.return_data_obj()

            workflow.project = await ph.find_project(workflow.project_uid)
            if workflow.tag_uids:
                workflow.tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
            if workflow.focus_resource_uid:
                workflow.focus_resource = await rh.find_resource(workflow.focus_resource_uid)
            if workflow.process_uids:
                workflow.processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))

        self.context.logger.info(f"Updated workflow: [{workflow.uid}]")
        return workflow

    async def set_activation(self, workflow_uid: str, active_state: bool) -> Workflow:
        self.context.logger.debug(f"Setting workflow activation: [{workflow_uid}] to [{active_state}]")

        workflow = await self.find_workflow(workflow_uid=workflow_uid)
        workflow.active = active_state
        workflow.cascade_active = active_state

        await self.update_workflow(workflow_uid=workflow_uid, workflow=workflow)

        self.context.logger.info(f"Set workflow activation: [{workflow.uid}]")
        return workflow

    async def delete_workflow(self, workflow_uid: str) -> Workflow:
        self.context.logger.debug(f"Deleting Workflow: [{workflow_uid}]")

        workflow = await self.find_workflow(workflow_uid=workflow_uid)
        workflow.deleted = True
        workflow.cascade_deleted = True

        await self.update_workflow(workflow_uid=workflow_uid, workflow=workflow)

        self.context.logger.info(f"Workflow deleted: [{workflow.uid}]")
        return workflow


    async def validate_can_create_workflow(self, workflow: Workflow) -> None:
        # Validate Project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=workflow.project_uid)
        if workflow.project_uid != project.uid:
            raise DataIntegrityException("Workflow project_uid does not match project_uid")
        # Validate Tags
        th = TagHandler()
        if workflow.tag_uids:
            tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
            if any([t for t in workflow.tag_uids if t not in [tag.uid for tag in tags]]):
                raise DataIntegrityException("Workflow tag_uids contain invalid tag_uids")
        # Validate Resources
        rh = ResourceHandler()
        if workflow.focus_resource_uid:
            resource = await rh.find_resource(resource_uid=workflow.focus_resource_uid)
            if workflow.focus_resource_uid != resource.uid:
                raise DataIntegrityException("Workflow focus_resource_uid does not match resource_uid")
        # Validate Process
        prh = ProcessHandler()
        if workflow.process_uids:
            processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))
            if any([p for p in workflow.process_uids if p not in [process.uid for process in processes]]):
                raise DataIntegrityException("Workflow process_uids contain invalid process_uids")
        workflow.project = project
        workflow_filter = WorkflowFilter(
            project_uid=[workflow.project.uid],
            name=[workflow.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(WorkflowDB)
            query = workflow_filter.apply_filters(WorkflowDB, query)
            rows = session.exec(query).all()
            if rows:
                raise DuplicateRecordsException(f"Workflow with name [{workflow.name}] already exists")

    async def validate_can_update_workflow(self, workflow_uid: str, workflow: Workflow) -> None:
        # Validate Project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=workflow.project_uid)
        if workflow.project_uid != project.uid:
            raise DataIntegrityException("Workflow project_uid does not match project_uid")
        # Validate Tags
        th = TagHandler()
        if workflow.tag_uids:
            tags = await th.filter_tags(TagFilter(uid=workflow.tag_uids))
            if any([t for t in workflow.tag_uids if t not in [tag.uid for tag in tags]]):
                raise DataIntegrityException("Workflow tag_uids contain invalid tag_uids")
        # Validate Resources
        rh = ResourceHandler()
        if workflow.focus_resource_uid:
            resource = await rh.find_resource(resource_uid=workflow.focus_resource_uid)
            if workflow.focus_resource_uid != resource.uid:
                raise DataIntegrityException("Workflow focus_resource_uid does not match resource_uid")
        # Validate Process
        prh = ProcessHandler()
        if workflow.process_uids:
            processes = await prh.filter_processes(ProcessFilter(uid=workflow.process_uids))
            if any([p for p in workflow.process_uids if p not in [process.uid for process in processes]]):
                raise DataIntegrityException("Workflow process_uids contain invalid process_uids")
        workflow.project = project
        workflow_filter = WorkflowFilter(
            name=[workflow.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(WorkflowDB)
            query = workflow_filter.apply_filters(WorkflowDB, query)
            rows = session.exec(query).all()
            """
            if rows == 0 there are no records with the name and you can update
            if rows == 1 and the uuids match its fine
            if rows == 1 and the uuids do not match error
            if rows > 1 error
            """
            if len(rows) == 1:
                if rows[0].uid != workflow_uid:
                    raise DuplicateRecordsException(f"Workflow with name [{workflow.name}] already exists")
            elif len(rows) > 1:
                raise DuplicateRecordsException(f"Workflow with name [{workflow.name}] already exists")
