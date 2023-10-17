import json
import bz2
import gzip
from urllib.request import urlopen


def tar_pattern_decrypt(pattern_code, year, month, day):

    regex_tar_patterns_decrypt_str = {
        1: r"twitter-json-scrape-{}-{}.zip",
        2: r"archiveteam-twitter-{}-{}.tar",
        3: r"archiveteam-twitter-stream-{}-{}.tar",
        4: r"archiveteam-twitter-stream-{}-{}-b.tar",
        5: r"twitter-stream-{}-{}-{}.tar",
        6: r"twitter-{}-{}-{}.tar",
        7: r"twitter_stream_{}_{}_{}.tar",
        8: r"twitter-stream-{}-{}-{}.zip",
        9: r"twitter-stream-{}{}{}.tar",
    }

    return regex_tar_patterns_decrypt_str[pattern_code].format(year, month, day)

def bz2_pattern_decrypt(pattern_code, year, month, day, hour, minute):
    regex_bz2_patterns_decrypt_meaning = {
        1: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        2: r"(\d{4})/(\d{2})-b/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        3: r"(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        4: r"(\d{2})/(\d{2})/(\d{2}).json.bz2",
        5: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.gz",
        6: r"(\d{4})(\d{2})(\d{2})/(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})00.json.gz",
    }

    if pattern_code == 1:
        return f"{year}/{month}/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 2:
        return f"{year}/{month}-b/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 3:
        return f"{month}/{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 4:
        return f"{day}/{hour}/{minute}.json.bz2"
    elif pattern_code == 5:
        return f"{year}/{month}/{day}/{hour}/{minute}.json.gz"
    elif pattern_code == 6:
        return f"{year}{month}{day}/{year}{month}{day}{hour}{minute}00.json.gz"
    else:
        return None
    


def format_to_string(year, month, day, hour, minute):
    year = str(year) if year != None else None
    month = f'{int(month):02d}' if month != None else None
    day = f'{int(day):02d}' if day != None else None
    hour = f'{int(hour):02d}' if hour != None else None
    minute = f'{int(minute):02d}' if minute != None else None
    return year, month, day, hour, minute    


def get_download_urls(year, month, day = None, hour = None, minute = None):

    year, month, day, hour, minute = format_to_string(year, month, day, hour, minute)
    
    url_pattern_encrypted_data = json.load(open("url_patterns.json", "r"))

    if(year not in url_pattern_encrypted_data):
        return []
    if(month not in url_pattern_encrypted_data[year]):
        return []
    
    days_list = []
    if(day in url_pattern_encrypted_data[year][month]):
        days_list = [day]
    elif(day == None):
        days_list = url_pattern_encrypted_data[year][month].keys()
    else:
        if("00" not in url_pattern_encrypted_data[year][month]):
            return []
        else:
            days_list = ["00"]

    potential_urls = []

    for day in days_list:

        pattern_codes_list = url_pattern_encrypted_data[year][month][day]

        for pattern_codes in pattern_codes_list:

            # Get tar file name
            tar_pattern_code = pattern_codes[0]
            tar_file = tar_pattern_decrypt(tar_pattern_code[0], year, month, day)

            # Get base url

            if(len(tar_pattern_code) == 3):
                year_folder = tar_pattern_code[1]
                month_folder = tar_pattern_code[2]
            else:
                year_folder = year
                month_folder = month

            base_url = f"https://archive.org/download/archiveteam-twitter-json-2011" if(year_folder == '2011') else f"https://archive.org/download/archiveteam-twitter-stream-{year_folder}-{month_folder}"


            # Get bz2 file name
            bz2_pattern_codes = pattern_codes[1]

            hour_list = [str(h).zfill(2) for h in range(0,24)] if(hour == None) else [hour]
            
            minute_list = [str(m).zfill(2) for m in range(0,60)] if(minute == None) else [minute]

            for bz2_pattern_code in bz2_pattern_codes:
                for hour_ in hour_list:
                    for minute_ in minute_list:
                        bz2_file = bz2_pattern_decrypt(bz2_pattern_code, year, month, day, hour_, minute_)
                        potential_urls.append(f"{base_url}/{tar_file}/{bz2_file}")


    return potential_urls




def read_compressed_json(url):
    # try:
        with urlopen(url) as response:
            if url.endswith('.json.bz2'):
                with bz2.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            elif url.endswith('.json.gz'):
                with gzip.open(response, 'rt', encoding='utf-8') as file:
                    data = [json.loads(line) for line in file.readlines()]
            else:
                raise ValueError("Unsupported file format. Only .json.bz2 and .json.gz are supported.")

        return data

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None

# Example usage

def get_tweets(year, month, day = None, hour = None, minute = None):
    urls = get_download_urls(year, month, day, hour, minute)
    json_data = {}
    for url in urls:
        json_data[url] = read_compressed_json(url)
    return json_data
