from dateutil.relativedelta import relativedelta
import datetime
import json
import pandas as pd
import re
import ruamel.yaml as yaml
import toml


def format_str(value: str, replace_format: dict):
    for i, key in enumerate(replace_format):
        pattern = re.compile(key['find'])

        result: str = pattern.sub(
            key['replace'],
            str(value) if i == 0 else result
        )

    if result == 'None' or result == '':
        return None
    else:
        return result


def format_int(value: str, replace_format: dict):
    result = format_str(value, replace_format)

    if result is None:
        return None
    else:
        return int(result)


def format_date(value: str, replace_format: dict):
    result = format_str(value, replace_format)

    if result is None:
        return None
    else:
        if result == '不明':
            return result
        else:
            result = datetime.datetime.strptime(
                result,
                '%Y-%m-%d'
            )

        return result.strftime('%Y-%m-%d')


def format_list(value: str, replace_format: dict):
    result = format_str(value, replace_format)

    if result is None:
        return None
    else:
        return result.split(',')


with open('./data-updater/patients/config.toml', 'r', encoding='utf-8') as f:
    load_config: dict = toml.load(f)

    config: dict = load_config['get-details']

    replace: dict = load_config['replace-format']['value']

for i in config:
    dfs = pd.read_csv(i['src'], header=0)

    dfs_dict: dict = json.loads(dfs.to_json(orient='records'))

    details: list = [
        {
            '市内': len(dfs_dict) - index,
            '県内': format_int(
                j['県内'],
                replace['県内']
            ),
            '検査確定日':  format_date(
                j['検査確定日'],
                replace['検査確定日']
            ),
            '発症日': format_date(
                j.get('発症日'),
                replace['発症日']
            ),
            '年代': format_str(
                j['年代'],
                replace['年代']
            ),
            '性別': format_str(
                j['性別'],
                replace['性別']
            ),
            '職業': format_str(
                j['職業'],
                replace['職業']
            ),
            '推定感染経路': format_list(
                j['推定感染経路'],
                replace['推定感染経路']
            ),
            '行動歴': format_list(
                j['行動歴＊'],
                replace['行動歴']
            ) if '行動歴＊' in j
            else format_list(
                j['行動歴'],
                replace['行動歴']
            )
        }
        for index, j in enumerate(dfs_dict)
    ]

    with open(i['dst'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(details, f, allow_unicode=True)
