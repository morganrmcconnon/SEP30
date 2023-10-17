import os
import json

folder_structure_dict = {}

for root, dirs, files in os.walk("data"):
    for filename in [f for f in files if f.endswith(".txt")]:
        parent_folders = root.split(os.sep)
        year = parent_folders[1]
        month = parent_folders[2]
        if year not in folder_structure_dict:
            folder_structure_dict[year] = {}
        if month not in folder_structure_dict[year]:
            folder_structure_dict[year][month] = []

        folder_structure_dict[year][month].append(filename)

with open("data_folder_structure.json", "w") as f:
    json.dump(folder_structure_dict, f)