import pandas as pd
import requests
from datetime import datetime, time, timedelta
import time
import json


"""'
city_list = ["Graun im vinschgau","Maso corto","Mals","stilfs","Laas","Schlanders",
             "Ultimo-Ulten","Terlan","Bolzano","Laives","Caldaro sulla Strada del vino",
             "Welschnofen","Renon-Ritten","Kastelruth","Urtijei","Selva","Corvara",
             "Abtei-Badia","Sexten","Toblach","Olang","St.Lorenzen","Gais","Valle Aurina-Ahrntal",
             "Prettau","San Giacomo","Vandoies-Vintl","Brixen","Sterzing","Ratschings",
             "St.Leonhard in Passeier","Pennes","Valdurna","Sarnthein","Merano","Algund",
             "Partschins","Naturns"]
"""


API_KEY = "3781a117fbc24b712b262512ef3e1139"
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
#CALL_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
history_endpoint = "https://history.openweathermap.org/data/2.5/history"

"""'
#find latitude and longitude for all location in
location = []
for city in city_list:
    geocode_parameters = {
        "q": f"{city},IT",
        "appid": API_KEY,
    }
    geo_response = requests.get(GEOCODE_ENDPOINT, params=geocode_parameters).json()

    for item in geo_response:
        lat_lon = {
            "city": item["name"],
            "lat": item["lat"],
            "lon": item["lon"],
        }
        location.append(lat_lon)
    #for i in range(len(location)):
        #location[i]['city'] = city_list[i]

print(location)
"""
# start and end epoch time for yesterday

start_epoch = (int(time.time() // 86400)) * 86400 - 86400
end_epoch = (int(time.time() // 86400)) * 86400
print(start_epoch)
local_time = time.gmtime(start_epoch )
print("Local time:", local_time)
print(end_epoch)
local_time = time.gmtime(end_epoch)
print("Local time:", local_time)



#use history weather API
"""data = []
#for loc in location:
history_parameters = {
    #"q": loc["city"],
    "q": "Bolzano,IT",
    "type": "hour",
    "appid": API_KEY,
    "start": 1677801600,
    "end": 1677888000,
}
history_response = requests.get(history_endpoint, params=history_parameters).json()
#data.append(history_response)
"""
history_response = requests.get(
    f"https://history.openweathermap.org/data/2.5/history/city?q=Bolzano,IT&type=hour&start=start_df&cnt=3&appid=3781a117fbc24b712b262512ef3e1139"
).json()

print(history_response)


"""
weather_data = []
for i in range(len(city_location)):
    call_parameters = {
        "lat": city_location[i]["lat"],
        "lon": city_location[i]["lon"],
        "appid": API_KEY,
        "exclude": "current"
    }

    call_response = requests.get(CALL_ENDPOINT, params=call_parameters).json()
    weather_data.append(call_response)
print(weather_data)
"""
