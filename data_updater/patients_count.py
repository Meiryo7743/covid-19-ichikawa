import json
import pandas as pd
import ruamel.yaml as yaml

with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['patients'][0]

dst = config['dst']

data = config['data']
for i in data:
    with open(dst + i['data_details'], 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    age_sum = pd.DataFrame(raw)['年代']

    age_dict = {}

    # Count by age
    age = config['age']
    for j in age:
        age_bool = (age_sum == j['find'])
        age_dict[j['replace']] = int(age_bool.sum())

    # Count total
    age_dict['total'] = int(age_sum.value_counts().sum())

    with open(dst + i['data_count'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(age_dict, f, indent=2, allow_unicode=True)
