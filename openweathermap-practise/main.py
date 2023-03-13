import requests
from datetime import datetime, time
import time
import json



# start and end epoch time for yesterday

epoch_time = (int(time.time() // 86400)) * 86400 - 86400
end_epoch = (int(time.time() // 86400)) * 86400
print(epoch_time)
print(end_epoch)

current_time = int(time.time())
'''
# List of points extracted from the map

city_list = ["Graun im vinschgau","Maso corto","Mals","stilfs","Laas","Schlanders",
             "Ultimo-Ulten","Terlan","Bolzano","Laives","Caldaro sulla Strada del vino",
             "Welschnofen","Renon-Ritten","Kastelruth","Urtijei","Selva","Corvara",
             "Abtei-Badia","Sexten","Toblach","Olang","St.Lorenzen","Gais","Valle Aurina-Ahrntal",
             "Prettau","San Giacomo","Vandoies-Vintl","Brixen","Sterzing","Ratschings",
             "St.Leonhard in Passeier","Pennes","Valdurna","Sarnthein","Merano","Algund",
             "Partschins","Naturns"]
'''

# test cities
tesCities = ["Bolzano", "Merano"]


openweatherKey = ""
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
HISTORIC_URL = f"http://api.openweathermap.org/data/3.0/onecall/timemachine"


# script for find latitude and longitude for all location in the map

def epoch_time():
    return int(time.time() // 86400) * 86400 - 86400


def find_location(cities):
    locations = []
    for city in cities:
        geo_parameters = {"q": f"{city},IT", "appid": openweatherKey}
        geo_response = requests.get(GEOCODE_ENDPOINT, params=geo_parameters).json()
        for item in geo_response:
            lat_lon = {
                "city": item["name"],
                "lat": item["lat"],
                "lon": item["lon"]
                }
            locations.append(lat_lon)
    return locations



def get_historic_data(cities_location):
    epochTime = epoch_time()
    historic_data = []
    temp =[]
    for city in cities_location:
        baseTime = epochTime
        while baseTime <= time.time():
            parameters = {
                "lat": city["lat"],
                "lon": city["lon"],
                "dt": baseTime,
                "lang": "en",
                "units": "metric",
                "appid": openweatherKey,
            }
            response = requests.get(HISTORIC_URL, params=parameters).json()
            for item in response:
                '''history_response ={
                    "city": city,
                    "data_point": item["data"]
                }'''
                historic_data.append(history_response)
                baseTime += 600

    return historic_data

print(epoch_time())


data = get_historic_data(find_location(tesCities))
print(data)


