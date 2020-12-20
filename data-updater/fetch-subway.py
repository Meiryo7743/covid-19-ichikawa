import os
import urllib.request
import requests
import sys
import toml

with open('./data-updater/config.toml', 'r', encoding='utf-8') as f:
    config = toml.load(f)['subway']

dst = config['dst']

if not (os.path.isdir(dst)):
    os.mkdir(dst)

res = requests.get(config['src'])
if res.status_code == 200:
    data = config['data'][0]
    urllib.request.urlretrieve(res.url, dst + data['raw'])
else:
    sys.exit()
