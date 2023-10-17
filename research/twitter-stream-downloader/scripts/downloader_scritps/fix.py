import json
import os
import urllib.parse
import concurrent.futures

# This script focuses on fixing the dataset, before I change the other Python scripts to produce a more efficient, space-saving dataset

# To save space, remove all unnecessary parts in each json file, and store all .bz2 and .gz files in a .txt file

# Get all json files
json_files = []
for dirpath, dirnames, filenames in os.walk("data"):
    for filename in [f for f in filenames if f.endswith(".json")]:
        json_files.append(os.path.join(dirpath, filename))

# Fix each json file
def fix(json_file):
    data = json.loads(open(json_file, "r").read())
    data = [x.split('/')[-1] for x in data if x.endswith(".bz2") or x.endswith(".gz")]
    data = [urllib.parse.unquote(url_encoded_string) for url_encoded_string in data]
    # Write a list to a file, item per line
    with open(json_file.removesuffix(".json") + ".txt", "w") as f:
        f.write("\n".join(data))
        os.remove(json_file)

# Fix each json file in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(fix, json_files)
