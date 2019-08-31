# This script downloads all GTFS data available on transitfeeds.com via API
# This script is still a work in progress

import csv
import datetime
import json
import os
import requests 
import shutil
import time
import zipfile

# this interaction checks to make sure that the user really wants to delete already existing GTFS data
# I kept accidentally deleting files I wanted -- hence, this step
deleteGTFS = input("Do you want to delete existing GTFS data? Y/N ")
if deleteGTFS.upper() == "Y":
    try:
        shutil.rmtree("gtfs/")
    except FileNotFoundError:
        pass
else:
    pass
    
# download list of agency IDs from transit feeds

listOfAgencyIDs = []
api_key = "94413ac9-aec7-4720-a731-640e98d65763" # this is my API key; replace with your own
r_url = "https://api.transitfeeds.com/v1/getFeeds?key={}&location=67&descendants=1&limit=100".format(api_key)
r = requests.get(r_url)

numPages = r.json()["results"]["numPages"] # capture all gtfs feeds 

for page in range(1,(numPages+1)):
    url = r_url + "&page={}".format(str(page)) # pass page argument to API url
    r = requests.get(url)
    for feed in (r.json()["results"]["feeds"]):
        if feed["ty"] == "gtfs" and feed["id"] not in listOfAgencyIDs:
            listOfAgencyIDs.append(feed["id"]) # append GTFS feed to list of desired feeds

# download zipped GTFS data for each agency
for feed in listOfAgencyIDs:
    url = "https://api.transitfeeds.com/v1/getLatestFeedVersion?key={}&feed={}".format(api_key, feed)
    g = requests.get(url)
    slashRemoval = "--".join(feed.split("/"))
    filename = "{}.zip".format(slashRemoval)
    with open(filename, "wb") as fd:
        for chunk in g.iter_content(chunk_size=128):
            fd.write(chunk)
            
# unzip downloaded GTFS data in a new directory called "gtfs"
for feed in listOfAgencyIDs:
    slashRemoval = "--".join(feed.split("/"))
    path = "{}.zip".format(slashRemoval)
    new_path = "gtfs/{}".format(slashRemoval)
    try:
        zip_ref = zipfile.ZipFile(path, "r")
        zip_ref.extractall(new_path)
        zip_ref.close()
        os.remove(path)
    except:
        print(path)
        os.remove(path)


note_to_write = "downloaded from https://transitfeeds.com on {}".format(str(datetime.date.today()))
with open("gtfs/README.txt", "w") as text_file:
    text_file.write(note_to_write) 
