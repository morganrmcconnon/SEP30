import json
import re
import os

def match_pattern(input_string, regex_patterns):
    
    matched_pattern = None
    extracted_values = None

    for pattern in regex_patterns:
        match = re.match(pattern, input_string)
        if match:
            matched_pattern = pattern
            extracted_values = match.groups()
            break

    return matched_pattern, extracted_values

def check_match(ymd_tuple, dhm_tuple):
    if(ymd_tuple == None or dhm_tuple == None):
        return True
    ymd_tuple_full = list(ymd_tuple) + (5 - len(ymd_tuple)) * [None]
    dhm_tuple_full = (5 - len(dhm_tuple)) * [None] + list(dhm_tuple)
    for i in range(5):
        if ymd_tuple_full[i] != dhm_tuple_full[i] and ymd_tuple_full[i] != None and dhm_tuple_full[i] != None:
            return False
    return True
true_bz2_patterns = [
    "YYYY/mm/dd/HH/MM.json.bz2",
    "YYYY/mm-b/dd/HH/MM.json.bz2",
    "mm/dd/HH/MM.json.bz2",
    "dd/HH/MM.json.bz2",
    "YYYY/mm/dd/HH/MM.json.gz",
    "YYYYmmdd/YYYYmmddHHMM00.json.gz",
]
true_tar_patterns = [
    "twitter-json-scrape-YYYY-mm.zip.txt",
    "archiveteam-twitter-YYYY-mm.tar.txt",
    "archiveteam-twitter-stream-YYYY-mm.tar.txt",
    "archiveteam-twitter-stream-YYYY-mm-b.tar.txt",
    "twitter-stream-YYYY-mm-dd.tar.txt",
    "twitter-YYYY-mm-dd.tar.txt",
    "twitter_stream_YYYY_mm_dd.tar.txt",
    "twitter-stream-YYYY-mm-dd.zip.txt",
    "twitter-stream-YYYYmmdd.tar.txt",
]
regex_bz2_patterns = [
    r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
    r"(\d{4})/(\d{2})-b/(\d{2})/(\d{2})/(\d{2}).json.bz2",
    r"(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
    r"(\d{2})/(\d{2})/(\d{2}).json.bz2",
    r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.gz",
    r"(\d{4})(\d{2})(\d{2})/(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})00.json.gz",
]
regex_tar_patterns = [
    r"twitter-json-scrape-(\d{4})-(\d{2}).zip.txt",
    r"archiveteam-twitter-(\d{4})-(\d{2}).tar.txt",
    r"archiveteam-twitter-stream-(\d{4})-(\d{2}).tar.txt",
    r"archiveteam-twitter-stream-(\d{4})-(\d{2})-b.tar.txt",
    r"twitter-stream-(\d{4})-(\d{2})-(\d{2}).tar.txt",
    r"twitter-(\d{4})-(\d{2})-(\d{2}).tar.txt",
    r"twitter_stream_(\d{4})_(\d{2})_(\d{2}).tar.txt",
    r"twitter-stream-(\d{4})-(\d{2})-(\d{2}).zip.txt",
    r"twitter-stream-(\d{4})(\d{2})(\d{2}).tar.txt",
]

regex_bz2_patterns_encrypt = {
    r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2" : 1,
    r"(\d{4})/(\d{2})-b/(\d{2})/(\d{2})/(\d{2}).json.bz2" : 2,
    r"(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2" : 3,
    r"(\d{2})/(\d{2})/(\d{2}).json.bz2" : 4,
    r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.gz" : 5,
    r"(\d{4})(\d{2})(\d{2})/(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})00.json.gz" : 6,
}

regex_tar_patterns_encrypt = {
    r"twitter-json-scrape-(\d{4})-(\d{2}).zip.txt" : 1,
    r"archiveteam-twitter-(\d{4})-(\d{2}).tar.txt" : 2,
    r"archiveteam-twitter-stream-(\d{4})-(\d{2}).tar.txt" : 3,
    r"archiveteam-twitter-stream-(\d{4})-(\d{2})-b.tar.txt" : 4,
    r"twitter-stream-(\d{4})-(\d{2})-(\d{2}).tar.txt" : 5,
    r"twitter-(\d{4})-(\d{2})-(\d{2}).tar.txt" : 6,
    r"twitter_stream_(\d{4})_(\d{2})_(\d{2}).tar.txt" : 7,
    r"twitter-stream-(\d{4})-(\d{2})-(\d{2}).zip.txt" : 8,
    r"twitter-stream-(\d{4})(\d{2})(\d{2}).tar.txt" : 9,
}

regex_tar_patterns_decrypt_str = {
    1: r"twitter-json-scrape-{}-{}.zip.txt",
    2: r"archiveteam-twitter-{}-{}.tar.txt",
    3: r"archiveteam-twitter-stream-{}-{}.tar.txt",
    4: r"archiveteam-twitter-stream-{}-{}-b.tar.txt",
    5: r"twitter-stream-{}-{}-{}.tar.txt",
    6: r"twitter-{}-{}-{}.tar.txt",
    7: r"twitter_stream_{}_{}_{}.tar.txt",
    8: r"twitter-stream-{}-{}-{}.zip.txt",
    9: r"twitter-stream-{}{}{}.tar.txt",
}

