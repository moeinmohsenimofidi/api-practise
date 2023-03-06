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
city_list = ["Bolzano", "Merano"]

API_KEY = "3781a117fbc24b712b262512ef3e1139"
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
#CALL_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
history_endpoint = "https://history.openweathermap.org/data/3.0/history/timemachine"


#find latitude and longitude for all location in
locations = []
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
        locations.append(lat_lon)
    #for i in range(len(location)):
        #location[i]['city'] = city_list[i]

print(locations)

# start and end epoch time for yesterday

start_epoch = (int(time.time() // 86400)) * 86400 - 86400
end_epoch = (int(time.time() // 86400)) * 86400
print(start_epoch)
local_time = time.gmtime(start_epoch )
print("Local time:", local_time)
print(end_epoch)
local_time = time.gmtime(end_epoch)
print("Local time:", local_time)

print(int(time.time()))

'''
#use history weather API
#data = []
#for location in locations:

history_parameters = {
    "lat": 46.4981125,
    "lon": 11.3547801,
    "dt": start_epoch,
    "appid": API_KEY,

}


history_response = requests.get(url="https://history.openweathermap.org/data/3.0/history/timemachine", params=history_parameters).json()

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
'''