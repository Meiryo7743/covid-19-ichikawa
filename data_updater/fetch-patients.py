import csv
import json
import os
import pandas as pd
import requests
import sys

with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['patients']

dst = config['dst']

if not (os.path.isdir(dst)):
    os.mkdir(dst)

res = requests.get(config['src'])
if res.status_code == 200:
    dfs = pd.read_html(res.url)
else:
    sys.exit()

for i in config['data']:
    dfs[i['table_index']].to_csv(
        dst + i['raw'],
        sep='\t',
        index=False,
        header=False
    )
