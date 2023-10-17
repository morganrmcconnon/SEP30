import json
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# It took 4 hours to download all

def get_files_from_tar_file(url):
    # Given an url of the tar file on the Internet Archive, return a list of URLs of the files inside the tar file.

    print(url)

    response = requests.get(url)

    print(f"[{response.status_code}] {url}")

    while response.status_code != 200:

        print(f"[Failed to fetch URL:] {url}")

        status_code = response.status_code

        if str(status_code).startswith("5"):
            print("[Server error. Retrying...]")
            response = requests.get(url)
            print(f"[{response.status_code}] {url}")
            continue

        elif str(status_code).startswith("4"):
            print(f"[Client error. Aborting...] {url}")
            return []

        else:
            print(f"[Unknown error. Aborting...] {url}")
            return []

    soup = BeautifulSoup(response.content, "html.parser")

    print(f"[Finish parsing HTML as soup] {url}")

    files = []

    for link in soup.find_all("a", href=True):
        # if link['href'].endswith('.gz'):
        absolute_url = urljoin(url, link["href"])
        file_name = absolute_url.split("/")[-1]
        if(file_name.endswith(".gz") or file_name.endswith(".bz2")):
            files.append(file_name)

    print(f"[Finish getting href list] {url}")

    return files

# for each tar/zip file, get the list of files inside it
# Usually takes 1-2 minutes to run per tar/zip file, if the status code is 200. 
# Sometimes the status code starts with 5 when the server is busy, and the script will retry until it gets a 200 status code. If you see a 5 status code, don't worry, it will retry automatically. But you can stop the script and redownload again later if you want.

def process_tar_file(year, month, tar_file_url):

    files = get_files_from_tar_file(tar_file_url)

    save_to_folder = f"data/{year}/{int(month):02d}"
    
    tar_file_name = tar_file_url.split("/")[-2]
    
    with open(f"{save_to_folder}/{tar_file_name}.txt", "w") as file:
        file.write('\n'.join(files))
        print(f"[Saved] {tar_file_name}")
    
    with open("completed.txt", 'a') as file:
        file.write(f"{tar_file_url}\n")


if __name__ == "__main__":
    tweetfiles = json.loads(open("tweetfiles.json", "r").read())
    
    with open("completed.txt", 'r') as file:
        completed_files = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for year in tweetfiles.keys():
            for month in tweetfiles[year].keys():
                save_to_folder = f"data/{year}/{int(month):02d}"
                
                if not os.path.exists(save_to_folder):
                    os.makedirs(save_to_folder)

                for tar_file_url in tweetfiles[year][month].keys():
                    if tar_file_url in completed_files:
                        continue

                    executor.submit(process_tar_file, year, month, tar_file_url)