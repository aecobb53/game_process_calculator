import os
import json
import re

from typing import List, Dict
from copy import deepcopy
from datetime import datetime, timedelta

from factorio_data_objects import (
    FactorioDataItem,
    FactorioDataMachine,
    FactorioDataLogistics,
    FactorioDataResource,
    FactorioDataRecipe)
from rest_data_loader import RestDataLoader

factorio_recipie_lister_path = '/mnt/c/Users/aecob/AppData/Roaming/Factorio/script-output/recipe-lister'
# print(os.path.exists(factorio_recipie_lister_path))
# for i in os.listdir(factorio_recipie_lister_path):
#     print(i)

any_rest_calls = True
upload_data = True
timer_start_time = datetime.now()
print(f"Starting upload: {timer_start_time}")

if any_rest_calls:
    rdl = RestDataLoader()
    resp = rdl.get_project(params={'name':'Factorio'})
    if resp.json()['projects']:
        project_uid = resp.json()['projects'][0]['uid']
    else:
        if upload_data:
            resp = rdl.post_project(json={'name':'Factorio'})
            project_uid = resp.json()['uid']
        else:
            project_uid = 'edf22127-6a1a-4f0b-bafb-2c0ba208cf68'
else:
    project_uid = 'edf22127-6a1a-4f0b-bafb-2c0ba208cf68'

# ITEMS
item_file_list = [
    'item.json',
    'fluid.json',
]
item_objects = []
for fl in item_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        item = json.load(f)
        index = 0
        for key, value in item.items():
            if key in ['fluid-unknown']:
                continue
            value['filename'] = fl
            try:
                value['project_uid'] = project_uid
                obj = FactorioDataItem.model_validate(value)
                item_objects.append(obj)
                # obj.json_out()
            except Exception as e:
                print(f"Error: {e}")
                print('ITEM')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1


