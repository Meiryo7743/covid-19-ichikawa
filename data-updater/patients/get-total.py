import ruamel.yaml as yaml
import toml


def count(data: list, condition: str, age: str):
    return sum([i[condition] == age for i in data])


with open('./data-updater/patients/config.toml', 'r', encoding='utf-8') as f:
    load_config: dict = toml.load(f)

    config: dict = load_config['get-sum']

for i in config:
    with open(i['src'], 'r', encoding='utf-8') as f:
        raw = yaml.safe_load(f)

        total: list = [
            {
                'total':  len(raw),
                '年代_10歳未満': count(raw, '年代', '10歳未満'),
                '年代_10代': count(raw, '年代', '10代'),
                '年代_20代': count(raw, '年代', '20代'),
                '年代_30代': count(raw, '年代', '30代'),
                '年代_40代': count(raw, '年代', '40代'),
                '年代_50代': count(raw, '年代', '50代'),
                '年代_60代': count(raw, '年代', '60代'),
                '年代_70代': count(raw, '年代', '70代'),
                '年代_80代': count(raw, '年代', '80代'),
                '年代_90代': count(raw, '年代', '90代'),
                '年代_90代以上': count(raw, '年代', '90代以上'),
            }
        ]

    with open(i['dst'], 'w', encoding='utf-8', newline='\n') as f:
        yaml.dump(total, f, allow_unicode=True)
