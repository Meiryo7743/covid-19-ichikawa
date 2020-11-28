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

list = []

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

    date = date_left + '~' + date_right

    list.append([date, i['data'][0], i['data'][1], i['data'][2]])

dict = {
    'data': {
        'headers': [
            {'type': 'string', 'name': 'Durations'},
            {'type': 'number', 'name': '6:30~7:30'},
            {'type': 'number', 'name': '7:30~9:30'},
            {'type': 'number', 'name': '9:30~10:30'}
        ],
        'rows': list,
    },
    'options': {
        'backgroundColor': {
            'fill': 'none'
        },
        'chartArea': {
            'bottom': 14 * 6,
            'left': 14 * 4,
            'right': 14 * 4,
            'top': 14 * 2
        },
        'color': '#84919e',
        'fontName': 'sans-serif',
        'fontSize': 14,
        'hAxes': [
            {
                'slantedText': True,
                'slantedTextAngle': 45,
                'textStyle': {'color': '#84919e'}
            }
        ],
        'legend': {
            'alignment': 'end',
            'position': 'top',
            'textStyle': {'color': '#84919e'}
        },
        'series': {
            '0': {
                'targetAxisIndex': 0
            },
            '1': {
                'targetAxisIndex': 1
            }
        },
        'vAxes': [
            {
                'baseline': 0,
                'baselineColor': '#84919e',
                'format': "#'%'",
                'gridlines': {'color': '#84919e'},
                'maxValue': 20,
                'minorGridlines': {'color': 'none'},
                'minValue': -100,
                'textStyle': {'color': '#84919e'}
            },
            {
                'baseline': 0,
                'baselineColor': '#84919e',
                'format': "#'%'",
                'gridlines': {'color': '#84919e'},
                'maxValue': 20,
                'minorGridlines': {'color': 'none'},
                'minValue': -100,
                'textStyle': {'color': '#84919e'}
            }
        ],
        'width': len(list) * 3 * 14
    }
}

with open(dst + data['data_passengers'], 'w', newline='\n') as f:
    json.dump(dict, f, indent=2)
