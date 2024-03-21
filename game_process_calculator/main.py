import json
import os
import logging

from logging.handlers import RotatingFileHandler
from logging import FileHandler , StreamHandler
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
    BalanceWorkflowArgs)
from handlers import ProjectHandler, ResourceHandler, ProcessHandler, WorkflowHandler, DataHandler
from utils import parse_query_params, MissingRecordException, DuplicateRecordsException
from html import WorkflowDisplay

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

# Setting up CORS and who can access the API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get('/')
async def root(requests: Request):
    logger.debug('GET on /')
    return {'Hello': 'WORLD!'}

# DEV CLEAR DATA
@app.post('/clear-test-data')
async def root(requests: Request):
    logger.debug('POST on /clear-test-data')
    if str(os.environ['TESTING']) == '1':
        logger.debug('CLEARING DATA')
        project_handler = ProjectHandler()
        for fl in os.listdir(project_handler.save_dir):
            os.remove(os.path.join(project_handler.save_dir, fl))
        logger.debug('DATA CLEARED')
        return {'data_clearing': 'True'}

# Create Endpoints
@app.post('/projects')
async def create_project(project: Project):
    logger.debug('POST on /projects')
    data_handler = DataHandler()
    new_project = data_handler.create_project(project)
    return new_project.put()

@app.post('/resources')
async def create_resource(resource: Resource):
    logger.debug('POST on /resources')
    data_handler = DataHandler()
    new_resource = data_handler.create_resource(resource)
    return new_resource.put()

@app.post('/processes')
async def create_process(process: Process):
    logger.debug('POST on /processes')
    data_handler = DataHandler()
    new_process = data_handler.create_process(process)
    return new_process.put()

@app.post('/workflows')
async def create_workflow(workflow: Workflow):
    logger.debug('POST on /workflows')
    data_handler = DataHandler()
    new_workflow = data_handler.create_workflow(workflow)
    return new_workflow.put()

# Filter Endpoints
@app.get('/projects')
async def filter_projects(request: Request):
    logger.debug('GET on /projects')
    project_filter = parse_query_params(request=request, query_class=ProjectFilter)
    data_handler = DataHandler()
    projects = data_handler.filter_projects(project_filter=project_filter)
    return {'projects': [p.put() for p in projects]}

@app.get('/resources')
async def filter_resources(request: Request):
    logger.debug('GET on /resources')
    resource_filter = parse_query_params(request=request, query_class=ResourceFilter)
    data_handler = DataHandler()
    resources = data_handler.filter_resources(resource_filter=resource_filter)
    return {'resources': [p.put() for p in resources]}

@app.get('/processes')
async def filter_processes(request: Request):
    logger.debug('GET on /processes')
    process_filter = parse_query_params(request=request, query_class=ProcessFilter)
    data_handler = DataHandler()
    processes = data_handler.filter_processes(process_filter=process_filter)
    return {'processes': [p.put() for p in processes]}

@app.get('/workflows')
async def filter_workflows(request: Request):
    logger.debug('GET on /workflows')
    workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
    data_handler = DataHandler()
    workflows = data_handler.filter_workflows(workflow_filter=workflow_filter)
    return {'workflows': [p.put() for p in workflows]}

# Find Specific Endpoints
@app.get('/project/{project_uid}')
async def find_specific_project(project_uid: str = None):
    logger.debug('GET on /project')
    logger.debug(f"Project uuid: {project_uid}")
    data_handler = DataHandler()
    projects = data_handler.filter_projects(project_filter=ProjectFilter(uid=[project_uid]))

    if len(projects) == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    elif len(projects) == 1:
        return projects[0].put()
    else:
        raise HTTPException(status_code=404, detail="Multiple projects found")

@app.get('/resource/{resource_uid}')
async def find_specific_resource(resource_uid: str = None):
    logger.debug('GET on /resource')
    logger.debug(f"Resource uuid: {resource_uid}")
    data_handler = DataHandler()
    resources = data_handler.filter_resources(resource_filter=ResourceFilter(uid=[resource_uid]))

    if len(resources) == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    elif len(resources) == 1:
        return resources[0].put()
    else:
        raise HTTPException(status_code=404, detail="Multiple resources found")

@app.get('/process/{process_uid}')
async def find_specific_process(process_uid: str = None):
    logger.debug('GET on /process')
    logger.debug(f"Process uuid: {process_uid}")
    data_handler = DataHandler()
    processes = data_handler.filter_processes(process_filter=ProcessFilter(uid=[process_uid]))

    if len(processes) == 0:
        raise HTTPException(status_code=404, detail="Process not found")
    elif len(processes) == 1:
        return processes[0].put()
    else:
        raise HTTPException(status_code=404, detail="Multiple resources found")

@app.get('/workflow/{workflow_uid}')
async def find_specific_workflow(workflow_uid: str = None):
    logger.debug('GET on /workflow')
    logger.debug(f"Resource uuid: {workflow_uid}")
    data_handler = DataHandler()
    workflows = data_handler.filter_workflows(workflow_filter=WorkflowFilter(uid=[workflow_uid]))

    if len(workflows) == 0:
        raise HTTPException(status_code=404, detail="Workflow not found")
    elif len(workflows) == 1:
        return workflows[0].put()
    else:
        raise HTTPException(status_code=404, detail="Multiple workflows found")


# Update Endpoints
@app.put('/project/{project_uuid}')
async def update_project(project_uuid: str, project: Project):
    logger.debug('PUT on /project')
    logger.debug(f"Project uuid: {project_uuid}")
    logger.debug(project)
    project.uid = project_uuid

    data_handler = DataHandler()
    updated_project = data_handler.update_project(project)
    logger.debug(f"Updated project: {updated_project}")
    return updated_project.put()

