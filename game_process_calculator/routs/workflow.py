from fastapi import APIRouter, HTTPException, Request, Response, Depends

from models import Workflow, WorkflowFilter
from handlers import WorkflowHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/workflow',
    tags=['workflow'],
)


@router.post('/', status_code=201)
async def create_workflow(workflow: Workflow):
    wh = WorkflowHandler()
    try:
        created_workflow = await wh.create_workflow(workflow=workflow)
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
    return created_workflow


@router.get('/', status_code=200)
async def filter_workflow(request: Request):
    wh = WorkflowHandler()
    try:
        workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
        workflows = await wh.filter_workflows(workflow_filter=workflow_filter)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return {'workflows': workflows}


@router.put('/{workflow_id}', status_code=200)
async def update_workflow(workflow_id: str, workflow: Workflow):
    wh = WorkflowHandler()
    try:
        updated_workflow = await wh.update_workflow(workflow_uid=workflow_id, workflow=workflow)
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
    return updated_workflow


@router.get('/{workflow_id}', status_code=200)
async def find_workflow(workflow_id: str):
    wh = WorkflowHandler()
    try:
        workflow = await wh.find_workflow(workflow_uid=workflow_id)
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
    return workflow


@router.put('/{workflow_id}/activate', status_code=200)
async def activate_workflow(workflow_id: str):
    wh = WorkflowHandler()
    try:
        updated_workflow = await wh.set_activation(workflow_uid=workflow_id, active_state=True)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_workflow


@router.put('/{workflow_id}/deactivate', status_code=200)
async def deactivate_workflow(workflow_id: str):
    wh = WorkflowHandler()
    try:
        updated_workflow = await wh.set_activation(workflow_uid=workflow_id, active_state=False)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_workflow


@router.delete('/{workflow_id}', status_code=200)
async def delete_workflow(workflow_id: str):
    wh = WorkflowHandler()
    try:
        updated_workflow = await wh.delete_workflow(workflow_uid=workflow_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_workflow
