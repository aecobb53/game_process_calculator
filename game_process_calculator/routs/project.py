from fastapi import APIRouter, HTTPException, Request, Response, Depends

from models import Project, ProjectFilter
from handlers import ProjectHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from typing import Annotated

context = ContextSingleton()

router = APIRouter(
    prefix='/project',
    tags=['project'],
)


@router.post('/', status_code=201)
async def create_project(project: Project):
    ph = ProjectHandler()
    try:
        created_project = await ph.create_project(project=project)
    except DuplicateRecordsException as err:
        message = f"Dupe record attempt: {err}"
        context.logger.warning(message)
        raise HTTPException(status_code=409, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return created_project


@router.get('/', status_code=200)
async def filter_project(request: Request):
    ph = ProjectHandler()
    try:
        project_filter = parse_query_params(request=request, query_class=ProjectFilter)
        projects = await ph.filter_projects(project_filter=project_filter)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=409, detail='Internal Service Error')
    return {'projects': projects}


@router.put('/{project_id}', status_code=200)
async def update_project(project_id: str, project: Project):
    ph = ProjectHandler()
    try:
        updated_project = await ph.update_project(project_uid=project_id, project=project)
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
    return updated_project

@router.get('/{project_id}', status_code=200)
async def find_project(project_id: str):
    ph = ProjectHandler()
    try:
        project = await ph.find_project(project_uid=project_id)
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
    return project


@router.put('/{project_id}/activate', status_code=200)
async def activate_project(project_id: str):
    ph = ProjectHandler()
    try:
        updated_project = await ph.set_activation(project_uid=project_id, active_state=True)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_project


@router.put('/{project_id}/deactivate', status_code=200)
async def deactivate_project(project_id: str):
    ph = ProjectHandler()
    try:
        updated_project = await ph.set_activation(project_uid=project_id, active_state=False)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_project


@router.delete('/{project_id}', status_code=200)
async def delete_project(project_id: str):
    ph = ProjectHandler()
    try:
        updated_project = await ph.delete_project(project_uid=project_id)
    except MissingRecordException as err:
        message = f"Record not found: [{err}]"
        context.logger.warning(message)
        raise HTTPException(status_code=404, detail=message)
    except Exception as err:
        context.logger.warning(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Service Error')
    return updated_project
