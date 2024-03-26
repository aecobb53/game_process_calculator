"""
This url has the source code

Items
https://satisfactory.wiki.gg/wiki/Template:DocsItems.json?action=edit

Processes
https://satisfactory.wiki.gg/wiki/Template:DocsRecipes.json?action=edit

"""

import json
import os
from re import S
from unicodedata import name
import requests

from pydantic import BaseModel
from typing import Union, List, Dict, Optional

import sys
sys.path.append('game_process_calculator/utils')
from utils import Utils

# Utils.convert_to_camel()

class SatisfactoryItem(BaseModel):
    class_name: str
    name: str
    description: str
    unlocked_by: str
    stack_size: int
    energy: int
    radioactive: float
    can_be_discarded: bool
    sink_points: int
    abbreviation: Union[str, None]
    form: str
    fluid_color: str
    stable: bool
    experimental: bool

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = {utils.convert_to_snake(k): v for k, v in dct.items()}
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = {utils.convert_to_camel(k): v for k, v in self.dict().items()}
        return content

    def format_resp_payload(self):
        content = {
            'name': self.name,
            # 'name': self.class_name,
            'project_uid': project_uid,
            'metadata': self.put(),
        }
        return content

class SatisfactoryRecipe(BaseModel):
    class_name: str
    name: str
    unlocked_by: str
    duration: int
    ingredients: List
    products: List
    produced_in: List
    in_craft_bench: bool
    in_workshop: bool
    in_build_gun: bool
    in_customizer: bool
    manual_crafting_multiplier: float
    alternate: bool
    min_power: Union[int, None]
    max_power: Union[int, None]
    seasons: List
    stable: bool
    experimental: bool

    @classmethod
    def build(cls, dct):
        utils = Utils()
        content = {utils.convert_to_snake(k): v for k, v in dct.items()}
        obj = cls(**content)
        return obj

    def put(self):
        utils = Utils()
        content = {utils.convert_to_camel(k): v for k, v in self.dict().items()}
        return content

    def format_resp_payload(self):
        consume_uids = {}
        for ingredient in self.ingredients:
            item_data = items_data_dict[ingredient['item']]
            consume_uids[item_data['resp']['uid']] = ingredient['amount']

        produce_uids = {}
        for product in self.products:
            if product['item'] == 'Desc_BlueprintDesigner_C':
                continue
            item_data = items_data_dict[product['item']]
            produce_uids[item_data['resp']['uid']] =product['amount']

        process_time_seconds = self.duration

        content = {
            'name': self.name,
            # 'name': self.class_name,
            'project_uid': project_uid,
            'metadata': self.put(),
            'consume_uids': consume_uids,
            'produce_uids': produce_uids,
            'process_time_seconds': process_time_seconds,
        }
        return content


class SatisfactoryWorkflow(BaseModel):
    name: str
    project_uid: str
    process_type: Optional[str] = 'LINEAR'
    process_uids: List[str]
    focus_resource_uids: List[str]

    @classmethod
    def build(cls, dct):
        obj = cls(**dct)
        return obj

    # def put(self):
    #     utils = Utils()
    #     content = {utils.convert_to_camel(k): v for k, v in self.dict().items()}
    #     return content

    def format_resp_payload(self):
        content = {
            'name': self.name,
            'project_uid': self.project_uid,
            'process_type': self.process_type,
            'process_uids': self.process_uids,
            'focus_resource_uids': self.focus_resource_uids,
        }
        return content

# with open('/home/acobb/git/game_process_calculator/bin/data/satisfactory_source_recipes.json', 'r') as jf:
#     data = json.load(jf)
# for i in data.keys():
#     j = data[i][0]
#     if 'Wall' in i:
#         print(json.dumps(j, indent=4))
#     # if j['seasons']:
#     #     print(json.dumps(j, indent=4))
# exit()

project_name = 'Satisfactory'
# Create project if it doesnt already exist
docker_url = 'http://0.0.0.0'
port = '8203'
base_url = docker_url + ':' + port


"""
For testing clear the db
"""
resp = requests.post(f"{base_url}/clear-test-data")


