from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

from models import WorkflowFilter, BalanceWorkflowArgs
from handlers import WorkflowHandler
from utils import parse_query_params, MissingRecordException, DuplicateRecordsException
from app_files import ContextSingleton

from html import (
    # WorkflowDisplay,
    # create_project_html_page,
    # filter_projects_html_page,
    # find_project_html_page,
    # project_base_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/calculator',
    tags=['calculator', 'html'],
)


@router.get('/workflow')
async def html_calculate(request: Request):
    # project_page = unimplemented_page()
    # return HTMLResponse(content=project_page, status_code=501)




    # logger.debug('GET on /html/visualize-workflows')
    workflow_filter = parse_query_params(request=request, query_class=WorkflowFilter)
    # logger.debug(f'Workflow Filter: {workflow_filter}')
    balance_params = parse_query_params(request=request, query_class=BalanceWorkflowArgs)
    # logger.debug(f'Balance Params: {balance_params}')
    # data_handler = DataHandler()
    wh = WorkflowHandler()
    workflows = wh.filter_workflows(workflow_filter=workflow_filter)
    workflows_dict = data_handler.return_complex_workflow_object(
        workflows=workflows,
        balance_criteria=balance_params)
    workflow_doc = WorkflowDisplay(workflows_dict=workflows_dict)
    workflow_html = workflow_doc.display_workflow()
    with open(os.path.join('deleteme_html_files', 'workflow.html'), 'w') as f:
        f.write(workflow_html)
    return HTMLResponse(content=workflow_html, status_code=200)





# @router.get('/modify')
# async def html_modify_project(request: Request):
#     project_page = create_project_html_page()
#     return HTMLResponse(content=project_page, status_code=200)


# @router.get('/{project_uid}')
# async def html_project_project_uid(request: Request, project_uid: str):
#     ph = ProjectHandler()
#     try:
#         project = await ph.find_project(project_uid=project_uid)
#     except MissingRecordException as err:
#         context.logger.error(f"ERROR: {err}")
#         raise HTTPException(status_code=404, detail=str(err))
#     except DuplicateRecordsException as err:
#         context.logger.error(f"ERROR: {err}")
#         raise HTTPException(status_code=404, detail=str(err))
#     except Exception as err:
#         context.logger.error(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Server Error')
#     project_page = find_project_html_page(project=project)
#     return HTMLResponse(content=project_page, status_code=200)
