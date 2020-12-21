import ruamel.yaml as yaml
import toml
import collections
import sys


def flatten_list(l: list):
    for el in l:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten_list(el)
        else:
            yield el


def unique_list(l: list):
    return list(set(list(flatten_list(l))))


def load_file(src: str):
    with open(src, 'r', encoding='utf-8') as f:
        result = yaml.safe_load(f)
    return result


with open('./i18n-generator/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)

with open(config['i18n']['path'], 'r', encoding='utf-8') as f:
    translations: dict = toml.load(f)

i18n_keys: list = [
    j[key]
    for i in config['fetch']
    for j in load_file(i['path'])
    for key in i['key']
    if j[key] is not None
]

for i in unique_list(i18n_keys):
    i18n_values: dict = {
        'other': {
            j: i
            for j in config['i18n']['language']
        }
    }

    translations.setdefault('patients-' + i, i18n_values)

with open(config['i18n']['path'], 'w', encoding='utf-8', newline='\n') as f:
    toml.dump(translations, f)
