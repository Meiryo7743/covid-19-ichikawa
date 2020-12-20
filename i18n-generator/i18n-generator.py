import json
import os
import ruamel.yaml as yaml
import collections


def get_default_keys(d: dict, language: str):
    return {
        i: dict(d[i][language].items())
        for i in d
    }


def get_flatten_list(l: list):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from get_flatten_list(el)
        else:
            yield el


def get_unique_list(l: list):
    return list(set(list(get_flatten_list(l))))


def load_file(src: str):
    extension = os.path.splitext(src)[1]

    with open(src, 'r', encoding='utf-8') as f:
        if extension == '.json':
            result = json.load(f)
        elif extension == '.yaml':
            result = yaml.safe_load(f)

    return result


config: dict = load_file('./i18n-generator/config.yaml')

if not (os.path.isdir(config['i18n_dir'])):
    os.mkdir(config['i18n_dir'])

raw: list = [
    j[key]
    for i in config['fetch']
    for j in load_file(i['path'])
    for key in i['keys']
    if j[key] is not None
]

data_dict: dict = {
    'patients-' + i: {
        'other': i
    }
    for i in get_unique_list(raw)
}

translations: dict = load_file(config['default']['path'])

for i in config['language']:
    get_language: dict = get_default_keys(translations, i)

    for key in data_dict:
        get_language.setdefault(key, data_dict[key])

    with open('./i18n/' + i + '.yaml', 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(get_language, f, allow_unicode=True)
