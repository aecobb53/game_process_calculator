from fastapi import APIRouter, HTTPException, Request, Response, Depends

from models import Tag, TagFilter
from handlers import TagHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

context = ContextSingleton()

router = APIRouter(
    prefix='/tag',
    tags=['tag'],
)


@router.post('/', status_code=201)
async def create_tag(tag: Tag):
    th = TagHandler()
    try:
        created_tag = await th.create_tag(tag=tag)
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return created_tag


@router.get('/', status_code=200)
async def filter_tag(request: Request):
    th = TagHandler()
    try:
        tag_filter = parse_query_params(request=request, query_class=TagFilter)
        tags = await th.filter_tags(tag_filter=tag_filter)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return {'tags': tags}


@router.get('/{tag_id}', status_code=200)
async def find_tag(tag_id: str):
    th = TagHandler()
    try:
        tag = await th.find_tag(tag_uid=tag_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except DuplicateRecordsException as err:
        message = f"Duplicate records found: [{err}]"
        context.logger.error(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return tag


@router.put('/{tag_id}/activate', status_code=200)
async def activate_tag(tag_id: str):
    th = TagHandler()
    try:
        updated_tag = await th.set_activation(tag_uid=tag_id, active_state=True)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_tag


@router.put('/{tag_id}/deactivate', status_code=200)
async def deactivate_tag(tag_id: str):
    th = TagHandler()
    try:
        updated_tag = await th.set_activation(tag_uid=tag_id, active_state=False)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_tag


@router.delete('/{tag_id}', status_code=200)
async def delete_tag(tag_id: str):
    th = TagHandler()
    try:
        updated_tag = await th.delete_tag(tag_uid=tag_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_tag
