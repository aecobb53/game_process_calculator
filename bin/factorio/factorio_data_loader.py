import os
import json
import re

from factorio_data_objects import FactorioDataItem, FactorioDataMachine, FactorioDataInfrastructure, FactorioDataResource, FactorioDataRecipe

factorio_recipie_lister_path = '/mnt/c/Users/aecob/AppData/Roaming/Factorio/script-output/recipe-lister'
# print(os.path.exists(factorio_recipie_lister_path))
# for i in os.listdir(factorio_recipie_lister_path):
#     print(i)


# ITEMS
item_file_list = [
    'item.json',
    'fluid.json',
]
for fl in item_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        item = json.load(f)
        index = 0
        for key, value in item.items():
            if key in ['fluid-unknown']:
                continue
            value['filename'] = fl
            try:
                a = FactorioDataItem.model_validate(value)
            except Exception as e:
                print(f"Error: {e}")
                print('ITEM')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
            # a.json_out()


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
for fl in machine_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                a = FactorioDataMachine.model_validate(value)
            except Exception as e:
                print(f"Error: {e}")
                print('MACHINE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
            # a.json_out()


# INFRASTRUCTURE
machine_file_list = [
    'inserter.json',
    'transport-belt.json',
]
for fl in machine_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                a = FactorioDataInfrastructure.model_validate(value)
            except Exception as e:
                print(f"Error: {e}")
                print('INFRASTRUCTURE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
            # a.json_out()


# RESOURCE
machine_file_list = [
    'resource.json',
]
for fl in machine_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                a = FactorioDataResource.model_validate(value)
            except Exception as e:
                print(f"Error: {e}")
                print('RESOURCE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(list(value.keys()), indent=4)}")
                # print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
            # a.json_out()


# RECIPE
machine_file_list = [
    'recipe.json',
]
for fl in machine_file_list:
    with open(os.path.join(factorio_recipie_lister_path, fl), 'r') as f:
        machine = json.load(f)
        index = 0
        for key, value in machine.items():
            value['filename'] = fl
            try:
                a = FactorioDataRecipe.model_validate(value)
            except Exception as e:
                print(f"Error: {e}")
                print('RECIPE')
                print(f"File: {fl}")
                print(f"Key: {key}")
                print(f"Value: {json.dumps(value, indent=4)}")
                print(f"Index: {index}")
                break
            index += 1
            # a.json_out()

