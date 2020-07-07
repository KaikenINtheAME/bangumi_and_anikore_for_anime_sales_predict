import os
import json
import numpy as np
import pandas as pd

dictnames = os.listdir('./bangumi_data')

# I used a three-steps way to filter json file
# be honest, it's a dull way.

# get all file paths
filr_paths = []

for dname in dictnames:
    path = os.listdir('./bangumi_data/{}'.format(dname))
    for filename in path:
        filr_paths.append('./bangumi_data/{}/{}'.format(dname, filename))

# get anime paths
ani_path = []

for f in filr_paths:
    print('fetch {}...'.format(f))
    with open(f, "r") as fd:
        json_content = json.load(fd)
        if json_content['type'] == 2:
            ani_path.append(f)

# get 2018-2019 TV anime paths
ani_tv_path = []

season_list = ['2017年1月', '2017年4月', '2017年7月', '2017年10月',
               '2018年1月', '2018年4月', '2018年7月', '2018年10月']
ban_list = ['泡面', '泡面番','剧场版', 'OVA', 'ova',
            'OAD', 'oad', '里', '里番']

for path in ani_path:
    print("fetch {}...".format(path))
    with open(path, 'r') as fd:
        json_content = json.load(fd)
        # some items have not tags
        if 'tags' not in json_content.keys():
            continue
        tags = pd.DataFrame(json_content['tags'])
        in_list = False
        for season in season_list:
            if season in list(tags['name']):
                in_list = True
        for ban in ban_list:
            if ban in list(tags['name']):
                in_list = False
        if in_list:
            ani_tv_path.append(path)

ani_tv_path = pd.Series(ani_tv_path)
ani_tv_path.to_csv('bangumi_ani_tv_path.csv', encoding='utf-8')