project_payload = {
    'name': project_name,
}
resp = requests.post(f"{base_url}/projects", json=project_payload)
if resp.status_code == 201:
    project = resp.json()
elif resp.status_code == 409:
    resp = requests.get(f"{base_url}/projects", params=project_payload)
    project = resp.json()['projects'][0]
else:
    print(f"Error creating project: {resp.status_code}")
    print(resp.json())
    assert resp.ok
project_uid = project['uid']

# Items
items_data_dict = {}
with open('/home/acobb/git/game_process_calculator/bin/data/satisfactory_source_items.json', 'r') as jf:
    data = json.load(jf)
for index, item_class_name in enumerate(data.keys()):
    print(f"{index}: {item_class_name}")
    item_l = data[item_class_name]
    if len(item_l) != 1:
        print('ITS NOT LENGTH 1')
    item_dict = item_l[0]
    item = SatisfactoryItem.build(item_dict)
    # print(json.dumps(item.format_resp_payload(), indent=4))
    resp = requests.post(f"{base_url}/resources", json=item.format_resp_payload())
    if resp.status_code == 201:
        print(f"Recipe {item.name} created")
    elif resp.status_code == 409:
        print('')
        print('')
        print(f"Recipe {item.name} already exists")
        print(json.dumps(item_l[0], indent=4))
        print(json.dumps(item.format_resp_payload(), indent=4))
        resp_dupe = requests.get(f"{base_url}/resources", params={'name': item.name})
        print(resp_dupe.status_code)
        print(json.dumps(resp_dupe.json(), indent=4))
        exit()
    else:
        print(f"Error creating item: {resp.status_code}")
        print(resp.json())
        exit()
    items_data_dict[item_class_name] = {
        'metadata': item_dict,
        'resp': resp.json(),
    }

# focus = list(items_data_dict.keys())[0]
# print(json.dumps(items_data_dict, indent=4))


# Recipes
recipies_data_dict = {}
with open('/home/acobb/git/game_process_calculator/bin/data/satisfactory_source_recipes.json', 'r') as jf:
    data = json.load(jf)
for index, recipe_class_name in enumerate(data.keys()):
    print(f"{index}: {recipe_class_name}")
    recipe_l = data[recipe_class_name]
    if len(recipe_l) != 1:
        print('ITS NOT LENGTH 1')
    recipe_dict = recipe_l[0]
    if not any([recipe_dict['inCraftBench'], recipe_dict['inWorkshop']]):
        """
        These seem to be things in the game but not items you can craft so we want to skip them
        """
        continue
    recipe = SatisfactoryRecipe.build(recipe_dict)
    resp = requests.post(f"{base_url}/processes", json=recipe.format_resp_payload())
    if resp.status_code == 201:
        print(f"Recipe {recipe.name} created")
    elif resp.status_code == 409:
        print('')
        print('')
        print(f"Recipe {recipe.name} already exists")
        print(json.dumps(recipe_l[0], indent=4))
        print(json.dumps(recipe.format_resp_payload(), indent=4))
        resp_dupe = requests.get(f"{base_url}/processes", params={'name': recipe.name})
        print(resp_dupe.status_code)
        print(json.dumps(resp_dupe.json(), indent=4))
        break
    else:
        print(f"Error creating recipe: {resp.status_code}")
        print(resp.json())
        break
    recipies_data_dict[item_class_name] = {
        'metadata': recipe_dict,
        'resp': resp.json(),
    }

# Export and save the data
export_resp1 = requests.get(f"{base_url}/export-projects")
export_resp2 = requests.get(f"{base_url}/export-resources")
export_resp3 = requests.get(f"{base_url}/export-processes")

assert export_resp2.status_code == 200
assert export_resp3.status_code == 200

resources_export_path = '/home/acobb/git/game_process_calculator/bin/data/satisfactory_db_resources_export.json'
resources_export_details = export_resp2.json()
with open(resources_export_path, 'w') as jf:
    jf.write(json.dumps(resources_export_details, indent=4))

processes_export_path = '/home/acobb/git/game_process_calculator/bin/data/satisfactory_db_processes_export.json'
processes_export_details = export_resp3.json()
with open(processes_export_path, 'w') as jf:
    jf.write(json.dumps(processes_export_details, indent=4))