# MACHINES
machine_file_list = [
    'assembling-machine.json',
    'boiler.json',
    'furnace.json',
    'generator.json',
    'lab.json',
    'mining-drill.json',
    'reactor.json',
    'rocket-silo.json',
    'solar-panel.json',
]
machine_objects = []
for fl in machine_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            value['project_uid'] = project_uid
            try:
                obj = FactorioDataMachine.model_validate(value)
                machine_objects.append(obj)
                obj.json_out()
            except Exception as e:
                print(f"Error: {e}")
                print('MACHINE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
machine_objects.append(FactorioDataMachine(
    filename="assembling-machine.json",
    name="angels-manual-crafting",
    localised_name=[],
    notes=['Added manually to populate script'],
    project_uid=project_uid,
    type="manual-crafting",
    energy_usage=0,
    crafting_speed=1.0,
    crafting_categories={
        "angels-manual-crafting": True
    },
    energy_source={},
    pollution=0.0,))


# INFRASTRUCTURE
logistics_file_list = [
    'inserter.json',
    'transport-belt.json',
]
logistics_objects = []
for fl in logistics_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                value['project_uid'] = project_uid
                obj = FactorioDataLogistics.model_validate(value)
                logistics_objects.append(obj)
                obj.json_out()
            except Exception as e:
                print(f"Error: {e}")
                print('INFRASTRUCTURE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1


# RESOURCE
resource_file_list = [
    'resource.json',
]
resource_objects = []
for fl in resource_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                value['project_uid'] = project_uid
                obj = FactorioDataResource.model_validate(value)
                resource_objects.append(obj)
                obj.json_out()
                # print(json.dumps(obj.json_out(), indent=4))
                # exit()
            except Exception as e:
                print(f"Error: {e}")
                print('RESOURCE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                value['autoplace_specification'] = None
                # print(f"Value: {json.dumps(list(value.keys()), indent=4)}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1


# RECIPE
recipe_file_list = [
    'recipe.json',
]
recipe_objects = []
for fl in recipe_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                value['project_uid'] = project_uid
                obj = FactorioDataRecipe.model_validate(value)
                recipe_objects.append(obj)
                obj.json_out()
            except Exception as e:
                print(f"Error: {e}")
                print('RECIPE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1







def find_item_by_name(name: str, item_objects: List[FactorioDataItem | Dict]) -> FactorioDataItem:
    for index, item in enumerate(item_objects):
        if isinstance(item, dict):
            if item['name'] == name:
                return item
                # return index, item
        else:
            if item.name == name:
                return item
                # return index, item

def find_machine_by_crafting_category(target_crafting_category: str, machine_objects: List[FactorioDataMachine]) -> List[FactorioDataMachine]:
    machines = []
    for machine in machine_objects:
        if machine.crafting_categories:
            for crafting_category, enabled in machine.crafting_categories.items():
                if target_crafting_category == crafting_category and enabled:
                    machines.append(machine)
    return machines



print(f"item_objects: [{len(item_objects)}]")
print(f"machine_objects: [{len(machine_objects)}]")
print(f"logistics_objects: [{len(logistics_objects)}]")
print(f"resource_objects: [{len(resource_objects)}]")
print(f"recipe_objects: [{len(recipe_objects)}]")

uploaded_resources = []
uploaded_processes = []

failed_upload_resources = []
failed_upload_processes = []

any_rest_calls = True
print(f"UPLOADING ITEMS: [{len(item_objects)}]")
logging_interval = len(item_objects) // 10 + 1
for index, item in enumerate(item_objects):
    # Mock Post
    item.notes = [f"Uploaded from script."]

    payload = item.return_resource()
    if any_rest_calls:
        resp = rdl.get_resource(params={'name': item.name, 'project_uid': project_uid})
        if len(resp.json()['resources']) == 0:
            if upload_data:
                resp = rdl.post_resource(json=payload)
                item.resource_uid = resp.json()['uid']
        elif len(resp.json()['resources']) == 1:
            if upload_data:
                resource = resp.json()['resources'][0]
                for key, value in payload.items():
                    resource[key] = value
                resp = rdl.put_resource(resource_uid=resource['uid'], json=resource)
                item.resource_uid = resp.json()['uid']
        else:
            raise Exception(f"Multiple resources found for {item.name}")
    if not item.resource_uid:
        item.resource_uid = 'GPC_RESOURCE_UID'

    uploaded_resources.append(item)
    # print(json.dumps(item.json_out(), indent=4))
    # print(json.dumps(item.return_resource(), indent=4))
    # break
    if index % logging_interval == 0:
        print(f"Uploaded [{index}] of [{len(item_objects)}] items DONE. Or about [{index // logging_interval * 10}%]")
print('DONE UPLOADING ITEMS')

any_rest_calls = True
resources_in_project = rdl.get_resource(params={'project_uid': project_uid, 'limit': 100_000}).json()['resources']
print(f"UPLOADING RESOURCES: [{len(resource_objects)}]")
logging_interval = len(resource_objects) // 10 + 1
for index, item in enumerate(resource_objects):
    # Mock Post
    item.notes = [f"Uploaded from script."]
    for product in item.mineable_properties.products:
        resource_obj = find_item_by_name(product.name, resources_in_project)
        if resource_obj is None:
            raise ValueError(f"Resource not found: {product.name}")
        if isinstance(resource_obj, dict):
            item.produce_uids[resource_obj['uid']] = product.amount / product.probability
        else:
            item.produce_uids[resource_obj.resource_uid] = product.amount / product.probability
        if product.type == 'fluid':
            item.machine_uid = 'GPC_FLUID_MACHINE_UID'
        elif product.type == 'item':
            item.machine_uid = 'GPC_ITEM_MACHINE_UID'
        else:
            print('NOT MAPPED ITEM!!')
            exit()

    payload = item.return_process()
    if any_rest_calls:
        resp = rdl.get_process(params={'name': item.name, 'project_uid': project_uid})
        if len (resp.json()['processes']) == 0:
            if upload_data:
                resp = rdl.post_process(json=payload)
                item.process_uid = resp.json()['uid']
        elif len (resp.json()['processes']) == 1:
            if upload_data:
                process = resp.json()['processes'][0]
                for key, value in payload.items():
                    process[key] = value
                resp = rdl.put_process(process_uid=process['uid'], json=payload)
                item.process_uid = resp.json()['uid']
        else:
            raise Exception(f"Multiple processes found for {item.name}")

    if not item.process_uid:
        item.process_uid = 'GPC_PROCESS_UID'

    uploaded_processes.append(item)

    # print(json.dumps(item.return_process(), indent=4))
    # break
    if index % logging_interval == 0:
        print(f"Uploaded [{index}] of [{len(resource_objects)}] items DONE. Or about [{index // logging_interval * 10}%]")
print('DONE UPLOADING RESOURCES')

any_rest_calls = True
resources_in_project = rdl.get_resource(params={'project_uid': project_uid, 'limit': 100_000}).json()['resources']
print(f"UPLOADING RECIPES: [{len(recipe_objects)}]")
logging_interval = len(recipe_objects) // 10 + 1
for index, item in enumerate(recipe_objects):
    machines = find_machine_by_crafting_category(item.category, machine_objects)
    for machine in machines:
        item.notes = [f"Uploaded from script."]
        new_item = deepcopy(item)
        new_item.name = f"{item.name}::{machine.name}"
        new_item.notes.append(f"For machine [{machine.name}]")
        mock_machine_uid = f'GPC_MACHINE_UID-{machine.name}'
        new_item.machine_uid = mock_machine_uid

        """
        Amount calculation
        general_amount = (amount / probability)  # composite of changes to produce items and how many are produced
        general_speed = (speed_seconds / crafting_speed)  # crafting speed adjusted for speed factor
            For the life of me I cant find speed_seconds anywhere so by default its 1
        units_per_second = general_amount / general_speed
        """
        # Consumes
        if new_item.ingredients:
            for ingredient in new_item.ingredients:
                if ingredient.amount is None:
                    continue
                resource_obj = find_item_by_name(ingredient.name, resources_in_project)
                probability = ingredient.probability if ingredient.probability else 1
                general_amount = ingredient.amount / probability
                general_speed = 1 / machine.crafting_speed
                if isinstance(resource_obj, dict):
                    new_item.consume_uids[resource_obj['uid']] = general_amount
                else:
                    new_item.consume_uids[resource_obj.resource_uid] = general_amount
                new_item.process_time_seconds = general_speed
        # Produces
        if new_item.products:
            for product in new_item.products:
                if product.amount is None:
                    continue
                resource_obj = find_item_by_name(product.name, resources_in_project)
                probability = product.probability if product.probability else 1
                general_amount = product.amount / probability
                general_speed = 1 / machine.crafting_speed
                if isinstance(resource_obj, dict):
                    new_item.produce_uids[resource_obj['uid']] = general_amount
                else:
                    new_item.produce_uids[resource_obj.resource_uid] = general_amount
                new_item.process_time_seconds = general_speed
        # print(json.dumps(new_item.json_out(), indent=4))
        # print(json.dumps(new_item.return_process(), indent=4))
        # exit()

        payload = new_item.return_process()
        if any_rest_calls:
            resp = rdl.get_process(params={'name': new_item.name, 'project_uid': project_uid})
            if len (resp.json()['processes']) == 0:
                if upload_data:
                    resp = rdl.post_process(json=payload)
                    new_item.process_uid = resp.json()['uid']
            elif len (resp.json()['processes']) == 1:
                if upload_data:
                    process = resp.json()['processes'][0]
                    resp = rdl.put_process(process_uid=process['uid'], json=payload)
                    new_item.process_uid = resp.json()['uid']
            else:
                raise Exception(f"Multiple processes found for {new_item.name}")

        if not item.process_uid:
            item.process_uid = 'GPC_PROCESS_UID'

        uploaded_processes.append(new_item)
    if not machines:
        print(json.dumps(item.json_out(), indent=4))
        print(json.dumps(item.return_process(), indent=4))
        raise ValueError(f"No machines found for {item.name}")
    if index % logging_interval == 0:
        print(f"Uploaded [{index}] of [{len(recipe_objects)}] items DONE. Or about [{index // logging_interval * 10}%]")
print('DONE UPLOADING RECIPES')


print(f"uploaded_resources: [{len(uploaded_resources)}]")
print(f"uploaded_processes: [{len(uploaded_processes)}]")

timer_stop_time = datetime.now()
print(f"Finished Upload: {timer_stop_time}")
print(f"Total Time: {timer_stop_time - timer_start_time}")
