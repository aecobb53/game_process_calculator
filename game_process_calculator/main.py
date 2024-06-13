from glob import glob
import json
import os
import logging

from logging.handlers import RotatingFileHandler
from logging import FileHandler , StreamHandler
import re
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional, Union

from models import (
    Project,
    ProjectFilter,
    Process,
    ProcessFilter,
    Resource,
    ResourceFilter,
    Workflow,
    WorkflowFilter,
    ProcessType,
    BalanceWorkflowArgs,
    RestHeaders,
    ResponseTypes)
from handlers import ProjectHandler, ResourceHandler, ProcessHandler, WorkflowHandler, DataHandler
from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from html import WorkflowDisplay, create_project_html_page, filter_projects_html_page, filter_resources_html_page, find_project_html_page, project_base_page, unimplemented_page


from my_base_html_lib import MyBaseDocument, NavigationContent, SidebarContent, BodyContent, FooterContent
from phtml import Style, Header


appname = 'game_process_calculator'

# Logging
try:
    os.makedirs('logs')
except:
    pass
log_file = f"logs/{appname}.log"
logger = logging.getLogger('legba')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s - %(message)s', '%Y-%m-%dT%H:%M:%SZ')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
# if os.environ.get('STREAM_HANDLER', 'False') == 'True':
if os.environ.get('STREAM_HANDLER', 'True') == 'True':
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

app = FastAPI()
# context = ContextSingleton()
# context.add_logger(logger)
# Setting up CORS and who can access the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event('startup')
# async def update_context():
#     print('IN STARTUP')
#     context.add_logger(logger)
#     # context.config = {}

# Root
@app.get('/', status_code=200)
async def root(request: Request):
    logger.debug('GET on /')
    logger.debug(f"REQUEST STUFF")
    header_details = RestHeaders(request=request)
    if header_details.response_type == ResponseTypes.HTML:
        project_page = project_base_page()
        return HTMLResponse(content=project_page)
    elif header_details.response_type == ResponseTypes.JSON:
        return {'Hello': 'WORLD!'}
    return {'Hello': 'WORLD!'}

@app.get('/testing-rest', status_code=200)
async def testing_rest(request: Request):
    logger.debug('GET on /testing-rest')
    resp = {}
    try:
        logger.debug(f"HEADER")
        logger.debug(f"{request.headers}")
        resp['headers'] = request.headers
    except:
        pass
    try:
        logger.debug(f"QUERY PARAMS")
        logger.debug(f"{request.query_params}")
        resp['query_params'] = request.query_params
    except:
        pass
    try:
        logger.debug(f"BODY")
        body = await request.body()
        logger.debug(f"{body}")
        resp['body'] = body
    except:
        pass
    return resp
    # return {'Hello': 'WORLD!'}

@app.get('/service-info', status_code=200)
async def service_info(request: Request):
    logger.debug('GET on /service-info')
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

# DEV CLEAR DATA
@app.post('/clear-test-data')
async def root(request: Request):
    logger.debug('POST on /clear-test-data')
    if str(os.environ['TESTING']) == '1':
        logger.debug('CLEARING DATA')
        project_handler = ProjectHandler()
        for fl in os.listdir(project_handler.save_dir):
            os.remove(os.path.join(project_handler.save_dir, fl))
        logger.debug('DATA CLEARED')
        return {'data_clearing': 'True'}

# Create Endpoints
@app.post('/projects', status_code=201)
async def create_project(project: Project):
    logger.debug('POST on /projects')
    data_handler = DataHandler()
    try:
        new_project = data_handler.create_project(project)
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe record attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_project.put()

@app.post('/resources', status_code=201)
async def create_resource(resource: Resource):
    logger.debug('POST on /resources')
    data_handler = DataHandler()
    try:
        new_resource = data_handler.create_resource(resource)
    except MissingRecordException as err:
        logger.debug(f"Missing record attempt: {err}")
        raise HTTPException(status_code=400, detail=str(err))
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe record attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_resource.put()

@app.post('/processes', status_code=201)
async def create_process(process: Process):
    logger.debug('POST on /processes')
    data_handler = DataHandler()
    try:
        new_process = data_handler.create_process(process)
    except MissingRecordException as err:
        logger.debug(f"Missing process attempt: {err}")
        raise HTTPException(status_code=400, detail=str(err))
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe process attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_process.put()

@app.post('/workflows', status_code=201)
async def create_workflow(workflow: Workflow):
    logger.debug('POST on /workflows')
    data_handler = DataHandler()
    try:
        new_workflow = data_handler.create_workflow(workflow)
    except MissingRecordException as err:
        logger.debug(f"Missing workflow attempt: {err}")
        raise HTTPException(status_code=400, detail=str(err))
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe workflow attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return new_workflow.put()

