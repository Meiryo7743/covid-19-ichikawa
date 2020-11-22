import json
import os
import urllib.request
import requests
import sys

with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['subway'][0]

dst = config['dst']
data = config['data'][0]

if not (os.path.isdir(dst)):
    os.mkdir(dst)

res = requests.get(config['src'])
if res.status_code == 200:
    urllib.request.urlretrieve(res.url, dst + data['raw'])
else:
    sys.exit()
