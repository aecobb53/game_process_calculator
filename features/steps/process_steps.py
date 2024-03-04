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

@given('I create a process with the name "{process_name}" in the project named "{project_name}"')
def given_create_process(context, process_name, project_name):
    project_params = {
        'name': project_name
    }
    resp = requests.get(f"{base_url}/projects", params=project_params)
    assert resp.ok
    print(resp.json())
    print('posting process')
    process_payload = {
        'name': process_name,
        'project_uid': resp.json()['projects'][0]['uid']
    }
    print(process_payload)
    resp = requests.post(f"{base_url}/processes", json=process_payload)
    print(resp.ok)
    print(resp.json())
    assert resp.ok
    if 'created_processes' not in context:
        context.created_processes = []
    context.created_processes.append(resp.json())

@when('I capture the process id for "{name}" and save it to index "{index}"')
def capture_process_uid(context, name, index):
    params = {
        'name': [name, 'other']
    }
    resp = requests.get(f"{base_url}/processes", params=params)
    print(resp.json())
    assert resp.ok
    processes = resp.json()['processes']
    assert len(processes) == 1
    print('')
    print('')
    print('')
    print('')
    print('')
    print('HERE')
    print(processes)
    assert len(processes) == 1
    process = processes[0]
    print(process)
    if 'tracked_process_uids' not in context:
        context.tracked_process_uids = []
    if index == 'next':
        context.tracked_process_uids.append(process['uid'])
    else:
        context.tracked_process_uids[index] = process['uid']

@when('I modify the process at index "{index}" name to "{name}"')
def when_update_process(context, index, name):
    print(f"Modifying process at index {index} to name {name}")
    params = {
        'uid': context.tracked_process_uids[int(index)],
    }
    print(params)
    resp = requests.get(f"{base_url}/processes", params=params)
    print(f"Get request for processes code: {resp.status_code}")
    payload = resp.json()['processes'][0]
    print(f"Modified payload {payload}")
    payload['name'] = name
    resp = requests.put(f"{base_url}/process/{payload['uid']}", json=payload)
    print(resp.ok)
    assert resp.ok
    put_details = resp.json()
    print(resp.json())
    assert put_details['name'] == name

@when('I modify the process id at index "{process_index}" to "{consume_or_produce}" resource at index '
      '"{resource_index}" in quantity "{quantity}"')
def add_resource_to_process(context, process_index, consume_or_produce, resource_index, quantity):
    process_index = int(process_index)
    resource_index = int(resource_index)
    quantity = float(quantity)
    print(f"Adding resource to process")
    print(f"  Process index: {process_index}")
    print(f"  Resource index: {resource_index}")
    print(f"  With quantity: {quantity}")
    print(f"  Consume or produce: {consume_or_produce}")
    process_index = int(process_index)
    resource_index = int(resource_index)
    process = context.created_processes[process_index]
    resource = context.created_resources[resource_index]
    if consume_or_produce == 'consume':
        if process['consume_uids'] is None:
            process['consume_uids'] = {}
        process['consume_uids'][resource['uid']] = quantity
    elif consume_or_produce == 'produce':
        if process['produce_uids'] is None:
            process['produce_uids'] = {}
        process['produce_uids'][resource['uid']] = quantity
    resp = requests.put(f"{base_url}/process/{process['uid']}", json=process)
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@when('I modify the process id at index "{process_index}" to have a "{process_or_rest}" time of "{time_s}"')
def add_process_time(context, process_index, process_or_rest, time_s):
    process_index = int(process_index)
    time_s = float(time_s)
    print(f"Adding {process_or_rest} time to process")
    print(f"  Process index: {process_index}")
    print(f"  Time: {time_s}")
    process = context.created_processes[process_index]
    if process_or_rest == 'process':
        process['process_time_seconds'] = time_s
    elif process_or_rest == 'rest':
        process['rest_time_seconds'] = time_s
    resp = requests.put(f"{base_url}/process/{process['uid']}", json=process)
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@when('I delete the process at index "{index}"')
def when_delete_resource(context, index):
    index = int(index)
    resp = requests.delete(f"{base_url}/process/{context.created_processes[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    assert resp.ok

@then('I should see "{name}" in the saved processes')
def then_filter_processes(context, name):
    params = {
        'name': name
    }
    resp = requests.get(f"{base_url}/processes", params=params)
    print(resp)
    print(resp.json())
    assert resp.ok
    processes = resp.json()['processes']
    assert name in [p['name'] for p in processes]

@then('I verify the process at index "{index}" {has_has_not} changed')
def then_verify_process(context, index, has_has_not):
    index = int(index)
    resp = requests.get(f"{base_url}/process/{context.created_processes[index]['uid']}")
    print(resp.ok)
    print(resp.json())
    if has_has_not == 'has not':
        print('in has not changed')
        assert context.created_processes[index] == resp.json()
    else:
        print('in has changed')
        assert context.created_processes[index] != resp.json()

@then('I verify the process at index "{index}" has been deleted')
def then_verify_resource_deleted(context, index):
    print('TRYING TO VERIFY DELETE')
    index = int(index)
    resp = requests.get(f"{base_url}/process/{context.created_processes[index]['uid']}")
    print(resp.ok)
    assert not resp.ok
    print(resp.json())
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Process not found'}

@then('I verify the processes export "{matches_level}" "{file_path}"')
def verify_export_matches(context, matches_level, file_path):
    print(f"Verifying export processes matches {file_path}")
    resp = requests.get(f"{base_url}/export-processes")
    print(resp)
    print(resp.json())
    assert resp.ok
    resp_processes = resp.json()
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    print('made it here')

    if matches_level == 'matches':
        for process in resp_processes['processes']:
            print(process)
            assert process['uid'] is not None
            assert process['creation_datetime'] is not None
            process['uid'] = None
            process['project_uid'] = None
            process['creation_datetime'] = None
        for process in file_content['processes']:
            print(process)
            process['uid'] = None
            process['project_uid'] = None
    comparison_results = compare_things(file_content, resp_processes, verbose=True)
    print(f"Comparison results: {comparison_results}")
    for i in comparison_results:
        print(f"    {i}")
    print('response processes')
    print(json.dumps(resp_processes, indent=4))
    print('file processes')
    print(json.dumps(file_content, indent=4))
    assert comparison_results == []

@given('I import processes from "{file_path}"')
def verify_import_matches(context, file_path):
    print(f"Verifying import processes matches {os.path.join(ft_resources, file_path)}")
    with open(os.path.join(ft_resources, file_path), 'r') as fl:
        file_content = json.load(fl)
    resp = requests.post(f"{base_url}/import-processes", json=file_content)
    print(resp)
    print(resp.json())
    assert resp.ok

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

