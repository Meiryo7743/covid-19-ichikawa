import ruamel.yaml as yaml
import toml

with open('./i18n-generator/config.toml', 'r', encoding='utf-8') as f:
    config: dict = toml.load(f)

with open(config['i18n']['path'], 'r', encoding='utf-8') as f:
    translations: dict = toml.load(f)

for i in config['i18n']['language']:
    i18n: dict = {
        j: translations[j][i]
        for j in translations
    }

    with open('./i18n/' + i + '.yaml', 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(i18n, f, indent=2, allow_unicode=True)
