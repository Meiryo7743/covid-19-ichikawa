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
        # 市内
        key_ichikawa = format_number(
            j.get('市内'),
            config['formats']['values']['ichikawa']
        )

        # 県内
        key_chiba = format_number(
            j.get('県内'),
            config['formats']['values']['chiba']
        )

        # 検査確定日
        key_inspection_date = format_date(
            j.get('検査確定日'),
            config['formats']['values']['inspection_date']
        )

        # 発症日
        key_onset_date = format_date(
            j.get('発症日'),
            config['formats']['values']['onset_date']
        )

        # 年代
        key_age = format_value(
            j.get('年代'),
            config['formats']['values']['age']
        )

        # 性別
        key_sex = format_value(
            j.get('性別'),
            config['formats']['values']['sex']
        )

        # 職業
        key_occupation = format_value(
            j.get('職業'),
            config['formats']['values']['occupation']
        )

        # 推定感染経路
        key_infection_sources = format_list(
            j.get('推定感染経路'),
            config['formats']['values']['infection_sources']
        )

        # 行動歴
        if '行動歴＊' in j:
            key_activities = format_list(
                j.get('行動歴＊'),
                config['formats']['values']['activities']
            )
        elif '行動歴' in j:
            key_activities = format_list(
                j.get('行動歴'),
                config['formats']['values']['activities']
            )

        dict = {
            '市内': key_ichikawa,
            '県内': key_chiba,
            '検査確定日': key_inspection_date,
            '発症日': key_onset_date,
            '年代': key_age,
            '性別': key_sex,
            '職業': key_occupation,
            '推定感染経路': key_infection_sources,
            '行動歴': key_activities
        }
        data_dict.append(dict)

    with open(dst + i['data_details'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(data_dict, f, indent=2, allow_unicode=True)
