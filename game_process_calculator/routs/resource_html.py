from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

from handlers import ProjectHandler
from utils import MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from html import (
    # create_resource_html_page,
    filter_resources_html_page,
    # find_resource_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/resource',
    tags=['resource', 'html'],
)


@router.get('/')
async def html_resource(request: Request):
    resource_page = filter_resources_html_page()
    return HTMLResponse(content=resource_page, status_code=200)


@router.get('/modify')
async def html_modify_resource(request: Request):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)


@router.get('/{resource_uid}')
async def html_resource_resource_uid(request: Request, resource_uid: str):
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=501)
