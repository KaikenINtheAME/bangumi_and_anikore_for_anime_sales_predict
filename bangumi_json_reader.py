import os
import json
import numpy as np
import pandas as pd
from pandas import DataFrame, Series


# this function reading json file and than return a DataFrame
def json_cleaning(path):
    with open(path, "r") as fd:
        json_content = json.load(fd)
        tags = DataFrame(json_content['tags'])
        tags.set_index('name', inplace=True)
        # 'sr' means Series
        id_sr = Series(json_content['id'], index=['id'])
        name_sr = Series(json_content['name'], index=['name'])
        if 'rating' not in json_content.keys():
            return
        rat_sr = Series(json_content['rating']['count'])
        tt_sr = Series(json_content['rating']['total'], index=['total'])

        if 'wish' in Series(json_content['collection']).keys():
            wish_sr = Series(json_content['collection']['wish'], index=['wish'])
        else:
            wish_sr = Series([0])

        if 'cole_sr' in Series(json_content['collection']).keys():
            cole_sr = Series(json_content['collection']['collect'], index=['collect'])
        else:
            cole_sr = Series([0])

        if 'doing' in Series(json_content['collection']).keys():
            di_sr = Series(json_content['collection']['doing'], index=['doing'])
        else:
            di_sr = Series([0])

        if 'on_hold' in Series(json_content['collection']).keys():
            oh_sr = Series(json_content['collection']['on_hold'], index=['on_hold'])
        else:
            oh_sr = Series([0])
        dp_sr = Series(json_content['collection']['dropped'], index=['dropped'])
        df = pd.concat([id_sr, name_sr, rat_sr, tt_sr, wish_sr, cole_sr, di_sr,
                        oh_sr, dp_sr, tags], sort=False)
        df[0] = np.where(pd.isnull(df[0]), df['count'], df[0])
        del df['count']
        df.rename(columns={0: 'info'}, inplace=True)
        df.index.set_names('item', inplace=True)
    return df


paths = pd.read_csv('bangumi_ani_tv_path.csv', encoding='utf-8', header=None)

# look, I merging they like a baka.
# but this way can avoid MemoryError.

bangumi_dfs = []
for i in range(len(paths)):
    path = paths.loc[i][0]
    df = json_cleaning(path)
    if df is not None:
        bangumi_dfs.append(df)

all_tags = set()
for df in bangumi_dfs:
    all_tags.update(df.index)

orig = Series(['id', 'name', '1', '2', '3',
               '4', '5', '6', '7', '8', '9', '10', 'total',
               'wish', 'doing', 'on_hold', 'dropped'])

tags = pd.concat([all_tags, orig])

# a dummy DataFrame with all features in it.
dummy = DataFrame(range(len(tags)), index=tags[0])
dummy.index.rename('item', inplace=True)

df0 = pd.merge(dummy, bangumi_dfs[0], on='item')
for i in range(1, len(bangumi_dfs)):
    df = bangumi_dfs[i].rename({'info': 'info{}'.format(bangumi_dfs[i].loc['id'])})
    df0 = pd.merge(df0, df, how='outer')

# del the dummy column
del df0[0]

df0.to_csv('bangumi.csv', encoding='utf-8')
