import datetime
import requests

import pandas as pd

from typing import List

def check_latest(row):
    agencyId = row[0]
    latest = row[5]
    
    if type(latest) != float:
        ts = latest["ts"]
    else:
        ts = int(datetime.datetime.timestamp(datetime.datetime.now()))
    return {"id" : agencyId, "latest" : ts}

def get_agency_updates(api_key : str) -> List:
	
	# getFeeds endpoint provides the locations of all eligible GTFS feeds
	r_url = f"https://api.transitfeeds.com/v1/getFeeds?key={api_key}&location=67&descendants=1&limit=100"
	r = requests.get(r_url)
	j = r.json()

	responseData = pd.DataFrame(j["results"]["feeds"])

	agencies = list(responseData.apply(check_latest, axis=1))

	# TransitFeeds only allows up to 100 feeds to be returned on a single page (or by a single call)
	# Knowing the number of pages informs how many times we need to hit the endpoint
	number_of_pages = j["results"]["numPages"]

	if number_of_pages > 1:
		for page in range(2,number_of_pages+1):

			r_url = f"https://api.transitfeeds.com/v1/getFeeds?key={api_key}&location=67&descendants=1&limit=100"
			r = requests.get(r_url)
			j = r.json()

			responseData = pd.DataFrame(j["results"]["feeds"])

			agencies += list(responseData.apply(check_latest, axis=1))
	else:
		pass

	agencyUpdateTable = pd.DataFrame(agencies).drop_duplicates()
	agencyUpdateTable.to_json("current.json", orient="records")

def compare_update_times():

	current = pd.read