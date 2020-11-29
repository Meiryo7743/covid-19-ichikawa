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
        key_inspection_date = re.sub(
            r'^不明|調査中|\s+|None$',
            r'',
            str(j.get('検査確定日'))
        )
        key_inspection_date = re.sub(
            r'(\d+)月(\d+)日',
            r'2020-\1-\2',
            key_inspection_date
        )
        if key_inspection_date == '':
            key_inspection_date = None
        else:
            key_inspection_date = datetime.datetime.strptime(
                key_inspection_date,
                '%Y-%m-%d'
            )
            key_inspection_date = key_inspection_date.strftime('%Y-%m-%d')

            # 発症日
        key_onset_date = re.sub(
            r'^不明|調査中|\s+|None$',
            r'',
            str(j.get('発症日'))
        )
        key_onset_date = re.sub(
            r'(\d+)月(\d+)日',
            r'2020-\1-\2',
            key_onset_date
        )
        if key_onset_date == '':
            key_onset_date = None
        else:
            key_onset_date = datetime.datetime.strptime(
                key_onset_date,
                '%Y-%m-%d'
            )
            key_onset_date = key_onset_date.strftime('%Y-%m-%d')

        # 年代
        key_age = re.sub(
            r'^不明|調査中|\s+|None$',
            r'',
            str(j.get('年代'))
        )
        if key_age == '':
            key_age = None

        # 性別
        key_sex = str(j.get('性別'))

        # 職業
        key_occupation = re.sub(
            r'^不明|調査中|\s+|None$',
            r'',
            str(j.get('職業'))
        )
        if key_occupation == '':
            key_occupation = None

        # 推定感染経路
        key_infection_sources = re.sub(
            r'^不明|調査中|\s+|None$',
            r'',
            str(j.get('推定感染経路'))
        )
        key_infection_sources = re.sub(
            r'(.)接触',
            r'\1',
            key_infection_sources
        )
        key_infection_sources = re.sub(
            r'、',
            r',',
            key_infection_sources
        )
        if key_infection_sources == '':
            key_infection_sources = None
        else:
            key_infection_sources = key_infection_sources.split(',')

        # 行動歴
        if '行動歴＊' in j:
            key_activities = re.sub(
                r'^不明|調査中|\s+|None$',
                r'',
                str(j.get('行動歴＊'))
            )
        elif '行動歴' in j:
            key_activities = re.sub(
                r'^不明|調査中|\s+|None$',
                r'',
                str(j.get('行動歴'))
            )
        key_activities = re.sub(
            r'、',
            r',',
            key_activities
        )
        if key_activities == '':
            key_activities = None
        else:
            key_activities = key_activities.split(',')

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
