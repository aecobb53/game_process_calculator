from fastapi import APIRouter, HTTPException, Request, Response, Depends

from models import Process, ProcessFilter
from handlers import ProcessHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/process',
    tags=['process'],
)


@router.post('/', status_code=201)
async def create_process(process: Process):
    prh = ProcessHandler()
    try:
        created_process = await prh.create_process(process=process)
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
    return created_process


@router.get('/', status_code=200)
async def filter_process(request: Request):
    prh = ProcessHandler()
    try:
        process_filter = parse_query_params(request=request, query_class=ProcessFilter)
        processes = await prh.filter_processes(process_filter=process_filter)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return {'processes': processes}


@router.put('/{process_id}', status_code=200)
async def update_process(process_id: str, process: Process):
    prh = ProcessHandler()
    try:
        updated_process = await prh.update_process(process_uid=process_id, process=process)
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
    return updated_process


@router.get('/{process_id}', status_code=200)
async def find_process(process_id: str):
    prh = ProcessHandler()
    try:
        process = await prh.find_process(process_uid=process_id)
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
    return process


@router.put('/{process_id}/activate', status_code=200)
async def activate_process(process_id: str):
    prh = ProcessHandler()
    try:
        updated_process = await prh.set_activation(process_uid=process_id, active_state=True)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_process


@router.put('/{process_id}/deactivate', status_code=200)
async def deactivate_process(process_id: str):
    prh = ProcessHandler()
    try:
        updated_process = await prh.set_activation(process_uid=process_id, active_state=False)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_process


@router.delete('/{process_id}', status_code=200)
async def delete_process(process_id: str):
    prh = ProcessHandler()
    try:
        updated_process = await prh.delete_process(process_uid=process_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_process
