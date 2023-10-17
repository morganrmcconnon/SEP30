# JSON files urls of Twitter Stream collection
A collection of urls to the compressed JSON files tweets on the Twitter Stream Archive. https://archive.org/details/twitterstream

## Program
The program includes the `tweet_downloader.py` file, the `url_patterns.json` file.
If you want to use the program, you can just download the `tweet_downloader.py` file and the `url_patterns.json` file.

## How to use this program

You can use this dataset and the functions in `tweet_downloader.py` to scrape tweets from https://archive.org/details/twitterstream

You can use the `get_download_urls` to get the urls of the compressed `.json.bz2` and `.json.gz` files that can contains the tweets in a specific year, month, day, hour, minute.

Then you can use the `read_compressed_json` to download and read the compressed json files.

## Details

The script used to get the urls are in the `downloader_scritps` folder.

In this collection: https://archive.org/details/twitterstream, there are a number of .tar and .zip files that contains the JSON files of tweets. This repository contains a list of urls to these files, stored in `tweetfiles.json`. Those urls are collected using the  `tarfiles.py` script.

In each of those .tar and .zip files, there are a number of .json.bz2 or .json.gz files. The urls to those files are stored in the documents inside the `data` folder in this repository. Those urls are collected using the `jsonfiles.py` script.

**Note:** If the `data` folder is not completed, you can continue completing this dataset by just running the `jsonfiles.py` script.

The `tweetfiles.json` file is a list of urls to the .tar and .zip files in the collection. The `data` folder contains a number of .json.bz2 and .json.gz files urls. The `data` folder is organized in the following way:

```
data
├── <year>
│   ├── <month>
│   │   ├── <tar/zip file>.txt <--- Contains urls to .json.bz2 or .json.gz files 
│   │   ├── <tar/zip file>.txt
```

You can use the `combine_data.py` script to combine all json files in the `data` folder and store them in the `data.json` file. However, the file will be extremely big.

