import os
import json

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

# @given('I clear all test data')
# def clear_test_data(context):
#     resp = requests.post(f"{base_url}/clear-test-data")
#     print(resp)
#     print(resp.json())
#     assert resp.ok

@given('I create a project with the name "{name}"')
def given_create_project(context, name):
    payload = {
        'name': name
    }
    print(payload)
    resp = requests.post(f"{base_url}/projects", json=payload)
    print(resp)
    print(resp.json())
    if 'created_projects' not in context:
        context.created_projects = []
    context.created_projects.append(resp.json())
    assert resp.ok

@when('I capture the project id for "{name}" and save it to index "{index}"')
def capture_project_uid(context, name, index):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/projects", params=params)
    assert resp.ok
    projects = resp.json()['projects']
    assert len(projects) == 1
    project = projects[0]
    if 'tracked_project_uids' not in context:
        context.tracked_project_uids = []
    if index == 'next':
        context.tracked_project_uids.append(project['uid'])
    else:
        context.tracked_project_uids[index] = project['uid']

@when('I modify the project at index "{index}" name to "{name}"')
def when_update_project(context, index, name):
    print(f"Modifying project at index {index} to name {name}")
    params = {
        'uid': context.tracked_project_uids[int(index)],
    }
    print(params)
    resp = requests.get(f"{base_url}/projects", params=params)
    print(f"Get request for projects code: {resp.status_code}")
    payload = resp.json()['projects'][0]
    print(f"Payload to modify: {payload}")
    payload['name'] = name
    print(f"Modified payload {payload}")
    resp = requests.put(f"{base_url}/project/{payload['uid']}", json=payload)
    print(f"PUT response code: {resp.status_code}")
    print(f"PUT response: {resp.json()}")
    print(resp.ok)
    assert resp.ok
    put_details = resp.json()
    print(resp.json())
    assert put_details['name'] == name

@when('I delete the project at index "{index}"')
def when_delete_project(context, index):
    index = int(index)
    resp = requests.delete(f"{base_url}/project/{context.created_projects[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@then('I should see "{name}" in the saved projects')
def then_filter_projects(context, name):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/projects", params=params)
    print(resp)
    print(resp.json())
    assert resp.ok
    projects = resp.json()['projects']
    assert name in [p['name'] for p in projects]

@then('I verify the project at index "{index}" {has_has_not} changed')
def then_verify_project(context, index, has_has_not):
    index = int(index)
    print(f"Verifying project at index {index} has changed: {has_has_not}")
    resp = requests.get(f"{base_url}/project/{context.created_projects[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    if has_has_not == 'has not':
        print('in has not changed')
        assert context.created_projects[index] == resp.json()
    else:
        print('in has changed')
        assert context.created_projects[index] != resp.json()

@then('I verify the project at index "{index}" has been deleted')
def then_verify_project_deleted(context, index):
    print('TRYING TO VERIFY DELETE')
    index = int(index)
    resp = requests.get(f"{base_url}/project/{context.created_projects[index]['uid']}")
    print(resp.ok)
    assert not resp.ok
    print(resp.json())
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Project not found'}

@then('I verify the projects export "{matches_level}" "{file_path}"')
def verify_export_matches(context, matches_level, file_path):
    print(f"Verifying export projects matches {file_path}")
    resp = requests.get(f"{base_url}/export-projects")
    print(resp)
    print(resp.json())
    assert resp.ok
    resp_projects = resp.json()
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    if matches_level == 'matches':
        for project in resp_projects['projects']:
            print(project)
            assert project['uid'] is not None
            assert project['creation_datetime'] is not None
            project['uid'] = None
            project['creation_datetime'] = None
        for project in file_content['projects']:
            print(project)
            project['uid'] = None
    comparison_results = compare_things(file_content, resp_projects, verbose=True)
    print(f"Comparison results: {comparison_results}")
    for i in comparison_results:
        print(f"    {i}")
    print('response projects')
    print(json.dumps(resp_projects, indent=4))
    print('file projects')
    print(json.dumps(file_content, indent=4))
    assert resp_projects == file_content

@given('I import projects from "{file_path}"')
def verify_import_matches(context, file_path):
    print(f"Verifying import projects matches {os.path.join(ft_resources, file_path)}")
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    resp = requests.post(f"{base_url}/import-projects", json=file_content)
    print(resp)
    print(resp.json())
    assert resp.ok

# @given('we have behave installed')
# def step_impl(context):
#     pass

# @when('we implement a test')
# def step_impl(context):
#     assert True is not False
#     assert False

# @then('behave will test it for us!')
# def step_impl(context):
#     assert context.failed is False

