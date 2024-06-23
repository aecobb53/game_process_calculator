from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

from handlers import ProjectHandler
from utils import MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from html import (
    create_project_html_page,
    filter_projects_html_page,
    find_project_html_page,
    # project_base_page,
    # unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/project',
    tags=['project', 'html'],
)


@router.get('/')
async def html_project(request: Request):
    project_page = filter_projects_html_page()
    return HTMLResponse(content=project_page, status_code=200)


@router.get('/modify')
async def html_modify_project(request: Request):
    project_page = create_project_html_page()
    return HTMLResponse(content=project_page, status_code=200)


@router.get('/{project_uid}')
async def html_project_project_uid(request: Request, project_uid: str):
    ph = ProjectHandler()
    try:
        project = await ph.find_project(project_uid=project_uid)
    except MissingRecordException as err:
        context.logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        context.logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        context.logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    project_page = find_project_html_page(project=project)
    return HTMLResponse(content=project_page, status_code=200)
