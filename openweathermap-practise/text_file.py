import json
import datetime as datetime

with open('historic_data', "r") as f:
    json_data = json.load(f)
print(json_data)

for item in json_data:
    lat = item["lat"]
    lon = item["lon"]
    dt = item["data"][0]["dt"]
    value = item["data"][0]["temp"]
    timestamp = datetime.datetime.utcfromtimestamp(dt).isoformat()

    print(f'{lat}\t{lon}\t{timestamp}\t{value}')