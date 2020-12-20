import datetime
import json
import toml


def format_date(value):
    if value == '':
        return None
    else:
        result = datetime.datetime.strptime(
            value,
            '%Y-%m-%d'
        )
        return result.strftime('%m-%d')


with open('./data-updater/config.toml', 'r', encoding='utf-8') as f:
    config = toml.load(f)['subway']

dst = config['dst']
data = config['data'][0]

with open(dst + data['raw']) as f:
    data_json = json.load(f)['datasets']

list = []

for i in data_json:
    date_former = format_date(i['period']['begin'])
    date_latter = format_date(i['period']['end'])

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
