from dateutil.relativedelta import relativedelta
import csv
import datetime
import json
import pandas as pd
import re
import ruamel.yaml as yaml


def format_value(value, format_config):
    for i in format_config:
        result = re.sub(
            i['find'],
            i['replace'],
            str(value) if format_config.index(i) == 0 else result
        )
    if result == '':
        return None
    else:
        return result


def format_number(value, format_config):
    result = format_value(value, format_config)
    if not result == None:
        return int(result)


def format_date(value, format_config):
    result = format_value(value, format_config)
    if not result == None:
        result = datetime.datetime.strptime(
            result,
            '%Y-%m-%d'
        )
        return result.strftime('%Y-%m-%d')


def format_list(value, format_config):
    result = format_value(value, format_config)
    if not result == None:
        return result.split(',')


with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['patients']

dst = config['dst']

data = config['data']
for i in data:
    data_dict = []

    raw = pd.read_table(dst + i['raw'], header=0)
    data_json = json.loads(raw.to_json(orient='records'))
    for j in data_json:
        value_ichikawa = format_number(
            j.get('市内'),
            config['formats']['values']['ichikawa']
        )

        value_chiba = format_number(
            j.get('県内'),
            config['formats']['values']['chiba']
        )

        value_inspection_date = format_date(
            j.get('検査確定日'),
            config['formats']['values']['inspection_date']
        )

        value_onset_date = format_date(
            j.get('発症日'),
            config['formats']['values']['onset_date']
        )

        value_age = format_value(
            j.get('年代'),
            config['formats']['values']['age']
        )

        value_sex = format_value(
            j.get('性別'),
            config['formats']['values']['sex']
        )

        value_occupation = format_value(
            j.get('職業'),
            config['formats']['values']['occupation']
        )

        value_infection_sources = format_list(
            j.get('推定感染経路'),
            config['formats']['values']['infection_sources']
        )

        if '行動歴＊' in j:
            value_activities = format_list(
                j.get('行動歴＊'),
                config['formats']['values']['activities']
            )
        elif '行動歴' in j:
            value_activities = format_list(
                j.get('行動歴'),
                config['formats']['values']['activities']
            )

        dict = {
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
        data_dict.append(dict)

    with open(dst + i['data_details'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(data_dict, f, indent=2, allow_unicode=True)