@app.put('/resource/{resource_uuid}')
async def update_resource(resource_uuid: str, resource: Resource):
    logger.debug('PUT on /resource')
    logger.debug(f"Resource uuid: {resource_uuid}")
    logger.debug(resource)
    resource.uid = resource_uuid

    data_handler = DataHandler()
    updated_resource = data_handler.update_resource(resource)
    logger.debug(f"Updated resource: {updated_resource}")
    return updated_resource.put()

@app.put('/process/{process_uuid}')
async def update_process(process_uuid: str, process: Process):
    logger.debug('PUT on /process')
    logger.debug(f"Process uuid: {process_uuid}")
    logger.debug(process)
    process.uid = process_uuid

    data_handler = DataHandler()
    updated_process = data_handler.update_process(process)
    logger.debug(f"Updated process: {updated_process}")
    return updated_process.put()

@app.put('/workflow/{workflow_uuid}')
async def update_workflow(workflow_uuid: str, workflow: Workflow):
    logger.debug('PUT on /workflow')
    logger.debug(f"Workflow uuid: {workflow_uuid}")
    logger.debug(workflow)
    workflow.uid = workflow_uuid

    data_handler = DataHandler()
    updated_workflow = data_handler.update_workflow(workflow)
    logger.debug(f"Updated workflow: {updated_workflow}")
    return updated_workflow.put()

# Delete Endpoints
@app.delete('/project/{project_uid}')
async def delete_specific_project(project_uid: str = None):
    logger.debug('DELETE on /project')
    logger.debug(f"Project uuid: {project_uid}")
    data_handler = DataHandler()
    project_handler = ProjectHandler()
    try:
        updated_project = project_handler.delete(project_uid=project_uid)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple projects found")
    logger.debug(f"Deleted project: {updated_project}")
    return updated_project.put()

@app.delete('/resource/{resource_uid}')
async def delete_specific_resource(resource_uid: str = None):
    logger.debug('DELETE on /resource')
    logger.debug(f"Resource uuid: {resource_uid}")
    resource_handler = ResourceHandler()
    try:
        updated_resource = resource_handler.delete(resource_uid=resource_uid)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple resources found")
    logger.debug(f"Deleted resource: {updated_resource}")
    return updated_resource.put()

@app.delete('/process/{process_uid}')
async def delete_specific_process(process_uid: str = None):
    logger.debug('DELETE on /process')
    logger.debug(f"Process uuid: {process_uid}")
    process_handler = ProcessHandler()
    try:
        updated_process = process_handler.delete(process_uid=process_uid)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple processes found")
    logger.debug(f"Deleted process: {updated_process}")
    return updated_process.put()

@app.delete('/workflow/{workflow_uid}')
async def delete_specific_workflow(workflow_uid: str = None):
    logger.debug('DELETE on /workflow')
    logger.debug(f"Resource uuid: {workflow_uid}")
    workflow_handler = WorkflowHandler()
    try:
        updated_workflow = workflow_handler.delete(workflow_uid=workflow_uid)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple workflows found")
    logger.debug(f"Deleted workflow: {updated_workflow}")
    return updated_workflow.put()

# Export Endpoints
@app.get('/export-projects')
async def export_projects(requests: Request):
    logger.debug('GET on /export-projects')
    project_handler = ProjectHandler()
    content = project_handler.export_projects()
    return content

@app.get('/export-resources')
async def export_resources(requests: Request):
    logger.debug('GET on /export-resources')
    resource_handler = ResourceHandler()
    content = resource_handler.export_resources()
    return content

@app.get('/export-processes')
async def export_processes(requests: Request):
    logger.debug('GET on /export-processes')
    process_handler = ProcessHandler()
    content = process_handler.export_processes()
    return content

@app.get('/export-workflows')
async def export_workflows(requests: Request):
    logger.debug('GET on /export-workflows')
    workflow_handler = WorkflowHandler()
    content = workflow_handler.export_workflows()
    return content
# export_databases

# Import Endpoints
@app.post('/import-projects')
async def import_projects(request: Request):
    logger.debug('POST on /import-projects')
    imported_projects = await request.json()
    logger.debug(imported_projects)
    project_handler = ProjectHandler()
    projects = project_handler.import_projects(dct=imported_projects)
    return {'projects': [p.put() for p in projects]}

@app.post('/import-resources')
async def import_resources(request: Request):
    logger.debug('POST on /import-resources')
    imported_resources = await request.json()
    logger.debug(imported_resources)
    resource_handler = ResourceHandler()
    resources = resource_handler.import_resources(dct=imported_resources)
    return {'resources': [p.put() for p in resources]}

@app.post('/import-processes')
async def import_processes(request: Request):
    logger.debug('POST on /import-processes')
    imported_processes = await request.json()
    logger.debug(imported_processes)
    process_handler = ProcessHandler()
    processes = process_handler.import_processes(dct=imported_processes)
    return {'processes': [p.put() for p in processes]}

@app.post('/import-workflows')
async def import_workflows(request: Request):
    logger.debug('POST on /import-workflows')
    imported_workflows = await request.json()
    logger.debug(imported_workflows)
    workflow_handler = WorkflowHandler()
    workflows = workflow_handler.import_workflows(dct=imported_workflows)
    return {'workflows': [p.put() for p in workflows]}
# import_databases

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
    balance_params = parse_query_params(request=request, query_class=BalanceWorkflowArgs)
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