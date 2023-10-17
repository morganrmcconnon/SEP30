# %%
import json
import re
import os

data = json.load(open('data_folder_structure.json', 'r'))

tar_patterns = {}

for year in data.keys():
    
    for month in data[year].keys():
        
        patterns = list(dict.fromkeys([re.sub(r'\d', '{}', re.sub(r'20\d\d', '{YYYY}', filename)) for filename in data[year][month]]))

        for pattern in patterns:
            if(pattern not in tar_patterns):
                tar_patterns[pattern] = [[year, month]]
            else:
                tar_patterns[pattern].append([year, month])

        if(len(patterns) > 1):
            print(year, month, data[year][month])


# %%

all_bz2_patterns = {}

for year in data.keys():
    
    all_bz2_patterns[year] = {}

    for month in data[year].keys():

        all_bz2_patterns[year][month] = {}

        for filename in data[year][month]:

            bz2_files = open(os.path.join('data', year, month, filename), "r").read().split("\n")

            all_bz2_patterns[year][month][filename] = []

            for bz2_file in bz2_files:
                bz2_pattern = re.sub(r'\d', '{}', re.sub(r'20\d\d', '{YYYY}', bz2_file))
                if(bz2_pattern not in all_bz2_patterns[year][month][filename]):
                    all_bz2_patterns[year][month][filename].append(bz2_pattern)

