import os
import json
import re

from typing import List
from copy import deepcopy

from factorio_data_objects import FactorioDataItem, FactorioDataMachine, FactorioDataLogistics, FactorioDataResource, FactorioDataRecipe

factorio_recipie_lister_path = '/mnt/c/Users/aecob/AppData/Roaming/Factorio/script-output/recipe-lister'
# print(os.path.exists(factorio_recipie_lister_path))
# for i in os.listdir(factorio_recipie_lister_path):
#     print(i)

project_uid = '2579ad75-87c0-4152-9bd3-90768dbd2778'

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
                obj.json_out()
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
            try:
                value['project_uid'] = project_uid
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

            # print(f"{value['autoplace_specification'].keys()}")
            # for k, v  in value['autoplace_specification'].items():
            #     if isinstance(v, dict):
            #         print(f"K: [{k}], TYPE: [{type(v)}]")
            #         for k2, v2 in v.items():
            #             if isinstance(v2, dict):
            #                 print(f"K2: [{k2}], TYPE: [{type(v2)}]")
            #             elif isinstance(v2, list):
            #                 print(f"K2: [{k2}], LEN: [{len(v2)}]")
            #             else:
            #                 print(f"K2: [{k2}], V2: [{v2}]")
            #             # print(f"K2: [{k2}], V2: [{type(v2)}]")
            #     # else:
            #     #     print(f"K: [{k}], V: [{v}]")
            # exit()


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







def find_item_by_name(name: str, item_objects: List[FactorioDataItem]) -> FactorioDataItem:
    for index, item in enumerate(item_objects):
        if item.name == name:
            return index, item

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

# Set up a value uid

for item in item_objects:
    # Mock Post
    item.notes = f"Uploaded from script."
    payload = item.return_resource()
    item.resource_uid = 'GPC_RESOURCE_UID'

    uploaded_resources.append(item)
    # print(json.dumps(item.json_out(), indent=4))
    # print(json.dumps(item.return_resource(), indent=4))
    # break

for item in resource_objects:
    # Mock Post
    item.notes = f"Uploaded from script."
    for product in item.mineable_properties.products:
        index, resource_obj = find_item_by_name(product.name, item_objects)
        item.produce_uids[resource_obj.resource_uid] = product.amount / product.probability
        if product.type == 'fluid':
            item.machine_uid = 'GPC_FLUID_MACHINE_UID'
        elif product.type == 'item':
            item.machine_uid = 'GPC_ITEM_MACHINE_UID'
        else:
            print('NOT MAPPED ITEM!!')
            exit()
    payload = item.return_process()
    item.process_uid = 'GPC_PROCESS_UID'
    uploaded_processes.append(item)

    # print(json.dumps(item.return_process(), indent=4))
    # break

for item in recipe_objects:
    # Mock Post
    # item.notes = f"Uploaded from script."
    # # Consumes
    # if item.ingredients:
    #     for ingredient in item.ingredients:
    #         if ingredient.amount is None:
    #             continue
    #         index, resource_obj = find_item_by_name(ingredient.name, item_objects)
    #         probability = ingredient.probability if ingredient.probability else 1
    #         item.consume_uids[resource_obj.resource_uid] = ingredient.amount / probability
    # # Produces
    # if item.products:
    #     for product in item.products:
    #         if product.amount is None:
    #             continue
    #         index, resource_obj = find_item_by_name(product.name, item_objects)
    #         probability = product.probability if product.probability else 1
    #         item.produce_uids[resource_obj.resource_uid] = product.amount / probability



    # print(json.dumps(item.json_out(), indent=4))
    # print(json.dumps(item.return_process(), indent=4))
    machines = find_machine_by_crafting_category(item.category, machine_objects)
    for machine in machines:
        item.notes = f"Uploaded from script."
        # print(json.dumps(machine.json_out(), indent=4))
        # new_item = FactorioDataRecipe.model_validate(item)
        new_item = deepcopy(item)
        new_item.name = f"{item.name}::{machine.name}"
        new_item.notes += f" For machine [{machine.name}]"
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
                index, resource_obj = find_item_by_name(ingredient.name, item_objects)
                probability = ingredient.probability if ingredient.probability else 1
                general_amount = ingredient.amount / probability
                general_speed = 1 / machine.crafting_speed
                new_item.consume_uids[resource_obj.resource_uid] = general_amount
                new_item.process_time_seconds = general_speed
        # Produces
        if new_item.products:
            for product in new_item.products:
                if product.amount is None:
                    continue
                index, resource_obj = find_item_by_name(product.name, item_objects)
                probability = product.probability if product.probability else 1
                general_amount = product.amount / probability
                general_speed = 1 / machine.crafting_speed
                new_item.produce_uids[resource_obj.resource_uid] = general_amount
                new_item.process_time_seconds = general_speed
        uploaded_processes.append(new_item)

print(f"uploaded_resources: [{len(uploaded_resources)}]")
print(f"uploaded_processes: [{len(uploaded_processes)}]")

