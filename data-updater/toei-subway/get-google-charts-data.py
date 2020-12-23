import datetime
import json
import toml


def format_date(date: str):
    if date == '':
        return None
    else:
        result = datetime.datetime.strptime(
            date,
            '%Y-%m-%d'
        )

        return result.strftime('%m-%d')


with open('./data-updater/toei-subway/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)['get-passengers']

with open(config['src']) as f:
    datasets: dict = json.load(f)['datasets']

google_charts_rows: list = [
    [format_date(i['period']['begin']) + '~' + format_date(i['period']['end']),
        i['data'][0],
        i['data'][1],
        i['data'][2]]
    for i in datasets
]

google_charts_data: dict = {
    'data': {
        'headers': [
            {'type': 'string', 'name': 'Durations'},
            {'type': 'number', 'name': '6:30~7:30'},
            {'type': 'number', 'name': '7:30~9:30'},
            {'type': 'number', 'name': '9:30~10:30'},
        ],
        'rows': google_charts_rows,
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
        'color': '#8f8f8f',
        'fontName': 'sans-serif',
        'fontSize': 14,
        'hAxes': [
            {
                'slantedText': True,
                'slantedTextAngle': 45,
                'textStyle': {'color': '#8f8f8f'}
            }
        ],
        'legend': {
            'alignment': 'end',
            'position': 'top',
            'textStyle': {'color': '#8f8f8f'}
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
                'baselineColor': '#8f8f8f',
                'format': "#'%'",
                'gridlines': {'color': '#8f8f8f'},
                'maxValue': 20,
                'minorGridlines': {'color': 'none'},
                'minValue': -100,
                'textStyle': {'color': '#8f8f8f'}
            },
            {
                'baseline': 0,
                'baselineColor': '#8f8f8f',
                'format': "#'%'",
                'gridlines': {'color': '#8f8f8f'},
                'maxValue': 20,
                'minorGridlines': {'color': 'none'},
                'minValue': -100,
                'textStyle': {'color': '#8f8f8f'}
            }
        ],
        'width': len(google_charts_rows) * 3 * 14
    }
}

with open(config['dst'], 'w', encoding='utf-8', newline='\n') as f:
    json.dump(google_charts_data, f, indent=2)
