from datetime import datetime
from sqlmodel import Session, select

from .base_handler import BaseHandler
from copy import deepcopy
from models import (Project,
    ProjectDBCreate,
    ProjectDBRead,
    ProjectDB,
    ProjectFilter,
    TagDB,
    TagFilter,
    ResourceDB,
    ResourceFilter,
    ProcessDB,
    ProcessFilter,
    WorkflowDB,
    WorkflowFilter,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException


class ProjectHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_project(self, project: Project, detailed_output: bool = False) -> Project:
        self.context.logger.debug(f"Creating project: [{project.uid}]")

        # Validate allowed create Project
        await self.validate_can_create_project(project=project)

        with Session(self.context.database.engine) as session:
            create_obj = ProjectDBCreate.model_validate(project)
            create_obj = ProjectDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = ProjectDBRead.model_validate(create_obj)
            project = read_obj.return_data_obj()
        self.context.logger.info(f"Created project: [{project.uid}]")
        return project

    async def filter_projects(self, project_filter: ProjectFilter, detailed_output: bool = False) -> list[Project]:
        self.context.logger.debug(f"Filtering projects")
        with Session(self.context.database.engine) as session:
            query = select(ProjectDB)
            query = project_filter.apply_filters(ProjectDB, query)
            rows = session.exec(query).all()
            projects = []
            for row in rows:
                read_obj = ProjectDBRead.model_validate(row)
                project = read_obj.return_data_obj()
                projects.append(project)
        self.context.logger.debug(f"Filter projects found [{len(projects)}]")
        return projects

    async def find_project(self, project_uid: str, detailed_output: bool = False) -> Project:
        self.context.logger.debug(f"Find project: [{project_uid}]")
        with Session(self.context.database.engine) as session:
            query = select(ProjectDB)
            query = query.where(ProjectDB.uid == project_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No project found with uid: {project_uid}")
            read_obj = ProjectDBRead.model_validate(row)
            project = read_obj.return_data_obj()
        self.context.logger.debug(f"Project found: [{project.uid}]")
        return project

    async def update_project(self, project_uid: str, project: Project, detailed_output: bool = False) -> Project:
        self.context.logger.debug(f"Updating project: [{project_uid}]")

        # Validate allowed update Project
        await self.validate_can_update_project(project_uid=project_uid, project=project)

        with Session(self.context.database.engine) as session:
            query = select(ProjectDB)
            query = query.where(ProjectDB.uid == project_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No project found with uid: {project_uid}")

            # Verify data integrity
            immutable_fields = [
                'uid',
                'creation_datetime'
            ]
            immutable_modification_detected = []
            for key in immutable_fields:
                if getattr(row, key) != getattr(project, key):
                    immutable_modification_detected.append(key)
            if len(immutable_modification_detected) > 0:
                raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

            change_log = deepcopy(row.change_log)

            # Track changes
            changes = []
            for key in Project.__fields__.keys():
                if getattr(row, key) != getattr(project, key):
                    changes.append(key)
                    setattr(row, key, getattr(project, key))

            change_log_strs = []
            for change in changes:
                change_log_str = f"{change}: {getattr(row, change)} -> {getattr(project, change)}"
                change_log_strs.append(change_log_str)
            change_log[datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")] = ';'.join(change_log_strs)
            row.change_log = change_log

            row.update_datetime = datetime.utcnow()
            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = ProjectDBRead.model_validate(row)
            project = read_obj.return_data_obj()
        self.context.logger.info(f"Updated project: [{project.uid}]")
        return project

    async def set_activation(self, project_uid: str, active_state: bool) -> Project:
        self.context.logger.debug(f"Setting project activation: [{project_uid}] to [{active_state}]")

        project = await self.find_project(project_uid=project_uid)
        project.active = active_state
        project.cascade_active = active_state

        # Go through all sub resources here
        self.context.logger.debug(f"Cascade activation all resources in project: [{project_uid}] to [{active_state}]")
        with Session(self.context.database.engine) as session:
            # TAG
            tag_filter = TagFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            tag_query = select(TagDB)
            tag_query = tag_filter.apply_filters(TagDB, tag_query)
            rows = session.exec(tag_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade activation tag: [{row.uid}]")
                row.cascade_active = active_state
                session.add(row)

            # RESOURCE
            resource_filter = ResourceFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            resource_query = select(ResourceDB)
            resource_query = resource_filter.apply_filters(ResourceDB, resource_query)
            rows = session.exec(resource_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade activation resource: [{row.uid}]")
                row.cascade_active = active_state
                session.add(row)
            session.commit()

            # PROCESS
            process_filter = ProcessFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            process_query = select(ProcessDB)
            process_query = process_filter.apply_filters(ProcessDB, process_query)
            rows = session.exec(process_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade activation process: [{row.uid}]")
                row.cascade_active = active_state
                session.add(row)

            # WORKFLOW
            workflow_filter = WorkflowFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            workflow_query = select(WorkflowDB)
            workflow_query = workflow_filter.apply_filters(WorkflowDB, workflow_query)
            rows = session.exec(workflow_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade activation workflow: [{row.uid}]")
                row.cascade_active = active_state
                session.add(row)
            session.commit()

        project = await self.update_project(project_uid=project_uid, project=project)

        self.context.logger.info(f"Set project activation: [{project.uid}]")
        return project

    async def delete_project(self, project_uid: str) -> Project:
        self.context.logger.debug(f"Deleting Project: [{project_uid}]")

        project = await self.find_project(project_uid=project_uid)
        project.deleted = True
        project.cascade_deleted = True

        # Go through all sub resources here
        self.context.logger.debug(f"Cascade deleting all resources in project: [{project_uid}]")
        with Session(self.context.database.engine) as session:
            # TAG
            tag_filter = TagFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            tag_query = select(TagDB)
            tag_query = tag_filter.apply_filters(TagDB, tag_query)
            rows = session.exec(tag_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade deleting tag: [{row.uid}]")
                row.cascade_deleted = True
                session.add(row)

            # RESOURCE
            resource_filter = ResourceFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            resource_query = select(ResourceDB)
            resource_query = resource_filter.apply_filters(ResourceDB, resource_query)
            rows = session.exec(resource_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade deleting resource: [{row.uid}]")
                row.cascade_deleted = True
                session.add(row)

            # PROCESS
            process_filter = ProcessFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            process_query = select(ProcessDB)
            process_query = process_filter.apply_filters(ProcessDB, process_query)
            rows = session.exec(process_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade deleting process: [{row.uid}]")
                row.cascade_deleted = True
                session.add(row)

            # WORKFLOW
            workflow_filter = WorkflowFilter(project_uid=[project_uid], active='ANY', deleted='ANY', cascade_active='ANY', cascade_deleted='ANY')
            workflow_query = select(WorkflowDB)
            workflow_query = workflow_filter.apply_filters(WorkflowDB, workflow_query)
            rows = session.exec(workflow_query).all()
            for row in rows:
                self.context.logger.debug(f"Cascade deleting workflow: [{row.uid}]")
                row.cascade_deleted = True
                session.add(row)
            session.commit()

        project = await self.update_project(project_uid=project_uid, project=project)

        self.context.logger.info(f"Project deleted: [{project.uid}]")
        return project


    async def validate_can_create_project(self, project: Project) -> None:
        project_filter = ProjectFilter(
            name=[project.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ProjectDB)
            query = project_filter.apply_filters(ProjectDB, query)
            rows = session.exec(query).all()
            if rows:
                raise DuplicateRecordsException(f"Project with name [{project.name}] already exists")

    async def validate_can_update_project(self, project_uid: str, project: Project) -> None:
        project_filter = ProjectFilter(
            name=[project.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ProjectDB)
            query = project_filter.apply_filters(ProjectDB, query)
            rows = session.exec(query).all()
            """
            if rows == 0 there are no records with the name and you can update
            if rows == 1 and the uuids match its fine
            if rows == 1 and the uuids do not match error
            if rows > 1 error
            """
            if len(rows) == 1:
                if rows[0].uid != project_uid:
                    raise DuplicateRecordsException(f"Project with name [{project.name}] already exists")
            elif len(rows) > 1:
                raise DuplicateRecordsException(f"Project with name [{project.name}] already exists")
