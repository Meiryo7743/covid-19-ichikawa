from dateutil.relativedelta import relativedelta
import datetime
import json
import os
import re
import urllib.request

DIR = './data/'
SRC = DIR + 'metro.json'
DST = DIR + 'toei_subway.json'

# Check existence of data dir
if not (os.path.isdir(DIR)):
    os.mkdir(DIR)

# Download
URL = 'https://raw.githubusercontent.com/tokyo-metropolitan-gov/covid19/development/data/metro.json'
urllib.request.urlretrieve(URL, SRC)

# Convert
with open(SRC) as f:
    data = json.load(f)['datasets']

label = []
time_0 = []
time_1 = []
time_2 = []

for key in data:
    # Fix Date Format
    # MM/DD~DD -> 0MM/0DD~0DD
    date_fix = re.sub(
        r'^(\d+)/(\d+)~(\d+)$',
        r'0\1/0\2~0\3',
        key['label']
    )
    # -> MM/DD~DD
    date_fix = re.sub(
        r'0(\d\d)',
        r'\1',
        date_fix
    )
    # -> MM-DD~DD
    date_fix = re.sub(
        r'/',
        r'-',
        date_fix
    )
    # -> MM-DD~MM-DD
    date_fix = re.sub(
        r'^(\d\d-)(\d\d~)(\d\d)$',
        r'\1\2\1\3',
        date_fix
    )
    # -> YYYY-MM-DD~YYYY-MM-DD
    date_fix = re.sub(
        r'^(.+)~(.+)$',
        r'2020-\1~2020-\2',
        date_fix
    )

    # Fix Month (Left > Right -> Left < Right)
    date_left = re.sub(
        r'^(.+)~.+$',
        r'\1',
        date_fix
    )
    date_right = re.sub(
        r'^.+~(.+)$',
        r'\1',
        date_fix
    )
    date_left = datetime.datetime.strptime(date_left, '%Y-%m-%d')
    date_right = datetime.datetime.strptime(date_right, '%Y-%m-%d')

    if date_left > date_right:
        date_right = date_right + relativedelta(months=1)

    date_left = date_left.strftime('%m-%d')
    date_right = date_right.strftime('%m-%d')
    date = date_left + "~" + date_right

    label.append(date)
    time_0.append(key['data'][0])
    time_1.append(key['data'][1])
    time_2.append(key['data'][2])

dict = {
    'type': 'bar',
    'data': {
        'labels': label,
        'datasets': [
            {
                'label': '6:30~7:30',
                'data': time_0,
                'backgroundColor': '#c2d94c'
            },
            {
                'label': '7:30~9:30',
                'data': time_1,
                'backgroundColor': '#03af7a'
            },
            {
                'label': '9:30~10:30',
                'data': time_2,
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

# Export
with open(DST, 'w') as f:
    json.dump(dict, f, indent=2)

# Delete the Source File
os.remove(SRC)