workflow_list = [
    'Iron Rod',
    'Iron Plate',
    'Wire',
    'Cable',
    'Concrete',
    'Screw',
    'Rotor',
    'Reinforced Iron Plate',
    'Modular Frame',
    'Steel Beam',
    'Copper Sheet',
    'Encased Industrial Beam',
    'Steel Pipe',
    'Motor',
    'Plastic',
    'Rubber',
    'Heavy Modular Frame',
    'Fabric',
    'Computer',
    'Packaged Fuel',
    'Alclad Aluminum Sheet',
    'Radio Control Unit',
    'Gas Filter',
    'Supercomputer',
    'Aluminum Casing',
    'Fused Modular Frame',
    'Electromagnetic Control Rod',
    'Cooling System',
    'Turbo Motor',
]

def find_resource(name=None, uid=None):
    if name is not None:
        for resource in resources_export_details['resources']:
            if name == resource['name']:
                return resource
    elif uid is not None:
        for resource in resources_export_details['resources']:
            if uid == resource['uid']:
                return resource

def find_process(name=None, uid=None, resource_uid=None):
    if name is not None:
        for process in processes_export_details['processes']:
            if name == process['name']:
                return process
    elif uid is not None:
        for process in processes_export_details['processes']:
            if uid == process['uid']:
                return process
    elif resource_uid is not None:
        for process in processes_export_details['processes']:
            if resource_uid in process['produce_uids']:
                return process

def find_components(name=None, uid=None):
    recursive = []
    if name:
        resource = find_resource(name=name)
        process = find_process(name=name)
        if process is not None:
            if process['consume_uids']:
                for consume_uid in process['consume_uids']:
                    recursive.append(find_components(uid=consume_uid))
    elif uid:
        resource = find_resource(uid=uid)
        process = find_process(resource_uid=resource['uid'])
        if process is not None:
            if process['consume_uids']:
                for consume_uid in process['consume_uids']:
                    recursive.append(find_components(uid=consume_uid))
    return {
        'resource': resource,
        'process': process,
        'recursive': recursive,
    }

def compile_process_list(components_dict):
    process_list = []
    if components_dict['recursive']:
        for recursive in components_dict['recursive']:
            process_list.extend(compile_process_list(recursive))
    if components_dict['process']:
        process_list.append(components_dict['process']['uid'])
    return process_list


for workflow_name in workflow_list:
    print(f"Workflow: {workflow_name}")
    component_recursive_dict = find_components(name=workflow_name)

    # print(json.dumps(component_recursive_dict, indent=4))
    with open('/home/acobb/deleteme.json', 'w') as jf:
        jf.write(json.dumps(component_recursive_dict, indent=4))


    if all([component_recursive_dict['process'] is None,
            component_recursive_dict['resource'] is None]):
        print('MISSING PROCESS. Is it misspelled?')
        break
    if component_recursive_dict['process'] is None:
        """Its a raw resource"""
        continue

    process_list = compile_process_list(component_recursive_dict)
    # print(json.dumps(process_list, indent=4))
    workflow = SatisfactoryWorkflow(
        name=workflow_name,
        project_uid=project_uid,
        process_uids=process_list,
        focus_resource_uids=[component_recursive_dict['resource']['uid']])
    resp = requests.post(f"{base_url}/workflows", json=workflow.format_resp_payload())

export_resp4 = requests.get(f"{base_url}/export-workflows")
assert export_resp4.status_code == 200
processes_export_path = '/home/acobb/git/game_process_calculator/bin/data/satisfactory_db_workflow_export.json'
processes_export_details = export_resp4.json()
with open(processes_export_path, 'w') as jf:
    jf.write(json.dumps(processes_export_details, indent=4))


# Download html
params = {
    'name': 'Turbo Motor',
    'units_per_second': 17.0,
}
resp = requests.get(f"{base_url}/html/visualize-workflows", params=params)
assert resp.status_code == 200
html_path = '/home/acobb/git/game_process_calculator/bin/data/focus_file.html'
with open(html_path, 'w') as hf:
    hf.write(resp.text)

