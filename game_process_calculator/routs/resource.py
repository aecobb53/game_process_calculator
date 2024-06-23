from fastapi import APIRouter, HTTPException, Request, Response, Depends

from models import Resource, ResourceFilter
from handlers import ResourceHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/resource',
    tags=['resource'],
)


@router.post('/', status_code=201)
async def create_resource(resource: Resource):
    rh = ResourceHandler()
    try:
        created_resource = await rh.create_resource(resource=resource)
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
    return created_resource


@router.get('/', status_code=200)
async def filter_resource(request: Request):
    rh = ResourceHandler()
    try:
        resource_filter = parse_query_params(request=request, query_class=ResourceFilter)
        resources = await rh.filter_resources(resource_filter=resource_filter)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return {'resources': resources}


@router.put('/{resource_id}', status_code=200)
async def update_resource(resource_id: str, resource: Resource):
    rh = ResourceHandler()
    try:
        updated_resource = await rh.update_resource(resource_uid=resource_id, resource=resource)
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
    return updated_resource


@router.get('/{resource_id}', status_code=200)
async def find_resource(resource_id: str):
    rh = ResourceHandler()
    try:
        resource = await rh.find_resource(resource_uid=resource_id)
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
    return resource


@router.put('/{resource_id}/activate', status_code=200)
async def activate_resource(resource_id: str):
    rh = ResourceHandler()
    try:
        updated_resource = await rh.set_activation(resource_uid=resource_id, active_state=True)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_resource


@router.put('/{resource_id}/deactivate', status_code=200)
async def deactivate_resource(resource_id: str):
    rh = ResourceHandler()
    try:
        updated_resource = await rh.set_activation(resource_uid=resource_id, active_state=False)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_resource


@router.delete('/{resource_id}', status_code=200)
async def delete_resource(resource_id: str):
    rh = ResourceHandler()
    try:
        updated_resource = await rh.delete_resource(resource_uid=resource_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_resource
