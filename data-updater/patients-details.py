from dateutil.relativedelta import relativedelta
import csv
import datetime
import json
import pandas as pd
import re
import ruamel.yaml as yaml
import toml


def format_value(value, format):
    for i, key in enumerate(format):
        pattern = re.compile(key['find'])
        result = pattern.sub(
            key['replace'],
            str(value) if i == 0 else result
        )
    if result == '':
        return None
    else:
        return result


def format_number(value, format):
    result = format_value(value, format)
    if not result == None:
        return int(result)


def format_date(value, format):
    result = format_value(value, format)
    if not result == None:
        if result == '不明':
            return result
        else:
            result = datetime.datetime.strptime(
                result,
                '%Y-%m-%d'
            )
            return result.strftime('%Y-%m-%d')


def format_list(value, format):
    result = format_value(value, format)
    if not result == None:
        return result.split(',')


with open('./data-updater/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)['patients']

dst = config['dst']
format = config['formats']['values']

for i in config['data']:
    raw = pd.read_table(dst + i['raw'], header=0)

    data_list = []

    data_json = json.loads(raw.to_json(orient='records'))
    for j in data_json:
        value_ichikawa = format_number(
            j['市内'],
            format['ichikawa']
        )

        value_chiba = format_number(
            j['県内'],
            format['chiba']
        )

        value_inspection_date = format_date(
            j['検査確定日'],
            format['inspection_date']
        )

        value_onset_date = format_date(
            j.get('発症日'),
            format['onset_date']
        )

        value_age = format_value(
            j['年代'],
            format['age']
        )

        value_sex = format_value(
            j['性別'],
            format['sex']
        )

        value_occupation = format_value(
            j['職業'],
            format['occupation']
        )

        value_infection_sources = format_list(
            j['推定感染経路'],
            format['infection_sources']
        )

        if '行動歴＊' in j:
            value_activities = format_list(
                j['行動歴＊'],
                format['activities']
            )
        elif '行動歴' in j:
            value_activities = format_list(
                j['行動歴'],
                format['activities']
            )

        data_dict = {
            '市内': value_ichikawa,
            '県内': value_chiba,
            '検査確定日': value_inspection_date,
            '発症日': value_onset_date,
            '年代': value_age,
            '性別': value_sex,
            '職業': value_occupation,
            '推定感染経路': value_infection_sources,
            '行動歴': value_activities
        }

        data_list.append(data_dict)

    with open(dst + i['data_details'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(data_list, f, indent=2, allow_unicode=True)
