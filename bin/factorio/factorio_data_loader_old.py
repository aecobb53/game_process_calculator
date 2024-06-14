import os
import json
import re

from factorio_data_objects import FactorioDataItem
# from bin.factorio.factorio_data_objects import FactorioDataItem

# from .factorio_data_objects import FactorioDataItem

factorio_data_path = '/mnt/d/Games/steamapps/common/Factorio/data/base/prototypes/'
# factorio_recipie_lister_path = 'C:\Users\aecob\AppData\Roaming\Factorio\script-output\recipe-lister'
factorio_recipie_lister_path = '/mnt/c/Users/aecob/AppData/Roaming/Factorio/script-output/recipe-lister'
print(os.path.exists(factorio_recipie_lister_path))
for i in os.listdir(factorio_recipie_lister_path):
    print(i)

'active_mods.json'
'assembling-machine.json'
'boiler.json'
'equipment-grid.json'
'equipment.json'
'fluid.json'
'furnace.json'
'generator.json'
'inserter.json'
'item.json'
'lab.json'
'mining-drill.json'
'projectile.json'
'reactor.json'
'recipe.json'
'resource.json'
'rocket-silo.json'
'solar-panel.json'
'technology.json'
'transport-belt.json'

with open(os.path.join(factorio_recipie_lister_path, 'item.json'), 'r') as f:
    items = json.load(f)
    index = 0
    for key, value in items.items():
        try:
            a = FactorioDataItem.model_validate(value)
        except Exception as e:
            print(f"Error: {e}")
            print(f"Key: {key}")
            print(f"Value: {value}")
            print(f"Index: {index}")
            break
        index += 1


exit()

def load_factorio_items():
    items = []

    # with open(os.path.join(factorio_data_path, 'item.lua'), 'r') as f:
    #     items = json.load(f)
    # return items

data_dict = {}

for root, dirs, files in os.walk(factorio_data_path):
    for fl in files:
        # if 'item.lua' not in fl:
        #     continue

        if fl not in [
            # 'achievements.lua',  # achievements.lua
            # 'ambient-sounds.lua',  # ambient-sounds.lua
            # 'autoplace-controls.lua',  # autoplace-controls.lua
            # 'custom-inputs.lua',  # custom-inputs.lua
            # 'damage-type.lua',  # damage-type.lua
            'ammo-category.lua',  # categories/ammo-category.lua
            'equipment-category.lua',  # categories/equipment-category.lua
            'fuel-category.lua',  # categories/fuel-category.lua
            'module-category.lua',  # categories/module-category.lua
            ## 'recipe-category.lua',  # categories/recipe-category.lua
            # 'resource-category.lua',  # categories/resource-category.lua
            # 'legacy-entities.lua',  # legacy/legacy-entities.lua
            # 'noise-layers.lua',  # tile/noise-layers.lua
        ]:
            continue
        path = os.path.join(root, fl)
        grab = False
        file_lines = []
        with open(path, 'r') as f:
            for line in f.readlines():
                # file_lines.append(line[:-1])
                file_lines.append(line.strip())
                if 'data:extend' in line:
                    grab = True
        if grab:
            data_dict[path] = []
            print(f"Working on file [{path}]")
            # print(path)
            # continue

            nested = []
            start_tracking = False
            start_index = None
            end_index = None
            file_monolith = ''.join(file_lines)
            i = 0
            """
            Gather data ranges between the brackets to focus on later
            """
            for _ in range(len(file_monolith)):
                if i >= len(file_monolith):
                    break

                c = file_monolith[i]
                data_extended_index_addition = 11
                if file_monolith[i:i+data_extended_index_addition] == 'data:extend':
                    start_tracking = True
                    i += data_extended_index_addition
                    start_index = i
                    nested = [file_monolith[i]]
                if start_tracking and c in ['[', '{', '(']:
                    nested.append(c)
                if start_tracking and c in [']', '}', ')']:
                    nested.pop(-1)
                if start_tracking and not nested:
                    end_index = i
                    break

                i += 1

            """
            Pull out the data between the brackets
            """
            # print(start_index, end_index)
            # print(file_monolith[start_index:end_index])
            content = file_monolith[start_index+1:end_index-1]  # Because its wrapped in '()'
            content = content[1:-1] # Back this out again
            # print(content)

            # def parse_kv(kv_string):
            #     kv = [kv.strip() for kv in kv_string.split('=')]
            #     if len(kv) == 1:
            #         return None, kv[0]
            #     elif len(kv) != 2:
            #         raise ValueError(f"Invalid key-value pair [{kv_string}]")
            #     key = kv[0]
            #     value = kv[1]
            #     return key, value

            # def aggregate_kv(kv_list):
            #     print('')
            #     print('')
            #     print(len(kv_list))
            #     for i in kv_list:
            #         print(i)

            def form_dict(kv_string):
                """
                Taking the expected format, take the dict in string format and return a dict
                """
                # print('')
                # print('')
                kv_list = kv_string.split(',')
                data = {}
                for i in kv_list:
                    kv = [kv for kv in i.split('=')]
                    # kv = [[j.stirp() for j in kv] for kv in i.split('=')]
                    key = kv[0].strip()
                    value = '='.join(kv[1:]).strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    data[key] = value
                # print(json.dumps(data, indent=4))
                return data

            def form_data_list(list_of_lists):
                """
                Designed to return a list of dicts and be use recursively to handle nested lists
                """
                print(len(list_of_lists))
                data_layers = []
                for index, row in enumerate(list_of_lists):
                    if len(row) > 1:
                        result = form_dict(row)
                        data_layers.append(result)
                    else:
                        print(f"-{row}-")
                return data_layers

            lst = []
            sublist = []
            collection = ''
            data_list = []
            for c in content:
                if c == '{':
                    lst.append(collection)
                    lst.append('{')
                    collection = ''
                    continue
                if c == '}':
                    lst.append(collection)
                    lst.append('}')
                    dct = form_dict(collection)
                    # a = form_dict(collection)
                    # print(a)
                    data_list.append(dct)
                    collection = ''
                    continue
                collection += c
            lst = [l for l in lst if l not in [',', '', ' ', '\n']]

            print(json.dumps(data_list, indent=4))
            data_dict[path] = data_list
