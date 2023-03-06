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
test_cities = ["Bolzano", "Merano"]


API_KEY = "702aaee7581400652b3e4dca17874e95"
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
#history_endpoint = f"http://api.openweathermap.org/data/3.0/onecall/timemachine?lat=39.099724&lon=-94.578331&units=metric&dt={start_epoch}&appid={API_KEY}"


# script for find latitude and longitude for all location in the map


def find_location (cities):
    locations = []
    for city in cities:
        geocode_parameters = {
            "q": f"{city},IT",
            "appid": API_KEY
        }
        geo_response = requests.get(GEOCODE_ENDPOINT, params=geocode_parameters).json()
        for item in geo_response:
            lat_lon = {
                "city": item["name"],
                "lat": item["lat"],
                "lon": item["lon"]
            }
        locations.append(lat_lon)
    return locations

cities_location = find_location(test_cities)
base_time = (int(time.time() // 86400)) * 86400 - 86400
weather_data = []
for city in cities_location:
    print(city)
    lat = city["lat"]
    lon = city["lon"]
    while base_time <= 1677975000:
        print("#")
        history_url = f"http://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&units=metric&dt={epoch_time}&appid={API_KEY}"
        history_response = requests.get(history_url).json()
        weather_data.append(history_response)
        base_time += 600
