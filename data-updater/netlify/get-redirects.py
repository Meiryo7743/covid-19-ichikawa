import toml
import sys

with open('./data-updater/netlify/config.toml', 'r', encoding='utf-8', newline='\n') as f:
    load_config: dict = toml.load(f)
    config: dict = load_config['get-redirects']

redirects: dict = {
    'redirects': [
        {
            'from': '/' + j + i['from'],
            'to': i['to'] if i['to'].startswith('http') else '/' + j + i['to'],
            'force': i.get('force'),
            'status': i.get('status'),
        }
        for i in config['redirect']
        for j in config['language']
    ]
}

with open(config['dst'], 'w', encoding='utf-8', newline='\n') as f:
    toml.dump(redirects, f)
