import toml

with open('./i18n-generator/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)

with open(config['i18n']['path'], 'r', encoding='utf-8') as f:
    translations: dict = toml.load(f)

for i in config['i18n']['language']:
    i18n: dict = {
        j: {
            'one': translations[j].get('one').get(i) if translations[j].get('one') is not None else None,
            'other': translations[j]['other'][i],
        }
        for j in translations
    }

    with open('./i18n/' + i + '.toml', 'w', encoding='utf-8', newline='\n') as f:
        toml.dump(i18n, f)
