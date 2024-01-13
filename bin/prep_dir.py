import json
import re
import os

input_dir = '/home/acobb/git/game_process_calculator/game_process_calculator/models'

init = []
test_cmds = []

for root, dirs, files, in os.walk(input_dir):
    for fl in files:
        if fl.endswith('.py'):
            print(fl)
            with open(os.path.join(root, fl), 'r') as f:
                content = [l[:-1] for l in f.readlines()]
            # print(content)
            for cont in content:
                match = re.search(r'class (\w+)\(BaseModel\):', cont)
                if match:
                    print(match.group(1))
                    class_name = match.group(1)
                    init.append(f"from .{fl[:-3]} import {class_name}")

print(json.dumps(init, indent=4))
print(json.dumps(test_cmds, indent=4))
