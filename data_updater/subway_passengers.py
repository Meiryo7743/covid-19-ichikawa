from dateutil.relativedelta import relativedelta
import datetime
import json
import re


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


with open('./data_updater/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)['subway']

dst = config['dst']
data = config['data'][0]

with open(dst + data['raw']) as f:
    data_json = json.load(f)['datasets']

format = config['formats']['values']

list = []

for i in data_json:
    date = format_value(
        i['label'],
        format['label']
    )

    date_former = datetime.datetime.strptime(
        date.split('~')[0],
        '%Y-%m-%d'
    )
    date_latter = datetime.datetime.strptime(
        date.split('~')[1],
        '%Y-%m-%d'
    )

    if date_former > date_latter:
        date_latter = date_latter + relativedelta(months=1)

    date_former = date_former.strftime('%m-%d')
    date_latter = date_latter.strftime('%m-%d')

    date = date_former + '~' + date_latter

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

with open(dst + data['data_passengers'], 'w', encoding='utf-8', newline='\n') as f:
    json.dump(dict, f, indent=2)
