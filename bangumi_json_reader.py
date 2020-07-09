import os
import json
import numpy as np
import pandas as pd
from pandas import DataFrame, Series


# this function reading json file and than return a DataFrame
def json_cleaning(path):
    with open(path, "r", encoding="utf-8") as fd:
        json_content = json.load(fd, encoding="utf-8")
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
print('paths loading complete. ')
print('press any ket to continue...')
_ = input('>')




print('transforming json to DataFrame...')
bangumi_dfs = []
for path in paths[1]:
    df = json_cleaning(path)
    print('Get DataFrame from {}'.format(path))
    if df is not None:
        bangumi_dfs.append(df)

# get all tags
all_tags = set()
for df in bangumi_dfs:
    all_tags.update(df.index)

print("all_tags's length: ", len(all_tags))

orig = ['id', 'name', '1', '2', '3',
               '4', '5', '6', '7', '8', '9', '10', 'total',
               'wish', 'doing', 'on_hold', 'dropped']

all_tags.update(orig)
print('all_tags length: ',len(all_tags))
items = list(all_tags)
print('items length:', len(items))
items = Series(items)
items = items.rename(columns={0: 'tags'})
print("items's length:", len(items))

# a dummy DataFrame with all features in it.
dummy = DataFrame(range(len(items.array)), index=items.array)
dummy.index.rename('item', inplace=True)
print('dummy length: ', len(dummy))

# a new list with processed DataFrame.
# if directly use 'concat' you will get a ValueError
# sorry but I don't know why
# so I try a clumsy way.

bgm_dfs =[]
for df in bangumi_dfs[::1]:
    df = dummy.merge(df, how='left', on='item')
    bgm_dfs.append(df)

# use 'merge' or 'join' will cause a MemoryError
df0 = pd.concat([df for df in bgm_dfs if df.shape == (3170, 2)], join='outer', axis=1)
# remove all dummy columns
df0 = df0.T.drop_duplicates(keep=False).T

df0.to_csv('bangumi.csv', encoding='utf-8')
print('csv file is saved.')
print('press any key to exit.')
_ = input('>')