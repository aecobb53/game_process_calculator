import os
import json
from time import process_time, time

from behave import *
# import sys
# sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
# from game_process_calculator import ProjectFilter

from step_utils import compare_things


import requests

docker_url = 'http://0.0.0.0'
port = '8203'
base_url = docker_url + ':' + port
ft_resources = os.path.join(os.getcwd(), 'features', 'resources')

@given('I create a workflow with the name "{workflow_name}" in the project named "{project_name}" with the process_type of "{process_type}"')
def given_create_workflow(context, workflow_name, project_name, process_type):
    project_params = {
        'name': project_name
    }
    resp = requests.get(f"{base_url}/projects", params=project_params)
    assert resp.ok
    print(resp.json())
    print('posting workflow')
    workflow_payload = {
        'name': workflow_name,
        'project_uid': resp.json()['projects'][0]['uid'],
        'process_type': process_type,
    }
    print(workflow_payload)
    resp = requests.post(f"{base_url}/workflows", json=workflow_payload)
    print(resp.ok)
    print(resp.json())
    assert resp.ok
    if 'created_workflows' not in context:
        context.created_workflows = []
    context.created_workflows.append(resp.json())


@when('I capture the workflow id for "{name}" and save it to index "{index}"')
def capture_workflow_uid(context, name, index):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/workflows", params=params)
    # print(resp.json())
    assert resp.ok
    workflows = resp.json()['workflows']
    assert len(workflows) == 1
    workflow = workflows[0]
    if 'tracked_workflow_uids' not in context:
        context.tracked_workflow_uids = []
    if index == 'next':
        context.tracked_workflow_uids.append(workflow['uid'])
    else:
        context.tracked_workflow_uids[index] = workflow['uid']

@when('I modify the workflow at index "{index}" "{key}" to "{value}"')
def when_update_workflow(context, index, key, value):
    print(f"Modifying workflow at index {index} to {key} {value}")
    params = {
        'uid': context.tracked_workflow_uids[int(index)],
    }
    print(params)
    resp = requests.get(f"{base_url}/workflows", params=params)
    print(f"Get request for workflows code: {resp.status_code}")
    payload = resp.json()['workflows'][0]
    if value.startswith('[') and value.endswith(']'):
        value = json.loads(value)
    payload[key] = value
    print(f"Modified payload {payload}")
    resp = requests.put(f"{base_url}/workflow/{payload['uid']}", json=payload)
    print(resp.ok)
    assert resp.ok
    put_details = resp.json()
    print(resp.json())
    assert put_details[key] == value

