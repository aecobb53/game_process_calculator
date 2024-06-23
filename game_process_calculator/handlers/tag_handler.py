from sqlmodel import Session, select

from .base_handler import BaseHandler
from models import (Tag,
    TagDBCreate,
    TagDBRead,
    TagDB,
    TagFilter,)
from utils import DuplicateRecordsException, MissingRecordException, DataIntegrityException
from . import ProjectHandler


class TagHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_tag(self, tag: Tag) -> Tag:
        self.context.logger.debug(f"Creating tag: [{tag.uid}] for project: [{tag.project_uid}]")

        # Validate allowed create Tag
        await self.validate_can_create_tag(tag=tag)
        ph = ProjectHandler()

        with Session(self.context.database.engine) as session:
            create_obj = TagDBCreate.model_validate(tag)
            create_obj = TagDB.model_validate(create_obj)
            session.add(create_obj)
            session.commit()
            session.refresh(create_obj)
            read_obj = TagDBRead.model_validate(create_obj)
            tag = read_obj.return_data_obj()

            tag.project = await ph.find_project(tag.project_uid)

        self.context.logger.info(f"Created tag: [{tag.uid}]")
        return tag

    async def filter_tags(self, tag_filter: TagFilter) -> list[Tag]:
        self.context.logger.debug(f"Filtering tags")

        ph = ProjectHandler()

        print(f"TAG FILTEr")
        print(tag_filter.dict())

        with Session(self.context.database.engine) as session:
            query = select(TagDB)
            query = tag_filter.apply_filters(TagDB, query)
            rows = session.exec(query).all()
            tags = []
            for row in rows:
                read_obj = TagDBRead.model_validate(row)
                tag = read_obj.return_data_obj()

                tag.project = await ph.find_project(tag.project_uid)

                tags.append(tag)
        self.context.logger.debug(f"Filter tags found [{len(tags)}]")
        return tags

    async def find_tag(self, tag_uid: str) -> Tag:
        self.context.logger.debug(f"Find tag: [{tag_uid}]")

        ph = ProjectHandler()

        with Session(self.context.database.engine) as session:
            query = select(TagDB)
            query = query.where(TagDB.uid == tag_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No tag found with uid: {tag_uid}")
            read_obj = TagDBRead.model_validate(row)
            tag = read_obj.return_data_obj()

            tag.project = await ph.find_project(tag.project_uid)

        self.context.logger.debug(f"Tag found: [{tag.uid}]")
        return tag

    async def update_tag(self, tag_uid: str, tag: Tag) -> Tag:
        self.context.logger.debug(f"Updating tag: [{tag_uid}]")

        # Validate allowed update Tag
        await self.validate_can_update_tag(tag_uid=tag_uid, tag=tag)
        ph = ProjectHandler()

        with Session(self.context.database.engine) as session:
            query = select(TagDB)
            query = query.where(TagDB.uid == tag_uid)
            row = session.exec(query).first()
            if row is None:
                raise MissingRecordException(f"No tag found with uid: {tag_uid}")

            # Verify data integrity
            immutable_fields = [
                'uid',
                'creation_datetime'
            ]
            immutable_modification_detected = []
            for key in immutable_fields:
                if getattr(row, key) != getattr(tag, key):
                    immutable_modification_detected.append(key)
            if len(immutable_modification_detected) > 0:
                raise DataIntegrityException(f"Immutable fields were modified: {immutable_modification_detected}")

            for key in Tag.__fields__.keys():
                try:
                    if getattr(row, key) != getattr(tag, key):
                        setattr(row, key, getattr(tag, key))
                except AttributeError:
                    pass

            session.add(row)
            session.commit()
            session.refresh(row)
            read_obj = TagDBRead.model_validate(row)
            tag = read_obj.return_data_obj()

            tag.project = await ph.find_project(tag.project_uid)

        self.context.logger.info(f"Updated tag: [{tag.uid}]")
        return tag

    async def set_activation(self, tag_uid: str, active_state: bool) -> Tag:
        self.context.logger.debug(f"Setting tag activation: [{tag_uid}] to [{active_state}]")

        tag = await self.find_tag(tag_uid=tag_uid)
        tag.active = active_state
        tag.cascade_active = active_state

        await self.update_tag(tag_uid=tag_uid, tag=tag)

        self.context.logger.info(f"Set tag activation: [{tag.uid}]")
        return tag

    async def delete_tag(self, tag_uid: str) -> Tag:
        self.context.logger.debug(f"Deleting Tag: [{tag_uid}]")

        tag = await self.find_tag(tag_uid=tag_uid)
        tag.deleted = True
        tag.cascade_deleted = True

        await self.update_tag(tag_uid=tag_uid, tag=tag)

        self.context.logger.info(f"Tag deleted: [{tag.uid}]")
        return tag


    async def validate_can_create_tag(self, tag: Tag) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=tag.project_uid)
        if tag.project_uid != project.uid:
            raise DataIntegrityException("Tag project_uid does not match project_uid")
        tag.project = project
        tag_filter = TagFilter(
            project_uid=[tag.project.uid],
            name=[tag.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(TagDB)
            query = tag_filter.apply_filters(TagDB, query)
            rows = session.exec(query).all()
            if rows:
                raise DuplicateRecordsException(f"Tag with name [{tag.name}] already exists")

    async def validate_can_update_tag(self, tag_uid: str, tag: Tag) -> None:
        # Validate project
        ph = ProjectHandler()
        project = await ph.find_project(project_uid=tag.project_uid)
        if tag.project_uid != project.uid:
            raise DataIntegrityException("Tag project_uid does not match project_uid")
        tag.project = project
        tag_filter = TagFilter(
            name=[tag.name],
            active=True,
            deleted=False,
            cascade_active=True,
            cascade_deleted=False
        )
        with Session(self.context.database.engine) as session:
            query = select(TagDB)
            query = tag_filter.apply_filters(TagDB, query)
            rows = session.exec(query).all()
            """
            if rows == 0 there are no records with the name and you can update
            if rows == 1 and the uuids match its fine
            if rows == 1 and the uuids do not match error
            if rows > 1 error
            """
            if len(rows) == 1:
                if rows[0].uid != tag_uid:
                    raise DuplicateRecordsException(f"Tag with name [{tag.name}] already exists")
            elif len(rows) > 1:
                raise DuplicateRecordsException(f"Tag with name [{tag.name}] already exists")
