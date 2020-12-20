import json
import os
import ruamel.yaml as yaml
import collections


def flatten(l: list):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def get_unique_list(l: list):
    return list(set(list(flatten(l))))


def get_data(src: str):
    extension = os.path.splitext(src)[1]

    if extension == '.json':
        with open(src, 'r', encoding='utf-8') as f:
            result = json.load(f)
    elif extension == '.yaml':
        with open(src, 'r', encoding='utf-8') as f:
            result = yaml.safe_load(f)
    else:
        print('Error: unexpected file.')

    return result


def get_default_keys(value: dict, language: str):
    return {
        i: dict(value[i][language].items())
        for i in value
    }


with open('./i18n-generator/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

raw: list = [
    j[key]
    for i in config['fetch']
    for j in get_data(i['path'])
    for key in i['keys']
    if j[key] is not None
]

data_dict: dict = {
    'patients-' + i: {
        'other': i
    }
    for i in get_unique_list(raw)
}

with open(config['default']['path'], 'r', encoding='utf-8') as f:
    content: dict = yaml.safe_load(f)

for i in config['language']:
    get_language: dict = get_default_keys(content, i)

    for key in data_dict:
        get_language.setdefault(key, data_dict[key])

    with open('./i18n-generator/' + i + '.yaml', 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(get_language, f, indent=2, allow_unicode=True)
