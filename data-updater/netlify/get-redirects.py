import re
import toml

LANGUAGES = ['ja', 'en']
REDIRECTS = [
    {
        'from': '/contacts',
        'to': 'https://forms.gle/rJAhPqckU1Ak7tFQ9',
        'force': True
    },
    {
        'from': '/cards/details-of-all-patients',
        'to': '/cards/details-of-patients-with-symptoms',
        'force': True
    },
    {
        'from': '/cards/details-of-latest-30-patients',
        'to': '/cards/details-of-latest-30-patients-with-symptoms',
        'force': True
    },
    {
        'from': '/cards/the-number-of-patients',
        'to': '/cards/the-number-of-patients-with-symptoms',
        'force': True
    },
    {
        'from': '/cards/changes-in-the-number-of-passengers-on-toei-subway',
        'to': '/cards/changes-in-the-rates-of-toei-subway-passengers',
        'force': True
    },
    {
        'from': '/*',
        'to': '/404.html',
        'force': False,
        'status': '404'
    }
]

data = {
    'redirects': []
}

for i in REDIRECTS:
    for j in LANGUAGES:
        dict = {}

        dict['from'] = '/' + j + i.get('from')

        if i.get('to').startswith('http'):
            dict['to'] = i.get('to')
        else:
            dict['to'] = '/' + j + i.get('to')

        dict['force'] = i.get('force')

        if not i.get('status') == None:
            dict['status'] = int(i.get('status'))

        data['redirects'].append(dict)

with open('./static/netlify.toml', 'w', encoding='utf-8', newline='\n') as f:
    toml.dump(data, f)
