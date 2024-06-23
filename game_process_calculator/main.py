import os
import json

from fastapi import FastAPI, Query, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from models import RestHeaders, ResponseTypes
from handlers import DatabaseHandler
from app_files import ContextSingleton, init_logger
from html import (project_base_page)
# from html import (WorkflowDisplay,
#     create_project_html_page,
#     filter_projects_html_page,
#     filter_resources_html_page,
#     find_project_html_page,
#     project_base_page,
#     unimplemented_page)

from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from phtml import Header, Style

from routs import (project_router,
    tag_router,
    resource_router,
    process_router,
    workflow_router,
    project_html_router,
    resource_html_router,
    process_html_router,
    workflow_html_router,)

# Service Info
with open(os.path.join(os.path.dirname(os.getcwd()), 'info.json'), 'r') as jf:
    app_info = json.load(jf)

app = FastAPI(
    title=app_info['service_name'],
    description=app_info['description'],
    version=app_info['version'],
)

# Setting up CORS and who can access the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(tag_router)
app.include_router(resource_router)
app.include_router(process_router)
app.include_router(workflow_router)
app.include_router(project_html_router)
app.include_router(resource_html_router)
app.include_router(process_html_router)
app.include_router(workflow_html_router)


@app.on_event("startup")
async def startup_event():
    db = DatabaseHandler()
    db.create_tables()
    context = ContextSingleton()
    context.database = db
    context.logger = init_logger()


# Root
@app.get('/', status_code=200)
async def root(request: Request):
    # context.logger.debug('GET on /')
    # context.logger.debug(f"REQUEST STUFF")
    header_details = RestHeaders(request=request)
    if header_details.response_type == ResponseTypes.HTML:
        project_page = project_base_page()
        return HTMLResponse(content=project_page)
    elif header_details.response_type == ResponseTypes.JSON:
        return {'Hello': 'WORLD!'}
    return {'Hello': 'WORLD!'}


@app.get('/service-info', status_code=200)
async def service_info(request: Request):
    # logger.debug('GET on /service-info')
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info.json')
    header_details = RestHeaders(request=request)
    with open(file_path, 'r') as f:
        service_info = json.load(f)
    if header_details.response_type == ResponseTypes.HTML:
        navigation_content = NavigationContent(webpage_name="Game Process Calculator")
        body_content = BodyContent(body_content=[service_info])
        footer_content = FooterContent(
            footer_content=[Header(level=3, internal='Game Process Calculator').add_style(
                Style(style_details={'margin': '0', 'padding': '0'}))],)
        new_formated_doc = MyBaseDocument(
            navigation_content=navigation_content,
            body_content=body_content,
            footer_content=footer_content,
        )
        return HTMLResponse(content=new_formated_doc.return_document, status_code=200)
    elif header_details.response_type == ResponseTypes.JSON:
        return service_info