# print(json.dumps(data_dict, indent=4))
# for i in data_dict.keys():
#     print(i)

            # exit()


            # nested_layer = []
            # data_layers = []

            # # for index, row in enumerate(lst):
            # #     # print('')
            # #     # print('')
            # #     if len(row) > 1:
            # #         result = form_dict(row)
            # #         data_layers.append(result)
            # #     else:
            # #         print(f"-{row}-")
            # #         # if row == '{':
            # #         #     nested_layer.append(row)
            # #         #     data_layers[-1].append([])
            # #         #     continue
            # #         # if row == '}':
            # #         #     nested_layer.pop(-1)
            # #         #     data_layers.append()
            # #         #     continue
            # data_layers = form_data_list(lst)
            # print(json.dumps(data_layers, indent=4))
            # exit()
            # #     # print(f"-{row[:100]}-")
            # #     row_l = row.split(',')
            # #     # print(f"-{row_l[:2]}-")
            # #     for item in row_l:
            # #         key, value = parse_kv(item)
            # #         # print('')
            # #         # print(item)
            # #         # print(f"KEY: [{key}] VALUE: [{value}]")
            # #         if key:
            # #             pair = {key: value}
            # #             # print(pair, len(nested_layer))
            # #             aggregate_indexes.append(index)
            # #         elif value == '{':
            # #             nested_layer.append(value)
            # #             # print(nested_layer)
            # #         elif value == '}':
            # #             nested_layer.pop(-1)
            # #             aggregate_start_index = aggregate_indexes.pop(-1)
            # #             aggregate_stop_index = index
            # #             # print(nested_layer)
            # #             aggregate_kv(lst[aggregate_start_index:aggregate_stop_index])
            # #             sublist = []
            # #         else:
            # #             print(f"Invalid key-value pair [{item}]")
            # #             sublist.append(item)
            # #             # raise ValueError(f"Invalid key-value pair [{item}]")
            # # # print(content.split('{'))
            # # exit()  



            # # nested_layer = []
            # # string_layer = []
            # # i = 0
            # # # for _ in range(len(content)):

            # # for _ in range(250):
            # #     if i >= len(content):
            # #         break

            # #     c = content[i]
            # #     print(i, c, nested_layer, string_layer)
            # #     if c in ['[', '{', '('] and not string_layer:
            # #         nested_layer.append(c)
            # #     if c in [']', '}', ')'] and not string_layer:
            # #         nested_layer.pop(-1)

            # #     if c == '"' or c == "'":
            # #         if string_layer and (string_layer[-1] == c):
            # #             string_layer.pop(-1)
            # #         else:
            # #             string_layer.append(c)
                    
                

            # #     # if nested_layer == 0 and c == ',':
            # #     #     print(i)

            # #     i += 1
            # # exit()
            # # # for _ in range(len(file_monolith)):
            # # #     if i >= len(file_monolith):
            # # #         break
            # # #     c = file_monolith[i]
            # # #     if file_monolith[i:i+11] == 'data:extend':
            # # #         print(f"found on index {i}")
            # # #         start_tracking = True
            # # #         start_index = i
            # # #         i = i + 10
            # # #         nested = [file_monolith[i]]
            # # #     if start_tracking and c in ['[', '{', '(']:
            # # #         nested.append(c)
            # # #     if start_tracking and c in [']', '}', ')']:
            # # #         nested.pop(-1)
            # # #     if start_tracking and not nested:
            # # #         print(f"end on index {i}")
            # # #         end_index = i
            # # #         break
            # # #     i += 1
            # # # print(start_index, end_index)
            # # # print(file_monolith[start_index:end_index])
            
                
            # # # for line in file_lines:
            # # #     if 'data:extend' in line:
            # # #         nested = True
            # # #         print(line)

            # #     # if 'data' in line:
            # #     #     if 'data:extend' in line:
            # #     #         continue
            # #     #     match = re.search(r'[_-]data', line)
            # #     #     if match:
            # #     #         continue
            # #     #     match = re.search(r'data\.', line)
            # #     #     if match:
            # #     #         continue
            # #     #     print('')
            # #     #     print(path)
            # #     #     print(line)
