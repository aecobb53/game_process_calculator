from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

from handlers import ProjectHandler
from utils import MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from html import (
    # create_workflow_html_page,
    # filter_workflows_html_page,
    # find_workflow_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/workflow',
    tags=['workflow', 'html'],
)


@router.get('/')
async def html_workflow(request: Request):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)


@router.get('/modify')
async def html_modify_workflow(request: Request):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)


@router.get('/{workflow_uid}')
async def html_workflow_workflow_uid(request: Request, workflow_uid: str):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)
