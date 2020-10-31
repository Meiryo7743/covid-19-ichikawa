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
FILES = [
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

for i in FILES:
    URL = 'https://docs.google.com/spreadsheets/d/e/' + \
        i['id'] + '/pub?single=true&output=tsv&gid=' + i['gid']
    DST = DIR + i['name']
    FILE_TSV = DST + '.tsv'
    FILE_YAML = DST + '.yaml'

    # Download the data files
    urllib.request.urlretrieve(URL, FILE_TSV)

    # Set data
    data = []

    # Load TSV
    with open(FILE_TSV, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            data.append(row)

    # Convert TSV to YAML
    with open(FILE_YAML, 'w') as f:
        yaml.dump(data, f, encoding='utf-8', allow_unicode=True)

    # Get the content of YAML
    with open(FILE_YAML, encoding='utf-8') as f:
        content = f.read()

    # Replace some strings in order to be correct YAML format
    with open(FILE_YAML, 'w') as f:
        content = re.sub(r"'(\[.+\]|\d+|)'", r'\1', content)
        f.write(content)

    # Delete TSV files
    os.remove(FILE_TSV)
