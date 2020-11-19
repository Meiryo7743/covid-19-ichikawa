import csv
import os
import re
import urllib.request
import yaml

# Data dir
DIR = './data/'

# Check existence of data dir
if not (os.path.isdir(DIR)):
    os.mkdir(DIR)

# List of the data files
SHEETS = [
    {
        'name': 'details_of_patients_with_symptoms',
        'id': '2PACX-1vSVUIR-4xTBX2x-5-4lf9dbjuvGsRUL45GxDJ_RUIG1aUNC9XB9QFNlusKNgvUu4LJuR3rvu5JBQd4c',
        'gid': '0'
    },
    {
        'name': 'the_number_of_patients_with_symptoms',
        'id': '2PACX-1vSVUIR-4xTBX2x-5-4lf9dbjuvGsRUL45GxDJ_RUIG1aUNC9XB9QFNlusKNgvUu4LJuR3rvu5JBQd4c',
        'gid': '1334047042'
    },
    {
        'name': 'details_of_patients_without_symptoms',
        'id': '2PACX-1vRhCk-rWHxbPh2CWEvtJsVWi52WzdusohxNmIOgPSlr6y3mq1aEfm3HWcB0yV7tp9OI4UULAnMJV7XF',
        'gid': '0'
    },
    {
        'name': 'the_number_of_patients_without_symptoms',
        'id': '2PACX-1vRhCk-rWHxbPh2CWEvtJsVWi52WzdusohxNmIOgPSlr6y3mq1aEfm3HWcB0yV7tp9OI4UULAnMJV7XF',
        'gid': '1334047042'
    }
]

for i in SHEETS:
    url = 'https://docs.google.com/spreadsheets/d/e/' + \
        i['id'] + '/pub?single=true&output=tsv&gid=' + i['gid']
    dst = DIR + i['name']
    file_tsv = dst + '.tsv'
    file_yaml = dst + '.yaml'

    # Download the data files
    urllib.request.urlretrieve(url, file_tsv)

    # Set data
    data = []

    # Load TSV
    with open(file_tsv, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            data.append(row)

    # Convert TSV to YAML
    with open(file_yaml, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, encoding='utf-8', allow_unicode=True)

    # Get the content of YAML
    with open(file_yaml, encoding='utf-8') as f:
        content = f.read()

    # Replace some strings in order to be correct YAML format
    with open(file_yaml, 'w', encoding='utf-8') as f:
        content = re.sub(r"'(\[.+\]|\d+|)'", r'\1', content)
        f.write(content)

    # Delete TSV files
    os.remove(file_tsv)
