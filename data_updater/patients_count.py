import json
import pandas as pd
import ruamel.yaml as yaml

with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['patients']

dst = config['dst']

for i in config['data']:
    with open(dst + i['data_details'], 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

    age = pd.DataFrame(raw)['年代']
    dict = {}

    # Count patients by age
    for j in config['formats']['keys']['age']:
        count_by_age = (age == j['find'])
        dict[j['replace']] = int(count_by_age.sum())

    # Count total patients
    dict['total'] = int(age.value_counts().sum())

    # Convert the data to list type so that Hugo can process them
    data = [dict]

    with open(dst + i['data_count'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(data, f, indent=2, allow_unicode=True)
