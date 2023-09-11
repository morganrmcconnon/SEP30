def get_url_pattern_code(year, month, day, hour, minute):
    '''
    Returns the url pattern code for a given time.
    '''

    year = int(year) if year != None else None
    month = int(month) if month != None else None
    day = int(day) if day != None else None
    hour = int(hour) if hour != None else None
    minute = int(minute) if minute != None else None


    if year == 2011 and month >= 9:
        return (1,1)
    
    if year == 2012:
        return (2,1) if month <= 12 else (2,3)

    if (((2013, 1) <= (year, month) and (year, month) <= (2013, 8))
    or ((2014, 2) <= (year, month) and (year, month) <= (2014, 9))
    or ((2016, 8) <= (year, month) and (year, month) <= (2017, 1))
    ):
        return (3,3)
    
    if ((year, month, day, hour) == (2016, 8, 8, 8)):
        return (3,5)
    
    if (((2013, 9) <= (year, month) and (year, month) <= (2013, 12))
    or ((2014, 10) <= (year, month) and (year, month) <= (2016, 6))
    or ((2017, 2) <= (year, month) and (year, month) <= (2017, 6))
    or ((2018, 1) <= (year, month) and (year, month, day) <= (2018, 4, 23))
    or ((year, month) == (2016, 7))
    ):
        return (3,1)
    
    if ((year, month) == (2017, 12)):
        return (5, 1, 2017, 11)
    
    if ((2017, 7) <= (year, month) and (year, month) <= (2017, 11)):
        return (5, 1)
        
    if ((2018, 4, 24) <= (year, month, day) and (year, month, day) <= (2018, 10, 31)):
        return (6, 1)

    if ((year, month) == (2019, 9)):
        return (7, 4, 2019, 8)
    
    if ((2019, 10) <= (year, month) and (year, month) <= (2019, 12)):
        return (7, 4, 2018, month)

    if ((2018, 11) <= (year, month) and (year, month) <= (2020, 2)):
        return (7, 4)
    
    if ((2020, 3) <= (year, month) and (year, month) <= (2020, 6)):
        return (7, 3)
    
    if ((2020, 7) <= (year, month) and (year, month) <= (2021, 8)):
        return (8, 1)
    
    if ((2021, 8) <= (year, month) and (year, month) <= (2022, 11)):
        return (9, 6)
    
    else:
        return None
    

def tar_pattern_decrypt(pattern_code, year : str, month :str, day : str):

    year = str(year) if year != None else None
    month = f'{int(month):02d}' if month != None else None
    day = f'{int(day):02d}' if day != None else None

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
    regex_bz2_patterns_decrypt_meaning = { # not using this, but keeping it here for reference
        1: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        2: r"(\d{4})/(\d{2})-b/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        3: r"(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.bz2",
        4: r"(\d{2})/(\d{2})/(\d{2}).json.bz2",
        5: r"(\d{4})/(\d{2})/(\d{2})/(\d{2})/(\d{2}).json.gz",
        6: r"(\d{4})(\d{2})(\d{2})/(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})00.json.gz",
    }

    year = str(year) if year != None else None
    month = f'{int(month):02d}' if month != None else None
    day = f'{int(day):02d}' if day != None else None
    hour = f'{int(hour):02d}' if hour != None else None
    minute = f'{int(minute):02d}' if minute != None else None
    

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
 

def get_download_url(year, month, day, hour, minute):
    '''
    Returns the url to download the jsonl file for a given time.

    The time range is from 2011-09-01 00:00:00 to 2022-11-22 23:59:00.

    Be aware that the filename with the year, month, day, hour and minute in the name does not necessarily contain the actual tweets posted at that time.
    '''

    pattern_codes = get_url_pattern_code(year, month, day, hour, minute)
    
    if pattern_codes == None:
        return None
    
    tar_file = tar_pattern_decrypt(pattern_codes[0], year, month, day)
    bz2_file = bz2_pattern_decrypt(pattern_codes[1], year, month, day, hour, minute)

    if(len(pattern_codes) == 3):
        year_folder = str(pattern_codes[2])
        month_folder = str(pattern_codes[3])
    else:
        year_folder = str(year)
        month_folder = str(month)

    base_file = f"archiveteam-twitter-json-2011" if(year_folder == '2011') else f"archiveteam-twitter-stream-{year_folder}-{month_folder}"

    return f"https://archive.org/download/{base_file}/{tar_file}/{bz2_file}"


