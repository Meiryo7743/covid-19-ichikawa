import csv
import os
import pandas as pd
import requests
import sys
import toml

with open('./data-updater/patients/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)['fetch']

res = requests.get(config['src'])

if res.status_code == 200:
    dfs = pd.read_html(res.url)

    for i in config['table']:
        dfs[i['index']].to_csv(
            i['dst'],
            index=False,
            header=False
        )
else:
    print('Error: the status code is ' + str(res.status_code) + '.')
    sys.exit()