@when('I delete the workflow at index "{index}"')
def when_delete_workflow(context, index):
    index = int(index)
    resp = requests.delete(f"{base_url}/workflow/{context.created_workflows[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@when('I modify the workflow id at index "{workflow_index}" to include process at index "{process_index}"')
def add_process_to_workflow(context, workflow_index, process_index):
    workflow_index = int(workflow_index)
    process_index = int(process_index)
    print(f"Adding process to workflow")
    print(f"  Workflow index: {workflow_index}")
    print(f"  Process index: {process_index}")
    workflow = context.created_workflows[workflow_index]
    process = context.created_processes[process_index]
    print(f"  Workflow: {workflow}")
    print(f"  Process: {process}")
    if workflow['process_uids'] is None:
        workflow['process_uids'] = []
    workflow['process_uids'].append(process['uid'])
    resp = requests.put(f"{base_url}/workflow/{workflow['uid']}", json=workflow)
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@when('I modify the workflow at index "{workflow_index}" to add resource at index "{resource_index}" as a focus resource')
def add_focus_resource_to_workflow(context, workflow_index, resource_index):
    workflow_index = int(workflow_index)
    resource_index = int(resource_index)
    print(f"Adding focus resource to workflow")
    print(f"  Workflow index: {workflow_index}")
    print(f"  Resource index: {resource_index}")
    workflow = context.created_workflows[workflow_index]
    resource = context.created_resources[resource_index]
    print(f"  Workflow: {workflow}")
    print(f"  Resource: {resource}")
    if workflow['focus_resource_uids'] is None:
        workflow['focus_resource_uids'] = []
    workflow['focus_resource_uids'].append(resource['uid'])
    resp = requests.put(f"{base_url}/workflow/{workflow['uid']}", json=workflow)
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@then('I should see "{name}" in the saved workflows')
def then_filter_workflows(context, name):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/workflows", params=params)
    print(resp)
    print(resp.json())
    assert resp.ok
    workflows = resp.json()['workflows']
    assert name in [p['name'] for p in workflows]

@then('I verify the workflow at index "{index}" {has_has_not} changed')
def then_verify_workflow(context, index, has_has_not):
    index = int(index)
    resp = requests.get(f"{base_url}/workflow/{context.created_workflows[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    if has_has_not == 'has not':
        print('in has not changed')
        assert context.created_workflows[index] == resp.json()
    else:
        print('in has changed')
        assert context.created_workflows[index] != resp.json()

@then('I verify the workflow at index "{index}" has been deleted')
def then_verify_workflow_deleted(context, index):
    print('TRYING TO VERIFY DELETE')
    index = int(index)
    resp = requests.get(f"{base_url}/workflow/{context.created_workflows[index]['uid']}")
    print(resp.ok)
    assert not resp.ok
    print(resp.json())
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Workflow not found'}

@then('I verify the workflows export "{matches_level}" "{file_path}"')
def verify_export_matches(context, matches_level, file_path):
    print(f"Verifying export workflows matches {file_path}")
    resp = requests.get(f"{base_url}/export-workflows")
    print(resp)
    print(resp.json())
    assert resp.ok
    resp_workflows = resp.json()
    print(ft_resources, file_path)
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    print(file_content)
    if matches_level == 'matches':
        for workflow in resp_workflows['workflows']:
            print(workflow)
            assert workflow['uid'] is not None
            assert workflow['creation_datetime'] is not None
            workflow['uid'] = None
            workflow['project_uid'] = None
            workflow['creation_datetime'] = None
        for workflow in file_content['workflows']:
            print(workflow)
            workflow['uid'] = None
            workflow['project_uid'] = None
    comparison_results = compare_things(file_content, resp_workflows, verbose=True)
    print(f"Comparison results: {comparison_results}")
    for i in comparison_results:
        print(f"    {i}")
    print('response workflows')
    print(json.dumps(resp_workflows, indent=4))
    print('file workflows')
    print(json.dumps(file_content, indent=4))
    assert resp_workflows == file_content

@given('I import workflows from "{file_path}"')
def verify_import_matches(context, file_path):
    print(f"Verifying import workflows matches {os.path.join(ft_resources, file_path)}")
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    resp = requests.post(f"{base_url}/import-workflows", json=file_content)
    print(resp)
    print(resp.json())
    assert resp.ok

@then('I want to look at the data')
def then_look_at_data(context):
    resp = requests.get(f"{base_url}/visualize-workflows")
    print(resp.ok)
    print(resp.json())
    assert resp.ok
    print(json.dumps(resp.json(), indent=4))
    workflows = resp.json()['workflows']
    for workflow in workflows:
        print(f"Workflow: {workflow['name']}")
        if workflow['process_type'] == 'LINEAR':
            for process in workflow['processes']:
                print(f"    Process: {process['name']}")
                process_time = process['process_time_seconds'] or 0
                rest_time = process['rest_time_seconds'] or 0
                time_for_process = process_time + rest_time
                print(f"        Run time: {time_for_process} (s)")
                for resource in process['consumes_resources']:
                    amount = process['consume_uids'][resource['uid']]
                    print(f"        Consumes: {resource['name']}: {amount}")
                for resource in process['produces_resources']:
                    amount = process['produce_uids'][resource['uid']]
                    print(f"        Produces: {resource['name']}: {amount}")

    assert False

@then('I want to look at the data at a balance of "{units_per_second}" units per second')
def then_look_at_data_with_balance(context, units_per_second):
    units_per_second = float(units_per_second)
    params = {
        'units_per_second': units_per_second
    }
    resp = requests.get(f"{base_url}/visualize-workflows", params=params)
    print(resp.ok)
    print(resp.json())
    assert resp.ok
    print(json.dumps(resp.json(), indent=4))
    workflows = resp.json()['workflows']
    for workflow in workflows:
        print(f"Workflow: {workflow['name']}")
        if workflow['process_type'] == 'LINEAR':
            for process in workflow['processes']:
                print(f"    Process: {process['name']}")
                process_time = process['process_time_seconds'] or 0
                rest_time = process['rest_time_seconds'] or 0
                time_for_process = process_time + rest_time
                print(f"        Run time: {time_for_process} (s)")
                for resource in process['consumes_resources']:
                    amount = process['consume_uids'][resource['uid']]
                    print(f"        Consumes: {resource['name']}: {amount}")
                for resource in process['produces_resources']:
                    amount = process['produce_uids'][resource['uid']]
                    print(f"        Produces: {resource['name']}: {amount}")

    assert False

@then('I visualize workflow at index "{index}" with html and a units per second of "{units_per_second}"')
def then_visualize_with_html(context, index, units_per_second):
    index = int(index)
    print('')
    print('')
    print('')
    print('VISUALIZING WORKFLOW WITH HTML')
    print(f"  Workflow index: {index}")
    # workflow = context.created_workflows[index]
    # print(f"  Workflow: {workflow}")
    # if workflow['focus_resource_uids'] is None:
    #     workflow['focus_resource_uids'] = []
    # resp = requests.get(f"{base_url}/html/visualize-workflows/{workflow['uid']}")
    if units_per_second is not None and units_per_second != 'None':
        units_per_second = float(units_per_second)
        params = {
            'units_per_second': units_per_second
        }
        resp = requests.get(f"{base_url}/html/visualize-workflows", params=params)
    else:
        resp = requests.get(f"{base_url}/html/visualize-workflows")
    print(resp.ok)
    print(resp.text)
    assert resp.ok
    assert resp.text is not None
    assert False

# # # @given('we have behave installed')
# # # def step_impl(context):
# # #     pass

# # # @when('we implement a test')
# # # def step_impl(context):
# # #     assert True is not False
# # #     assert False

# # # @then('behave will test it for us!')
# # # def step_impl(context):
# # #     assert context.failed is False

