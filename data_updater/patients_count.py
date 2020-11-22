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

    age = pd.DataFrame(raw)['年代']
    dict = {}

    # Count patients by age
    key = config['age']
    for j in key:
        age_bool = (age == j['find'])
        dict[j['replace']] = int(age_bool.sum())

    # Count total patients
    dict['total'] = int(age.value_counts().sum())

    # Convert the data to list type so that Hugo can process them
    data_count = [dict]

    with open(dst + i['data_count'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(data_count, f, indent=2, allow_unicode=True)
