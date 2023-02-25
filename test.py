from http import client

import requests
import pandas as pd
import time
from pprint import pprint as pp
import json
from operator import itemgetter
from httplib2 import auth





PAGE_TOKEN =""
API_KEY = "AIzaSyCVn30zAVbkG5GiJ7bV2nyeVU-agTnByaw"
CHANNEL_ID ="UCfM3zsQsOnfWNUppiycmBuw"
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

search_parameters = {
    "key" : API_KEY,
    "channelId":CHANNEL_ID,
    "part": "snippet,id",
    "order": "date",
    "maxResults": 50,
}
result = list()

def search(url, parameters):
    response = requests.get(url, params=parameters).json()

    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            title = item["snippet"]["title"]
            description = item["snippet"]["description"]
            p_date = item["snippet"]["publishTime"].split("T")[0]
            if description == "":
                description = "Description is not Available"
            data = {
                    #"id": y_id,
                    "title": title,
                    "description": description,
                    "publishDate": p_date,
                }
            result.append(data)
    sorted_data = json.dumps(sorted(result, key=itemgetter("publishDate")), indent=2)
    print(result)

search(SEARCH_URL, search_parameters)
print("/"*20)


