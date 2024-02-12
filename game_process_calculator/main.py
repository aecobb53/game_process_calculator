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
    ProcessType)
from handlers import ProjectHandler

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
    logger.debug('POST on /projects')
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
    project_handler = ProjectHandler()
    new_project = project_handler.create(project)
    return new_project.put()

# create_project
# create_resource
# create_process
# create_workflow

# Filter Endpoints
@app.get('/projects')
async def filter_projects(names: Optional[List[str]] = None):
    logger.debug('GET on /projects')
    project_handler = ProjectHandler()
    project_filter = ProjectFilter()
    projects = project_handler.filter(project_filter=project_filter)
    return {'projects': [p.put() for p in projects]}
# filter_projects
# filter_resources
# filter_processes
# filter_workflows

# Find Specific Endpoints
@app.get('/project/{project_uid}')
async def find_specific_project(project_uid: str = None):
    logger.debug('GET on /project')
    logger.debug(f"Project uuid: {project_uid}")
    project_handler = ProjectHandler()
    project_filter = ProjectFilter(uid=[project_uid])
    projects = project_handler.filter(project_filter=project_filter)

    if len(projects) == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    elif len(projects) == 1:
        return projects[0].put()
    else:
        raise HTTPException(status_code=404, detail="Multiple projects found")
# find_specific_project
# find_specific_resource
# find_specific_processe
# find_specific_workflow

# Update Endpoints
# update_project
@app.put('/project/{project_uuid}')
async def update_project(project_uuid: str, project: Project):
    logger.debug('PUT on /project')
    logger.debug(f"Project uuid: {project_uuid}")
    logger.debug(project)
    project.uid = project_uuid

    project_handler = ProjectHandler()
    try:
        updated_project = project_handler.update(project=project)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple projects found")
    logger.debug(f"Updated project: {updated_project}")
    return updated_project.put()
# update_resource
# update_process
# update_workflow

# Delete Endpoints
# delete_project
@app.delete('/project/{project_uid}')
async def delete_specific_project(project_uid: str = None):
    logger.debug('DELETE on /project')
    logger.debug(f"Project uuid: {project_uid}")
    project_handler = ProjectHandler()
    try:
        updated_project = project_handler.delete(project_uid=project_uid)
    except IndexError:
        logger.warning('Better error handling needs to be added!!!!')
        raise HTTPException(status_code=404, detail="Multiple projects found")
    logger.debug(f"Deleted project: {updated_project}")
    return updated_project.put()
# delete_resource
# delete_process
# delete_workflow

# Export Endpoints
# export_projects
@app.get('/export-projects')
async def export_projects(requests: Request):
    logger.debug('GET on /export-projects')
    project_handler = ProjectHandler()
    content = project_handler.export_projects()
    return content
# export_resources
# export_processs
# export_workflows
# export_databases

# Import Endpoints
# import_projects
@app.post('/import-projects')
async def import_projects(request: Request):
    logger.debug('POST on /import-projects')
    imported_projects = await request.json()
    logger.debug(imported_projects)
    project_handler = ProjectHandler()
    projects = project_handler.import_projects(dct=imported_projects)
    return {'projects': [p.put() for p in projects]}
# import_resources
# import_processs
# import_workflows
# import_databases









# # @app.get('/main-page', response_class=HTMLResponse)
# # async def current_builds(requests: Request):
# #     with open('templates/main_page.html', 'r') as hf:
# #         html_content = hf.read()
# #     return HTMLResponse(content=html_content, status_code=200)

# # @app.get('/test-get', resource_class=HTMLResponse)
# # async def test_get_endpoint(requests: Request):
# #     return HTMLResponse(status_code=200)

# # @app.get('/test-get-data', resource_class=HTMLResponse)
# # async def test_get_endpoint(requests: Request):
# #     data = {
# #         'results': [
# #             {}
# #         ]
# #     }
# #     return HTMLResponse(status_code=200)

# # @app.post('/test-post', resource_class=HTMLResponse)
# # async def test_post_endpoint(requests: Request):
# #     return HTMLResponse(status_code=200)