# Filter Endpoints
@app.get('/projects', status_code=200)
async def filter_projects(request: Request):
    logger.debug('GET on /projects')
    try:
        project_filter = parse_query_params(request=request, query_class=ProjectFilter)
        data_handler = DataHandler()
        projects = data_handler.filter_projects(project_filter=project_filter)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'projects': [p.put() for p in projects]}

@app.get('/resources', status_code=200)
async def filter_resources(request: Request):
    logger.debug('GET on /resources')
    try:
        resource_filter = parse_query_params(request=request, query_class=ResourceFilter)
        data_handler = DataHandler()
        resources = data_handler.filter_resources(resource_filter=resource_filter)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'resources': [p.put() for p in resources]}

@app.get('/processes', status_code=200)
async def filter_processes(request: Request):
    logger.debug('GET on /processes')
    try:
        process_filter = parse_query_params(request=request, query_class=ProcessFilter)
        data_handler = DataHandler()
        processes = data_handler.filter_processes(process_filter=process_filter)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'processes': [p.put() for p in processes]}

@app.get('/workflows', status_code=200)
async def filter_workflows(request: Request):
    logger.debug('GET on /workflows')
    try:
        workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
        data_handler = DataHandler()
        workflows = data_handler.filter_workflows(workflow_filter=workflow_filter)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'workflows': [p.put() for p in workflows]}

