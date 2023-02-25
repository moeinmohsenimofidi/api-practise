import requests
from pprint import pprint as pp
import pandas as pd
import matplotlib.pyplot as plt


baseurl = "https://rickandmortyapi.com/api/"
endpoint = "character"

def main_request(baseurl, endpoint, page_no):
    response = requests.get(baseurl + endpoint + f"?page={page_no}")
    result = response.json()
    return result

def get_pages(response):
    return response["info"]["pages"]

def parse_json(response):
    charlist = []
    for item in response["results"]:
        char ={
            "id": item["id"],
            "name": item["name"],
            "NO_episode": len(item["episode"]),
        }
        charlist.append(char)

    return charlist



data = (main_request(baseurl, endpoint, 1))
mainlist =[]
for x in range(1, get_pages(data) +1):
    mainlist.extend(parse_json(main_request(baseurl, endpoint, x)))

df = pd.DataFrame(mainlist)
df.to_csv("characterlist.csv", index=False)
print(data)