# # @app.put('/test-put', resource_class=HTMLResponse)
# # async def test_put_endpoint(requests: Request):
# #     return HTMLResponse(status_code=200)

# @app.get('/ifsc-data')
# async def ifsc_current_rankings_data(requests: Request):
#     logger.debug('GET on /ifsc-data')
#     data = search_ifsc_data()
#     content = {
#         "data": data
#     }
#     return content


# @app.get('/timecard')
# async def timecard_get(requests: Request, day: str = None):
#     logger.debug(f'day: {day}')
#     logger.debug('GET on /timecard')
#     tc = Timecard()
#     return tc.display_data(day=day)


# @app.get('/html/timecard')
# async def timecard_get(requests: Request):
#     logger.debug('GET on /html/timecard')
#     with open('templates/get_timecard_chargecodes.html', 'r') as hf:
#         html_content = hf.read()
#     return HTMLResponse(content=html_content, status_code=200)


# @app.put('/timecard')
# async def timecard_put(requests: Request, timecard_data: PUTTimecard):
#     logger.debug('PUT on /timecard')
#     logger.debug(f"timecard_data: {timecard_data}")
#     tc = Timecard()
#     tc.save(data=timecard_data)
#     return tc.data


# @app.post('/timecard-set')
# async def timecard_post(requests: Request, timecard_data: PUTTimecard):
#     logger.debug('POST on /timecard-set')
#     try:
#         tc = Timecard()
#         tc.save(data=timecard_data.put)
#         logger.debug(f"Database overwritten")
#     except Exception as err:
#         logger.error(f"Internal Exception raised: {err}")
#         return {'message': f"Internal Exception raised: {err}"}
#     return tc.data


# @app.post('/timecard-entry')
# async def timecard_post(requests: Request, timecard_entry: POSTTimecardEntry):
#     logger.debug('POST on /timecard-entry')
#     try:
#         tc = Timecard()
#         entry = timecard_entry.return_timecard_entry()
#         entry.validate_im_good()
#         tc.add_entry(entry=entry)
#         tc.save()
#     except ValueError as err:
#         logger.warning(f"{err}")
#         raise HTTPException(status_code=500, detail=f"{err}")
#     except Exception as err:
#         logger.warning(f"{err}")
#         raise HTTPException(status_code=500, detail=f"{err}")
#     return entry.put

# @app.put('/timecard-entry/{entry_id}')
# async def timecard_put(requests: Request, entry_id: str, timecard_entry: POSTTimecardEntry):
#     logger.debug('PUT on /timecard-entry')
#     try:
#         tc = Timecard()
#         entry = timecard_entry.return_timecard_entry()
#         entry.validate_im_good()
#         tc.update_entry(entry_id=entry_id, updated_entry=entry)
#         tc.save()
#     except ValueError as err:
#         logger.warning(f"{err}")
#         raise HTTPException(status_code=500, detail=f"{err}")
#     except Exception as err:
#         logger.warning(f"{err}")
#         raise HTTPException(status_code=500, detail=f"{err}")
#     return entry.put

# @app.get('/html/timecard-entry')
# async def timecard_get(requests: Request):
#     logger.debug('GET on /html/timecard-entry')
#     with open('templates/post_timecard_entry.html', 'r') as hf:
#         html_content = hf.read()
#     return HTMLResponse(content=html_content, status_code=200)

# @app.get('/charge-codes')
# async def timecard_get(requests: Request):
#     logger.debug('GET on /charge-codes')
#     charge_code_dict = {k: getattr(ShorthandMapping, k).value for k in [ShorthandMapping(e).name for e in ShorthandMapping]}
#     return charge_code_dict

# # Task Service
# @app.post('/task-service')
# async def task_service_post(requests: Request, task_service_payload: TaskServicePayload):
#     logger.debug('POST on /task-service')
#     save_task_service_payload(content=task_service_payload, logit=logger)
#     return {'status': 'Saved'}

# @app.get('/task-service')
# async def task_service_get(requests: Request):
#     logger.debug('GET on /task-service')
#     obj = load_task_service_payload(logit=logger)
#     return obj.put()