from dateutil.relativedelta import relativedelta
import datetime
import json
import re

with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['subway'][0]

dst = config['dst']
data = config['data'][0]

with open(dst + data['raw']) as f:
    data_json = json.load(f)['datasets']

labels = []
time_0630_0730 = []
time_0730_0930 = []
time_0930_1030 = []

for i in data_json:
    # Fix Date Format
    # MM/DD~DD -> 0MM/0DD~0DD
    date = re.sub(
        r'^(\d+)/(\d+)~(\d+)$',
        r'0\1/0\2~0\3',
        i['label']
    )
    # -> MM/DD~DD
    date = re.sub(
        r'0(\d\d)',
        r'\1',
        date
    )
    # -> MM-DD~DD
    date = re.sub(
        r'/',
        r'-',
        date
    )
    # -> MM-DD~MM-DD
    date = re.sub(
        r'^(\d\d-)(\d\d~)(\d\d)$',
        r'\1\2\1\3',
        date
    )
    # -> YYYY-MM-DD~YYYY-MM-DD
    date = re.sub(
        r'^(.+)~(.+)$',
        r'2020-\1~2020-\2',
        date
    )

    # Fix Month (Left > Right -> Left < Right)
    date_left = re.sub(
        r'^(.+)~.+$',
        r'\1',
        date
    )
    date_right = re.sub(
        r'^.+~(.+)$',
        r'\1',
        date
    )
    date_left = datetime.datetime.strptime(date_left, '%Y-%m-%d')
    date_right = datetime.datetime.strptime(date_right, '%Y-%m-%d')

    if date_left > date_right:
        date_right = date_right + relativedelta(months=1)

    date_left = date_left.strftime('%m-%d')
    date_right = date_right.strftime('%m-%d')

    date = date_left + "~" + date_right

    labels.append(date)
    time_0630_0730.append(i['data'][0])
    time_0730_0930.append(i['data'][1])
    time_0930_1030.append(i['data'][2])

dict = {
    'type': 'bar',
    'data': {
            'labels': labels,
            'datasets': [
                {
                    'label': '6:30~7:30',
                    'data': time_0630_0730,
                    'backgroundColor': '#c2d94c'
                },
                {
                    'label': '7:30~9:30',
                    'data': time_0730_0930,
                    'backgroundColor': '#03af7a'
                },
                {
                    'label': '9:30~10:30',
                    'data': time_0930_1030,
                    'backgroundColor': '#84dcb0'
                }
            ]
    },
    'options': {
        'scales': {
            'yAxes': [
                {'ticks': {'suggestedMax': 10, 'suggestedMin': 0, 'stepSize': 10}}
            ]
        }
    }
}

with open(dst + data['data_passengers'], 'w', newline='\n') as f:
    json.dump(dict, f, indent=2)
