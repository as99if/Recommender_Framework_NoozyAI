import fnmatch
import os
import json
import pprint
import sys
import random

import pandas as pd

_video_ids = ['1zvaXioSwy', '1zvaXioSwy', 'HLhX98vwDm', 'JRh0bL2imm', '0ttVaMqQhZ', 'wo7QQKKdtW', 'hDiXkAABCM',
             'kbT9AiPt1L', 'jlkH3UxU3G', 'kbT9AiPt1L', 'G7ia9HXVAH', 'u38TGk3C5U', '5K5ZHFQ48z', 'JRh0bL2imm',
             'NaNEP4ccrN', 'JRh0bL2imm', '1cBMqBsxN9', 'rpACux3Aed', '9GPXTYTt1i', 'JZhmchEzeU', 'bFKi4VV5qF']
video_ids = []

algorithm_id = 'CB-ItemBased-Hybrid'

path = os.path.dirname(sys.modules['__main__'].__file__)
#print(path)
metadata_filename = 'all_metadata_latest.json'
metadata = None
m = None
with open(metadata_filename, encoding='utf-8') as json_file:
    metadata = json.load(json_file)
    metadata = pd.json_normalize(metadata)
    keys = metadata['dc:identifier'].unique().tolist()
    video_ids = random.sample(keys, 20)

for video_id in video_ids:
    filename = f'forEvaluationHybrid/recommendation_{video_id}_{algorithm_id}.json'
    store_filename = os.path.join(path, filename)
    with open(filename, encoding='utf-8') as json_file:
        data = json.load(json_file)

        print(f"Sample : {video_ids.index(video_id)}")
        m = metadata.loc[metadata['dc:identifier'] == video_id]
        ref_name = f"{video_id}-{m['dc:title'].values[0]}"
        #print(ref_name)

        #print("Reference Video : " + data['ref'])
        lala = pd.DataFrame.from_dict(data['result'])
        #pprint.pprint(lala)
        # lala.to_excel(f'excel/{algorithm_id}.xlsx', encoding='utf-8', sheet_name=ref_name)
        lala.to_excel(f'excelHybrid/{ref_name}.xlsx', encoding='utf-8')

        #print("==================")
        # pprint.pprint(lala)
