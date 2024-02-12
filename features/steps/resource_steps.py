from behave import *
# import sys
# sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
# from game_process_calculator import ProjectFilter


import requests

docker_url = 'http://0.0.0.0'
port = '8203'
base_url = docker_url + ':' + port

@given('I create a resource with the name "{resource_name}" and the project name "{project_name}"')
def given_create_resource(context, resource_name, project_name):
    print('GET PROJECT')
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


# @when('I capture the project id for "{name}" and save it to index "{index}"')
# def capture_project_uid(context, name, index):
#     params = {
#         'name': name
#     }
#     resp = requests.get(f"{base_url}/projects", params=params)
#     # print(resp.json())
#     assert resp.ok
#     projects = resp.json()['projects']
#     assert len(projects) == 1
#     project = projects[0]
#     if 'tracked_project_uids' not in context:
#         context.tracked_project_uids = []
#     if index == 'next':
#         context.tracked_project_uids.append(project['uid'])
#     else:
#         context.tracked_project_uids[index] = project['uid']

# @when('I modify the project at index "{index}" name to "{name}"')
# def when_update_resource(context, index, name):
#     print(f"Modifying project at index {index} to name {name}")
#     params = {
#         'uid': context.tracked_project_uids[int(index)],
#     }
#     print(params)
#     resp = requests.get(f"{base_url}/projects", params=params)
#     print(f"Get request for projects code: {resp.status_code}")
#     payload = resp.json()['projects'][0]
#     print(f"Modified paylode{payload}")
#     payload['name'] = name
#     resp = requests.put(f"{base_url}/project/{payload['uid']}", json=payload)
#     print(resp.ok)
#     assert resp.ok
#     put_details = resp.json()
#     print(resp.json())
#     assert put_details['name'] == name

# @when('I delete the project at index "{index}"')
# def when_delete_resource(context, index):
#     index = int(index)
#     resp = requests.delete(f"{base_url}/project/{context.created_projects[index]['uid']}")
#     print(resp.ok)
#     print(resp.json())
#     assert resp.ok

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

# @then('I verify the project at index "{index}" {has_has_not} changed')
# def then_verify_resource(context, index, has_has_not):
#     index = int(index)
#     resp = requests.get(f"{base_url}/project/{context.created_projects[index]['uid']}")
#     print(resp.ok)
#     print(resp.json())
#     if has_has_not == 'has not':
#         print('in has not changed')
#         assert context.created_projects[index] == resp.json()
#     else:
#         print('in has changed')
#         assert context.created_projects[index] != resp.json()

# @then('I verify the project at index "{index}" has been deleted')
# def then_verify_project_deleted(context, index):
#     print('TRYING TO VERIFY DELETE')
#     index = int(index)
#     resp = requests.get(f"{base_url}/project/{context.created_projects[index]['uid']}")
#     print(resp.ok)
#     assert not resp.ok
#     print(resp.json())
#     assert resp.status_code == 404
#     assert resp.json() == {'detail': 'Project not found'}



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

