import urllib.request
import requests
import sys
import toml

with open('./data-updater/toei-subway/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)['fetch']

res = requests.get(config['src'])

if res.status_code == 200:
    urllib.request.urlretrieve(res.url, config['dst'])
else:
    print('Error: the status code is ' + str(res.status_code) + '.')
    sys.exit()