# Find Specific Endpoints
@app.get('/project/{project_uid}')
async def find_specific_project(project_uid: str = None):
    logger.debug('GET on /project')
    logger.debug(f"Project uuid: {project_uid}")
    data_handler = DataHandler()
    try:
        project = data_handler.find_project(project_uid=project_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return project.put()

@app.get('/resource/{resource_uid}')
async def find_specific_resource(resource_uid: str = None):
    logger.debug('GET on /resource')
    logger.debug(f"Resource uuid: {resource_uid}")
    data_handler = DataHandler()
    try:
        resource = data_handler.find_resource(resource_uid=resource_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return resource.put()

@app.get('/process/{process_uid}')
async def find_specific_process(process_uid: str = None):
    logger.debug('GET on /process')
    logger.debug(f"Process uuid: {process_uid}")
    data_handler = DataHandler()
    try:
        process = data_handler.find_process(process_uid=process_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return process.put()

@app.get('/workflow/{workflow_uid}')
async def find_specific_workflow(workflow_uid: str = None):
    logger.debug('GET on /workflow')
    logger.debug(f"Resource uuid: {workflow_uid}")
    data_handler = DataHandler()
    try:
        workflow = data_handler.find_workflow(workflow_uid=workflow_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return workflow.put()

# Update Endpoints
@app.put('/project/{project_uuid}', status_code=200)
async def update_project(project_uuid: str, project: Project):
    logger.debug('PUT on /project')
    logger.debug(f"Project uuid: {project_uuid}")
    project.uid = project_uuid

    data_handler = DataHandler()
    try:
        updated_project = data_handler.update_project(project)
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe workflow attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Updated project: {updated_project}")
    return updated_project.put()

@app.put('/resource/{resource_uuid}', status_code=200)
async def update_resource(resource_uuid: str, resource: Resource):
    logger.debug('PUT on /resource')
    logger.debug(f"Resource uuid: {resource_uuid}")
    resource.uid = resource_uuid

    data_handler = DataHandler()
    try:
        updated_resource = data_handler.update_resource(resource)
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe workflow attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Updated resource: {updated_resource}")
    return updated_resource.put()

@app.put('/process/{process_uuid}', status_code=200)
async def update_process(process_uuid: str, process: Process):
    logger.debug('PUT on /process')
    logger.debug(f"Process uuid: {process_uuid}")
    process.uid = process_uuid

    data_handler = DataHandler()
    try:
        updated_process = data_handler.update_process(process)
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe workflow attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Updated process: {updated_process}")
    return updated_process.put()

@app.put('/workflow/{workflow_uuid}', status_code=200)
async def update_workflow(workflow_uuid: str, workflow: Workflow):
    logger.debug('PUT on /workflow')
    logger.debug(f"Workflow uuid: {workflow_uuid}")
    workflow.uid = workflow_uuid

    data_handler = DataHandler()
    try:
        updated_workflow = data_handler.update_workflow(workflow)
    except DuplicateRecordsException as err:
        logger.debug(f"Dupe workflow attempt: {err}")
        raise HTTPException(status_code=409, detail=str(err))
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Updated workflow: {updated_workflow}")
    return updated_workflow.put()

# Delete Endpoints
@app.delete('/project/{project_uid}', status_code=200)
async def delete_specific_project(project_uid: str = None):
    logger.debug('DELETE on /project')
    logger.debug(f"Project uuid: {project_uid}")
    data_handler = DataHandler()
    try:
        deleted_project = data_handler.delete_project(project_uid=project_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Deleted project: {deleted_project}")
    return deleted_project.put()

@app.delete('/resource/{resource_uid}', status_code=200)
async def delete_specific_resource(resource_uid: str = None):
    logger.debug('DELETE on /resource')
    logger.debug(f"Resource uuid: {resource_uid}")
    data_handler = DataHandler()
    try:
        deleted_resource = data_handler.delete_resource(resource_uid=resource_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Deleted resource: {deleted_resource}")
    return deleted_resource.put()

@app.delete('/process/{process_uid}', status_code=200)
async def delete_specific_process(process_uid: str = None):
    logger.debug('DELETE on /process')
    logger.debug(f"Process uuid: {process_uid}")
    data_handler = DataHandler()
    try:
        deleted_process = data_handler.delete_process(process_uid=process_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Deleted process: {deleted_process}")
    return deleted_process.put()

@app.delete('/workflow/{workflow_uid}', status_code=200)
async def delete_specific_workflow(workflow_uid: str = None):
    logger.debug('DELETE on /workflow')
    logger.debug(f"Resource uuid: {workflow_uid}")
    data_handler = DataHandler()
    try:
        deleted_workflow = data_handler.delete_workflow(workflow_uid=workflow_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    logger.debug(f"Deleted workflow: {deleted_workflow}")
    return deleted_workflow.put()

# Export Endpoints
# TODO: Allow for filtering in the exports to just export a project
@app.get('/export-projects', status_code=200)
async def export_projects(request: Request):
    logger.debug('GET on /export-projects')
    project_handler = ProjectHandler()
    try:
        content = project_handler.export_projects()
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return content

@app.get('/export-resources', status_code=200)
async def export_resources(request: Request):
    logger.debug('GET on /export-resources')
    resource_handler = ResourceHandler()
    try:
        content = resource_handler.export_resources()
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return content

@app.get('/export-processes', status_code=200)
async def export_processes(request: Request):
    logger.debug('GET on /export-processes')
    process_handler = ProcessHandler()
    try:
        content = process_handler.export_processes()
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return content

@app.get('/export-workflows', status_code=200)
async def export_workflows(request: Request):
    logger.debug('GET on /export-workflows')
    workflow_handler = WorkflowHandler()
    try:
        content = workflow_handler.export_workflows()
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return content

@app.get('/export-database', status_code=200)
async def export_database(request: Request):
    logger.debug('GET on /export-database')
    data_handler = DataHandler()
    try:
        content = data_handler.export_database()
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return content

# Import Endpoints
@app.post('/import-projects')
async def import_projects(request: Request):
    logger.debug('POST on /import-projects')
    imported_projects = await request.json()
    project_handler = ProjectHandler()
    try:
        projects = project_handler.import_projects(dct=imported_projects)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'projects': [p.put() for p in projects]}

@app.post('/import-resources')
async def import_resources(request: Request):
    logger.debug('POST on /import-resources')
    imported_resources = await request.json()
    resource_handler = ResourceHandler()
    try:
        resources = resource_handler.import_resources(dct=imported_resources)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'resources': [p.put() for p in resources]}

@app.post('/import-processes')
async def import_processes(request: Request):
    logger.debug('POST on /import-processes')
    imported_processes = await request.json()
    process_handler = ProcessHandler()
    try:
        processes = process_handler.import_processes(dct=imported_processes)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'processes': [p.put() for p in processes]}

@app.post('/import-workflows')
async def import_workflows(request: Request):
    logger.debug('POST on /import-workflows')
    imported_workflows = await request.json()
    workflow_handler = WorkflowHandler()
    try:
        workflows = workflow_handler.import_workflows(dct=imported_workflows)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'workflows': [p.put() for p in workflows]}

@app.post('/import-database')
async def database(request: Request):
    logger.debug('POST on /import-database')
    imported_data = await request.json()
    data_handler = DataHandler()
    try:
        data_handler.import_database(content=imported_data)
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    return {'status': 'SUCCESS'}

# Data Visualization Endpoints
@app.get('/visualize-workflows')
async def visualize_workflows(request: Request):
    logger.debug('GET on /visualize-workflows')
    workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
    data_handler = DataHandler()
    workflows = data_handler.filter_workflows(workflow_filter=workflow_filter)
    workflows_dict = data_handler.return_complex_workflow_object(workflows=workflows)
    return {'workflows': workflows_dict}

@app.get('/html/visualize-workflows')
async def visualize_workflow_html(request: Request):
    logger.debug('GET on /html/visualize-workflows')
    workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
    logger.debug(f'Workflow Filter: {workflow_filter}')
    balance_params = parse_query_params(request=request, query_class=BalanceWorkflowArgs)
    logger.debug(f'Balance Params: {balance_params}')
    data_handler = DataHandler()
    workflows = data_handler.filter_workflows(workflow_filter=workflow_filter)
    workflows_dict = data_handler.return_complex_workflow_object(
        workflows=workflows,
        balance_criteria=balance_params)
    workflow_doc = WorkflowDisplay(workflows_dict=workflows_dict)
    workflow_html = workflow_doc.display_workflow()
    with open(os.path.join('deleteme_html_files', 'workflow.html'), 'w') as f:
        f.write(workflow_html)
    return HTMLResponse(content=workflow_html, status_code=200)


@app.get('/html/projects')
async def html_projects(request: Request):
    logger.debug('GET on /html/projects')
    project_page = filter_projects_html_page()
    return HTMLResponse(content=project_page, status_code=200)

@app.get('/html/resources')
async def html_resources(request: Request):
    logger.debug('GET on /html/resources')
    resource_page = filter_resources_html_page()
    return HTMLResponse(content=resource_page, status_code=200)

@app.get('/html/project/{project_uid}')
async def html_projects(request: Request, project_uid: str):
    logger.debug(f'GET on /html/project/{project_uid}')
    data_handler = DataHandler()
    try:
        project = data_handler.find_project(project_uid=project_uid)
    except MissingRecordException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except DuplicateRecordsException as err:
        logger.error(f"ERROR: {err}")
        raise HTTPException(status_code=404, detail=str(err))
    except Exception as err:
        logger.error(f'ERROR: {err}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    project_page = find_project_html_page(project=project)
    return HTMLResponse(content=project_page, status_code=200)

@app.get('/html/modify-project')
async def modify_html_projects(request: Request):
    logger.debug(f'GET on /html/modify-project')
    project_page = create_project_html_page()
    return HTMLResponse(content=project_page, status_code=200)

@app.get('/html/processes')
async def modify_html_projects(request: Request):
    logger.debug(f'GET on /html/modify-project')
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=200)

@app.get('/html/workflows')
async def modify_html_projects(request: Request):
    logger.debug(f'GET on /html/modify-project')
    project_page = unimplemented_page()
    return HTMLResponse(content=project_page, status_code=200)


# filter_resources_html_page
# unimplemented_page
"""
HTML endpoints
/
    - Home page with links to other pages
/service-info
    - Short info about service
    - Include app versions?

(Create if no thing exists)
/update-project
/update-resource
/update-process
/update-workflow

/filter-projects
/filter-resources
/filter-processes
/filter-workflows

/visualize-project  (All associated thigns with links to each thing)
/visualize-resources
/visualize-processes
/visualize-workflows
"""


# OLD WORKING VERSION
# @app.get('/html/visualize-workflows')
# async def visualize_workflow_html(request: Request):
#     logger.debug('GET on /html/visualize-workflows')
#     workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
#     balance_params = parse_query_params(request=request, query_class=BalanceWorkflowArgs)
#     data_handler = DataHandler()
#     workflows = data_handler.filter_workflows(workflow_filter=workflow_filter)
#     workflows_dict = data_handler.return_complex_workflow_object(
#         workflows=workflows,
#         balance_criteria=balance_params)
#     workflow_doc = WorkflowDisplay(workflows_dict=workflows_dict)
#     workflow_html = workflow_doc.display_workflow()
#     with open(os.path.join('deleteme_html_files', 'workflow.html'), 'w') as f:
#         f.write(workflow_html)
#     return HTMLResponse(content=workflow_html, status_code=200)

# @app.get('/html/visualize-workflows/{workflow_uid}')
# async def visualize_workflow_html(workflow_uid: str = None):
#     logger.debug('GET on /html/visualize-workflows')
#     data_handler = DataHandler()
#     workflow = data_handler.find_workflow(workflow_uid=workflow_uid)
#     workflows_dict = data_handler.return_complex_workflow_object(workflows=workflows)
#     workflow_doc = WorkflowDisplay(workflows_dict=workflows_dict)
#     workflow_html = workflow_doc.display_workflow()
#     with open(os.path.join('deleteme_html_files', 'workflow.html'), 'w') as f:
#         f.write(workflow_html)
#     return HTMLResponse(content=workflow_html, status_code=200)