replace_patterns = {
    "{YYYY}/{}{}/{}{}/{}{}/{}{}.json.bz{}" : "YYYY/mm/dd/HH/MM.json.bz2",
    "{YYYY}/{}{}-b/{}{}/{}{}/{}{}.json.bz{}" : "YYYY/mm-b/dd/HH/MM.json.bz2",
    "{}{}/{}{}/{}{}/{}{}.json.bz{}" : "mm/dd/HH/MM.json.bz2",
    "{}{}/{}{}/{}{}.json.bz{}" : "dd/HH/MM.json.bz2",
    "" : "",
    "{YYYY}/{}{}/{}{}/{}{}/{}{}.json.gz" : "YYYY/mm/dd/HH/MM.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{}{}{}{}{}{}{}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{}{}{}{}{YYYY}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{}{}{}{YYYY}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{}{}{YYYY}{}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{}{YYYY}{}{}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{YYYY}{}{}{}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{}{YYYY}{YYYY}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{YYYY}{}{}{}{}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{YYYY}{}{YYYY}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    "{YYYY}{}{}{}{}/{YYYY}{}{YYYY}{YYYY}{}.json.gz" : "YYYYmmdd/YYYYmmddHHMM00.json.gz",
    'twitter-json-scrape-{YYYY}-{}{}.zip.txt': "twitter-json-scrape-YYYY-mm.zip.txt",
    'archiveteam-twitter-{YYYY}-{}{}.tar.txt': "archiveteam-twitter-YYYY-mm.tar.txt",
    'archiveteam-twitter-stream-{YYYY}-{}{}.tar.txt': "archiveteam-twitter-stream-YYYY-mm.tar.txt",
    'archiveteam-twitter-stream-{YYYY}-{}{}-b.tar.txt': "archiveteam-twitter-stream-YYYY-mm-b.tar.txt",
    'twitter-stream-{YYYY}-{}{}-{}{}.tar.txt': "twitter-stream-YYYY-mm-dd.tar.txt",
    'twitter-{YYYY}-{}{}-{}{}.tar.txt': "twitter-YYYY-mm-dd.tar.txt",
    'twitter_stream_{YYYY}_{}{}_{}{}.tar.txt': "twitter_stream_YYYY_mm_dd.tar.txt",
    'twitter-stream-{YYYY}-{}{}-{}{}.zip.txt': "twitter-stream-YYYY-mm-dd.zip.txt",
    'twitter-stream-{YYYY}{}{}{}{}.tar.txt': "twitter-stream-YYYYmmdd.tar.txt",
}

data = json.load(open('data_folder_structure.json', 'r'))

tar_patterns = {}

for year in data.keys():
    tar_patterns[year] = {}
    for month in data[year].keys():
        tar_patterns[year][month] = {}
        for tar_file in data[year][month]:
            pattern, values = match_pattern(tar_file, regex_tar_patterns)
            pattern = regex_tar_patterns_encrypt[pattern] if pattern else 0
            if pattern not in tar_patterns[year][month]:
                tar_patterns[year][month][pattern] = [values]
            else:
                tar_patterns[year][month][pattern].append(values)


year_months = {}

for year in tar_patterns.keys():
    for month in tar_patterns[year].keys():
        for tar_file in tar_patterns[year][month]:
            for values in tar_patterns[year][month][tar_file]:
                values_expanded = values if len(values) == 3 else (values[0], values[1], "00")
                if (year != values[0] or month != values[1]):
                    value_to_add = [tar_file, year, month]
                else:
                    value_to_add = [tar_file]
                if(values_expanded not in year_months):
                    year_months[values_expanded] = [value_to_add]
                else:
                    year_months[values_expanded].append(value_to_add)


year_months_encrypt = {}

for values in year_months:
    if(values[0] not in year_months_encrypt):
        year_months_encrypt[values[0]] = {}
    if(values[1] not in year_months_encrypt[values[0]]):
        year_months_encrypt[values[0]][values[1]] = {}
    
    year_months_encrypt[values[0]][values[1]][values[2]] = []

    for pattern in year_months[values]:
        tar_file = pattern[0]
        if(len(pattern) == 3):
            year_folder = pattern[1]
            month_folder = pattern[2]
        elif(len(pattern) == 1):
            year_folder = values[0]
            month_folder = values[1]
        tar_file = regex_tar_patterns_decrypt_str[tar_file].format(*values)
        
        bz2_files = open(os.path.join('data', year_folder, month_folder, tar_file), "r").read().split("\n")
        bz2_pattern_list = list(dict.fromkeys([match_pattern(bz2_file, regex_bz2_patterns)[0] for bz2_file in bz2_files]))
        bz2_pattern_list = [(regex_bz2_patterns_encrypt[pattern] if pattern else 0) for pattern in bz2_pattern_list]
        year_months_encrypt[values[0]][values[1]][values[2]].append([pattern, bz2_pattern_list])


open('year_month_encrypt.json', 'w').write(json.dumps(year_months_encrypt))