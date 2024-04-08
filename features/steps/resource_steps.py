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

@given('I create a resource with the name "{resource_name}" in the project named "{project_name}"')
def given_create_resource(context, resource_name, project_name):
    project_params = {
        'name': project_name
    }
    resp = requests.get(f"{base_url}/projects", params=project_params)
    assert resp.ok
    print(resp.json())
    print('posting resource')
    resource_payload = {
        'name': resource_name,
        'project_uid': resp.json()['projects'][0]['uid']
    }
    print(resource_payload)
    resp = requests.post(f"{base_url}/resources", json=resource_payload)
    print(resp.ok)
    print(resp.json())
    assert resp.ok
    if 'created_resources' not in context:
        context.created_resources = []
    context.created_resources.append(resp.json())


@when('I capture the resource id for "{name}" and save it to index "{index}"')
def capture_resource_uid(context, name, index):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/resources", params=params)
    # print(resp.json())
    assert resp.ok
    resources = resp.json()['resources']
    assert len(resources) == 1
    resource = resources[0]
    if 'tracked_resource_uids' not in context:
        context.tracked_resource_uids = []
    if index == 'next':
        context.tracked_resource_uids.append(resource['uid'])
    else:
        context.tracked_resource_uids[index] = resource['uid']

@when('I modify the resource at index "{index}" name to "{name}"')
def when_update_resource(context, index, name):
    print(f"Modifying resource at index {index} to name {name}")
    params = {
        'uid': context.tracked_resource_uids[int(index)],
    }
    print(params)
    resp = requests.get(f"{base_url}/resources", params=params)
    print(f"Get request for resources code: {resp.status_code}")
    payload = resp.json()['resources'][0]
    print(f"Modified payload {payload}")
    payload['name'] = name
    resp = requests.put(f"{base_url}/resource/{payload['uid']}", json=payload)
    print(resp.ok)
    assert resp.ok
    put_details = resp.json()
    print(resp.json())
    assert put_details['name'] == name

@when('I delete the resource at index "{index}"')
def when_delete_resource(context, index):
    index = int(index)
    resp = requests.delete(f"{base_url}/resource/{context.created_resources[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@then('I should see "{name}" in the saved resources')
def then_filter_resources(context, name):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/resources", params=params)
    print(resp)
    print(resp.json())
    assert resp.ok
    resources = resp.json()['resources']
    assert name in [p['name'] for p in resources]

@then('I verify the resource at index "{index}" {has_has_not} changed')
def then_verify_resource(context, index, has_has_not):
    index = int(index)
    resp = requests.get(f"{base_url}/resource/{context.created_resources[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    if has_has_not == 'has not':
        print('in has not changed')
        assert context.created_resources[index] == resp.json()
    else:
        print('in has changed')
        assert context.created_resources[index] != resp.json()

@then('I verify the resource at index "{index}" has been deleted')
def then_verify_resource_deleted(context, index):
    print('TRYING TO VERIFY DELETE')
    index = int(index)
    resp = requests.get(f"{base_url}/resource/{context.created_resources[index]['uid']}")
    print(resp.ok)
    assert not resp.ok
    print(resp.json())
    assert resp.status_code == 404

@then('I verify the resources export "{matches_level}" "{file_path}"')
def verify_export_matches(context, matches_level, file_path):
    print(f"Verifying export resources matches {file_path}")
    resp = requests.get(f"{base_url}/export-resources")
    print(resp)
    print(resp.json())
    assert resp.ok
    resp_resources = resp.json()
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    if matches_level == 'matches':
        for resource in resp_resources['resources']:
            print(resource)
            assert resource['uid'] is not None
            assert resource['creation_datetime'] is not None
            resource['uid'] = None
            resource['project_uid'] = None
            resource['creation_datetime'] = None
        for resource in file_content['resources']:
            print(resource)
            resource['uid'] = None
            resource['project_uid'] = None
    print('response resources')
    print(json.dumps(resp_resources, indent=4))
    print('file resources')
    print(json.dumps(file_content, indent=4))
    assert resp_resources == file_content

@given('I import resources from "{file_path}"')
def verify_import_matches(context, file_path):
    print(f"Verifying import resources matches {os.path.join(ft_resources, file_path)}")
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    resp = requests.post(f"{base_url}/import-resources", json=file_content)
    print(resp)
    print(resp.json())
    assert resp.ok

@then('I create a resource with the name "{resource_name}" in the project named "{project_name}" should have a status code of "{status_code}"')
def given_create_resource_with_code(context, resource_name, project_name, status_code):
    status_code = int(status_code)
    project_params = {
        'name': project_name
    }
    try:
        resp = requests.get(f"{base_url}/projects", params=project_params)
        project_uid =resp.json()['projects'][0]['uid']
    except:
        project_uid = 'UNKNOWN'
    print('posting resource')
    resource_payload = {
        'name': resource_name,
        'project_uid': project_uid
    }
    print(resource_payload)
    resp = requests.post(f"{base_url}/resources", json=resource_payload)
    print(resp.ok)
    print(resp.json())
    assert resp.status_code == status_code
    if 'created_resources' not in context:
        context.created_resources = []
    context.created_resources.append(resp.json())

# # @given('we have behave installed')
# # def step_impl(context):
# #     pass

# # @when('we implement a test')
# # def step_impl(context):
# #     assert True is not False
# #     assert False

# # @then('behave will test it for us!')
# # def step_impl(context):
# #     assert context.failed is False

