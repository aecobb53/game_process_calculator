from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

from handlers import ProjectHandler
from utils import MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from html import (
    # create_process_html_page,
    # filter_processes_html_page,
    # find_process_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/process',
    tags=['process', 'html'],
)


@router.get('/')
async def html_process(request: Request):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)


@router.get('/modify')
async def html_modify_process(request: Request):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)


@router.get('/{process_uid}')
async def html_process_process_uid(request: Request, process_uid: str):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)
