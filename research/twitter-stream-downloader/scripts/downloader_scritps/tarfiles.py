# %%
import requests
import xml.etree.ElementTree as ET
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os

def fetch_xml_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(
            f"Failed to fetch XML content from {url}. Status code: {response.status_code}"
        )


def get_original_file_names(xml_content):
    root = ET.fromstring(xml_content)
    tar_file_names = []
    for file_element in root.findall("./file"):
        file_name = file_element.get("name")
        source_type = file_element.get("source")
        if source_type == "original":
            tar_file_names.append(file_name)
    return tar_file_names


# %%

current_time = datetime.datetime.now()  # Get current time

# 2011 has a different format, so we will add it manually

tweetfiles = {}

tweetfiles[2011] = {
    9: {
        "https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-09.zip/": {}
    },
    10: {
        "https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-10.zip/": {}
    },
    11: {
        "https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-11.zip/": {}
    },
    12: {
        "https://archive.org/download/archiveteam-twitter-json-2011/twitter-json-scrape-2011-12.zip/": {}
    },
}


years = range(2012, 2023)
months = range(1, 13)

for year in years:
    tweetfiles[year] = {}

    for month in months:
        tweetfiles[year][month] = {}

        xml_url = f"https://archive.org/1/items/archiveteam-twitter-stream-{year}-{month:02d}/archiveteam-twitter-stream-{year}-{month:02d}_files.xml"

        try:
            xml_content = fetch_xml_content(xml_url)

            tar_file_names = get_original_file_names(xml_content)

            if tar_file_names:
                for file_name in tar_file_names:
                    # I explored the files and only .tar and .zip files are the compressed files that contains the data. All other files are metadata files or image files.
                    # If you want to check, omit this if statement and follow the code block further down below.
                    if not (file_name.endswith(".tar") or file_name.endswith(".zip")):
                        continue

                    tweetfiles[year][month][f"https://archive.org/download/archiveteam-twitter-stream-{year}-{month:02d}/{file_name}/"] = {}

            else:
                print(f"{xml_url} No original files found.")

        except Exception as e:
            print(f"Error: {e}")

runtime = datetime.datetime.now() - current_time  # Calculate runtime

# Takes about 3-4 minutes to run
print(f"Runtime: {runtime}, {runtime.total_seconds()} seconds")


# %%
# In a Jupyter notebook, explore all extensions of the files with this block of code:
# Only .tar and .zip files are the compressed files that contains the data. All other files are metadata files or image files.

tarfiles = []

for year in tweetfiles.keys():
    for month in tweetfiles[int(year)].keys():
        for file_name in tweetfiles[int(year)][int(month)].keys():
            tarfiles.append(file_name)

dict.fromkeys([url.split(".")[-1] for url in tarfiles])

# %%

# Save the filenames to a json file
open("tweetfiles.json", "w").write(json.dumps(tweetfiles))

