import json

data = json.load(open('json_data/data.json', 'r'))
new_data = json.load(open('json_data/sh.json', 'r'))

for game, d1 in data.items():
    for rule, d2 in d1.items():
        for behavior, d3 in d2.items():
            for mode in d3:
                cur = data[game][rule][behavior][mode]
                temp = new_data[game][rule][behavior][mode]
                for new_key, d4 in temp.items():
                    cur[new_key] = d4
                    for strategy, percent in d4.items():
                        cur[strategy][new_key] = 100 - percent
json.dump(data, open('json_data/temp.json', 'w'), indent=4)
