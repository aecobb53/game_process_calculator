from datetime import datetime
from sqlmodel import Session, select

from .base_handler import BaseHandler
from copy import deepcopy
from models import (TagFilter,
    ResourceFilter,
    Process,
    ProcessDBCreate,
    ProcessDBRead,
    ProcessDB,
    ProcessFilter,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException
from . import ProjectHandler, TagHandler, ResourceHandler


class ProcessHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_process(self, process: Process, detailed_output: bool = False) -> Process:
        self.context.logger.debug(f"Creating process: [{process.uid}] for project: [{process.project_uid}]")

        # Validate allowed create Process
        await self.validate_can_create_process(process=process)
        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()

        with Session(self.context.database.engine) as session:
            create_obj = ProcessDBCreate.model_validate(process)
            create_obj = ProcessDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = ProcessDBRead.model_validate(create_obj)
            process = read_obj.return_data_obj()

            if detailed_output:
                process.project = await ph.find_project(process.project_uid)
                if process.tag_uids:
                    process.tags = await th.filter_tags(TagFilter(uid=process.tag_uids), detailed_output=detailed_output)
                process.consume_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.consume_resource_uids.keys())), detailed_output=detailed_output)
                process.produce_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.produce_resource_uids.keys())), detailed_output=detailed_output)
                if process.machine_used_uid:
                    process.machine_used = await rh.find_resource(resource_uid=process.machine_used_uid)

        self.context.logger.info(f"Created process: [{process.uid}]")
        return process

    async def filter_processes(self, process_filter: ProcessFilter, detailed_output: bool = False) -> list[Process]:
        self.context.logger.debug(f"Filtering processes")

        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()

        with Session(self.context.database.engine) as session:
            query = select(ProcessDB)
            query = process_filter.apply_filters(ProcessDB, query)
            rows = session.exec(query).all()
            processes = []
            for row in rows:
                read_obj = ProcessDBRead.model_validate(row)
                data_obj = read_obj.return_data_obj()

                if detailed_output:
                    data_obj.project = await ph.find_project(data_obj.project_uid)
                    if data_obj.tag_uids:
                        data_obj.tags = await th.filter_tags(TagFilter(uid=data_obj.tag_uids), detailed_output=detailed_output)
                    data_obj.consume_resources = await rh.filter_resources(
                        ResourceFilter(uid=list(data_obj.consume_resource_uids.keys())), detailed_output=detailed_output)
                    data_obj.produce_resources = await rh.filter_resources(
                        ResourceFilter(uid=list(data_obj.produce_resource_uids.keys())), detailed_output=detailed_output)
                    if data_obj.machine_used_uid:
                        data_obj.machine_used = await rh.find_resource(resource_uid=data_obj.machine_used_uid)

                processes.append(data_obj)
        self.context.logger.debug(f"Filter processes found [{len(processes)}]")
        return processes

    async def find_process(self, process_uid: str, detailed_output: bool = False) -> Process:
        self.context.logger.debug(f"Find process: [{process_uid}]")

        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()

        with Session(self.context.database.engine) as session:
            query = select(ProcessDB)
            query = query.where(ProcessDB.uid == process_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No process found with uid: {process_uid}")
            read_obj = ProcessDBRead.model_validate(row)
            process = read_obj.return_data_obj()

            if detailed_output:
                process.project = await ph.find_project(process.project_uid)
                if process.tag_uids:
                    process.tags = await th.filter_tags(TagFilter(uid=process.tag_uids), detailed_output=detailed_output)
                process.consume_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.consume_resource_uids.keys())), detailed_output=detailed_output)
                process.produce_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.produce_resource_uids.keys())), detailed_output=detailed_output)
                if process.machine_used_uid:
                    process.machine_used = await rh.find_resource(resource_uid=process.machine_used_uid)

        self.context.logger.debug(f"Created process: [{process.uid}]")
        return process

    async def update_process(self, process_uid: str, process: Process, detailed_output: bool = False) -> Process:
        self.context.logger.debug(f"Updating process: [{process_uid}]")

        # Validate allowed update Process
        await self.validate_can_update_process(process_uid=process_uid, process=process)
        ph = ProjectHandler()
        th = TagHandler()
        rh = ResourceHandler()

        with Session(self.context.database.engine) as session:
            query = select(ProcessDB)
            query = query.where(ProcessDB.uid == process_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No process found with uid: {process_uid}")

            # Verify data integrity
            immutable_fields = [
                'uid',
                'creation_datetime'
            ]
            immutable_modification_detected = []
            for key in immutable_fields:
                if getattr(row, key) != getattr(process, key):
                    immutable_modification_detected.append(key)
            if len(immutable_modification_detected) > 0:
                raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

            change_log = deepcopy(row.change_log)

            # Track changes
            changes = []
            for key in Process.__fields__.keys():
                try:
                    if getattr(row, key) != getattr(process, key):
                        changes.append(key)
                        setattr(row, key, getattr(process, key))
                except AttributeError:
                    pass

            change_log_strs = []
            for change in changes:
                change_log_str = f"{change}: {getattr(row, change)} -> {getattr(process, change)}"
                change_log_strs.append(change_log_str)
            change_log[datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")] = ';'.join(change_log_strs)
            row.change_log = change_log

            row.update_datetime = datetime.utcnow()
            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = ProcessDBRead.model_validate(row)
            process = read_obj.return_data_obj()

            if detailed_output:
                process.project = await ph.find_project(process.project_uid)
                if process.tag_uids:
                    process.tags = await th.filter_tags(TagFilter(uid=process.tag_uids), detailed_output=detailed_output)
                process.consume_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.consume_resource_uids.keys())), detailed_output=detailed_output)
                process.produce_resources = await rh.filter_resources(
                    ResourceFilter(uid=list(process.produce_resource_uids.keys())), detailed_output=detailed_output)
                if process.machine_used_uid:
                    process.machine_used = await rh.find_resource(resource_uid=process.machine_used_uid)

        self.context.logger.info(f"Updated process: [{process.uid}]")
        return process

    async def set_activation(self, process_uid: str, active_state: bool) -> Process:
        self.context.logger.debug(f"Setting process activation: [{process_uid}] to [{active_state}]")

        process = await self.find_process(process_uid=process_uid)
        process.active = active_state
        process.cascade_active = active_state

        process = await self.update_process(process_uid=process_uid, process=process)

        self.context.logger.info(f"Set process activation: [{process.uid}]")
        return process

    async def delete_process(self, process_uid: str) -> Process:
        self.context.logger.debug(f"Deleting Process: [{process_uid}]")

        process = await self.find_process(process_uid=process_uid)
        process.deleted = True
        process.cascade_deleted = True

        process = await self.update_process(process_uid=process_uid, process=process)

        self.context.logger.info(f"Process deleted: [{process.uid}]")
        return process


    async def validate_can_create_process(self, process: Process) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=process.project_uid)
        if process.project_uid != project.uid:
            raise DataIntegrityException("Process project_uid does not match project_uid")
        process.project = project
        process_filter = ProcessFilter(
            project_uid=[process.project.uid],
            name=[process.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ProcessDB)
            query = process_filter.apply_filters(ProcessDB, query)
            rows = session.exec(query).all()
            if rows:
                raise DuplicateRecordsException(f"Process with name [{process.name}] already exists")

    async def validate_can_update_process(self, process_uid: str, process: Process) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=process.project_uid)
        if process.project_uid != project.uid:
            raise DataIntegrityException("Process project_uid does not match project_uid")
        process.project = project
        process_filter = ProcessFilter(
            name=[process.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ProcessDB)
            query = process_filter.apply_filters(ProcessDB, query)
            rows = session.exec(query).all()
            """
            if rows == 0 there are no records with the name and you can update
            if rows == 1 and the uuids match its fine
            if rows == 1 and the uuids do not match error
            if rows > 1 error
            """
            if len(rows) == 1:
                if rows[0].uid != process_uid:
                    raise DuplicateRecordsException(f"Process with name [{process.name}] already exists")
            elif len(rows) > 1:
                raise DuplicateRecordsException(f"Process with name [{process.name}] already exists")
