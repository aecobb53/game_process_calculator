from datetime import datetime
from sqlmodel import Session, select

from .base_handler import BaseHandler
from copy import deepcopy
from models import (TagFilter,
    Resource,
    ResourceDBCreate,
    ResourceDBRead,
    ResourceDB,
    ResourceFilter,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException
from . import ProjectHandler, TagHandler


class ResourceHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_resource(self, resource: Resource, detailed_output: bool = False) -> Resource:
        self.context.logger.debug(f"Creating resource: [{resource.uid}] for project: [{resource.project_uid}]")

        # Validate allowed create Resource
        await self.validate_can_create_resource(resource=resource)
        ph = ProjectHandler()
        th = TagHandler()

        with Session(self.context.database.engine) as session:
            create_obj = ResourceDBCreate.model_validate(resource)
            create_obj = ResourceDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = ResourceDBRead.model_validate(create_obj)
            resource = read_obj.return_data_obj()

            if detailed_output:
                resource.project = await ph.find_project(resource.project_uid)
                if resource.tag_uids:
                    resource.tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)

        self.context.logger.info(f"Created resource: [{resource.uid}]")
        return resource

    async def filter_resources(self, resource_filter: ResourceFilter, detailed_output: bool = False) -> list[Resource]:
        self.context.logger.debug(f"Filtering resources")

        ph = ProjectHandler()
        th = TagHandler()

        with Session(self.context.database.engine) as session:
            query = select(ResourceDB)
            query = resource_filter.apply_filters(ResourceDB, query)
            rows = session.exec(query).all()
            resources = []
            for row in rows:
                read_obj = ResourceDBRead.model_validate(row)
                resource = read_obj.return_data_obj()

                if detailed_output:
                    resource.project = await ph.find_project(resource.project_uid)
                    if resource.tag_uids:
                        resource.tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)

                resources.append(resource)
        self.context.logger.debug(f"Filter resources found [{len(resources)}]")
        return resources

    async def find_resource(self, resource_uid: str, detailed_output: bool = False) -> Resource:
        self.context.logger.debug(f"Find resource: [{resource_uid}]")

        ph = ProjectHandler()
        th = TagHandler()

        with Session(self.context.database.engine) as session:
            query = select(ResourceDB)
            query = query.where(ResourceDB.uid == resource_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No resource found with uid: {resource_uid}")
            read_obj = ResourceDBRead.model_validate(row)
            resource = read_obj.return_data_obj()

            if detailed_output:
                resource.project = await ph.find_project(resource.project_uid)
                if resource.tag_uids:
                    resource.tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)

        self.context.logger.debug(f"Created resource: [{resource.uid}]")
        return resource

    async def update_resource(self, resource_uid: str, resource: Resource, detailed_output: bool = False) -> Resource:
        self.context.logger.debug(f"Updating resource: [{resource_uid}]")

        # Validate allowed update Resource
        await self.validate_can_update_resource(resource_uid=resource_uid, resource=resource)
        ph = ProjectHandler()
        th = TagHandler()

        with Session(self.context.database.engine) as session:
            query = select(ResourceDB)
            query = query.where(ResourceDB.uid == resource_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No resource found with uid: {resource_uid}")

            # Verify data integrity
            immutable_fields = [
                'uid',
                'creation_datetime'
            ]
            immutable_modification_detected = []
            for key in immutable_fields:
                if getattr(row, key) != getattr(resource, key):
                    immutable_modification_detected.append(key)
            if len(immutable_modification_detected) > 0:
                raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

            change_log = deepcopy(row.change_log)

            # Track changes
            changes = []
            for key in Resource.__fields__.keys():
                try:
                    if getattr(row, key) != getattr(resource, key):
                        changes.append(key)
                        setattr(row, key, getattr(resource, key))
                except AttributeError:
                    pass

            change_log_strs = []
            for change in changes:
                change_log_str = f"{change}: {getattr(row, change)} -> {getattr(resource, change)}"
                change_log_strs.append(change_log_str)
            change_log[datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")] = ';'.join(change_log_strs)
            row.change_log = change_log

            row.update_datetime = datetime.utcnow()
            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = ResourceDBRead.model_validate(row)
            resource = read_obj.return_data_obj()

            if detailed_output:
                resource.project = await ph.find_project(resource.project_uid)
                if resource.tag_uids:
                    resource.tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)

        self.context.logger.info(f"Updated resource: [{resource.uid}]")
        return resource

    async def set_activation(self, resource_uid: str, active_state: bool) -> Resource:
        self.context.logger.debug(f"Setting resource activation: [{resource_uid}] to [{active_state}]")

        resource = await self.find_resource(resource_uid=resource_uid)
        resource.active = active_state
        resource.cascade_active = active_state

        resource = await self.update_resource(resource_uid=resource_uid, resource=resource)

        self.context.logger.info(f"Set resource activation: [{resource.uid}]")
        return resource

    async def delete_resource(self, resource_uid: str) -> Resource:
        self.context.logger.debug(f"Deleting Resource: [{resource_uid}]")

        resource = await self.find_resource(resource_uid=resource_uid)
        resource.deleted = True
        resource.cascade_deleted = True

        resource = await self.update_resource(resource_uid=resource_uid, resource=resource)

        self.context.logger.info(f"Resource deleted: [{resource.uid}]")
        return resource


    async def validate_can_create_resource(self, resource: Resource) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=resource.project_uid)
        if resource.project_uid != project.uid:
            raise DataIntegrityException("Resource project_uid does not match project_uid")
        # Validate Tags
        th = TagHandler()
        if resource.tag_uids:
            tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)
            if len(tags) != len(resource.tag_uids):
                raise DataIntegrityException("Resource tag_uids do not match tags")
        resource.project = project
        resource_filter = ResourceFilter(
            project_uid=[resource.project.uid],
            name=[resource.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ResourceDB)
            query = resource_filter.apply_filters(ResourceDB, query)
            rows = session.exec(query).all()
            if rows:
                raise DuplicateRecordsException(f"Resource with name [{resource.name}] already exists")

    async def validate_can_update_resource(self, resource_uid: str, resource: Resource) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=resource.project_uid)
        if resource.project_uid != project.uid:
            raise DataIntegrityException("Resource project_uid does not match project_uid")
        # Validate Tags
        th = TagHandler()
        if resource.tag_uids:
            tags = await th.filter_tags(TagFilter(uid=resource.tag_uids), detailed_output=detailed_output)
            if len(tags) != len(resource.tag_uids):
                raise DataIntegrityException("Resource tag_uids do not match tags")
        resource.project = project
        resource_filter = ResourceFilter(
            name=[resource.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(ResourceDB)
            query = resource_filter.apply_filters(ResourceDB, query)
            rows = session.exec(query).all()
            """
            if rows == 0 there are no records with the name and you can update
            if rows == 1 and the uuids match its fine
            if rows == 1 and the uuids do not match error
            if rows > 1 error
            """
            if len(rows) == 1:
                if rows[0].uid != resource_uid:
                    raise DuplicateRecordsException(f"Resource with name [{resource.name}] already exists")
            elif len(rows) > 1:
                raise DuplicateRecordsException(f"Resource with name [{resource.name}] already exists")
