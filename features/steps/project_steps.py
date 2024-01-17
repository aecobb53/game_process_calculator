from behave import *
# import sys
# sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
# from game_process_calculator import ProjectFilter


import requests

docker_url = 'http://0.0.0.0'
port = '8203'
base_url = docker_url + ':' + port

@given('I clear all test data')
def clear_test_data(context):
    resp = requests.post(f"{base_url}/clear-test-data")
    print(resp)
    print(resp.json())
    assert resp.ok

@given('I create a project with the name "{name}"')
def given_create_project(context, name):
    payload = {
        'name': name
    }
    resp = requests.post(f"{base_url}/projects", json=payload)
    print(resp)
    print(resp.json())
    assert resp.ok

@when('I capture the project id for "{name}" and save it to index "{index}"')
def capture_project_uid(context, name, index):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/projects", params=params)
    # print(resp.json())
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
    print('')
    print('')
    print('HERE')
    params = {
        'uid': context.tracked_project_uids[int(index)],
    }
    print(params)
    resp = requests.get(f"{base_url}/projects", params=params)
    print(resp)
    payload = resp.json()['projects'][0]
    print(payload)
    payload[name] = name
    # payload = {
    #     'name': name
    # }
    resp = requests.put(f"{base_url}/projects/{payload['uid']}", json=payload)
    print(resp)
    print(resp.json())
    assert resp.ok
    assert False

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