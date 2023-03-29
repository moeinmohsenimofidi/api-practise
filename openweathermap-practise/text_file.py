import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import pyproj
import time
import pytz
import json
import rasterio



# List of extracted points from the map
city_list = [
    "Graun im Vinschgau",
    "Maso Corto",
    "Mals",
    "Stilfs",
    "Laas",
    "Schlanders",
    "Ultimo - Ulten",
    "Terlan",
    "Bolzano",
    "Laives",
    "Caldaro sulla Strada del Vino",
    "Welschnofen",
    "Renon - Ritten",
    "Kastelruth",
    "Urtijei",
    "Selva",
    "Corvara",
    "Abtei-Badia",
    "Sexten",
    "Toblach",
    "Olang",
    "St. Lorenzen",
    "Gais",
    "Valle Aurina - Ahrntal",
    "Prettau",
    "San Giacomo",
    "Vandoies - Vintl",
    "Brixen",
    "Sterzing",
    "Ratschings",
    "St. Leonhard in Passeier",
    "Pennes",
    "Valdurna",
    "Sarnthein",
    "Merano",
    "Algund",
    "Partschins",
    "Naturns",
]


# test cities
testCities = ["bolzano"]


openweatherKey = "702aaee7581400652b3e4dca17874e95"
GEOCODE_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"
HISTORIC_URL = "http://api.openweathermap.org/data/3.0/onecall/timemachine"


# variables that need for convert the timezone and find EPSG:3857 coordinate parameters


"""
scripts for find latitude and longitude for all location in the map
"""


# Get the epoch time for yesterday start
def epoch_time():
    """Return the second as int
    this calculate the start of yesterday -> 00:00:00
    """
    return int(time.time() // 86400) * 86400 - 86400


def end_time():
    """Return the second as int
    this calculate the end of yesterday -> 24:00:00
    """
    return int(time.time() // 86400) * 86400


# Convert the time extracted from Openweather (dt) to the time format that use in the project Data base
def epoch_to_isoformat(dt):
    """Return date in the standard format YYYY-MM-DDTHH:MM:SS"""
    return datetime.utcfromtimestamp(dt).isoformat()

def find_location(cities):
    """Return geographical coordinates (lat, lon) by using name of the location (city name or area name)
    from the list of the Location
    """

    locations = []
    for city in cities:
        geo_parameters = {"q": f"{city},IT", "appid": openweatherKey}
        geo_response = requests.get(GEOCODE_ENDPOINT, params=geo_parameters).json()
        for item in geo_response:
            lat_lon = {"city": item["name"], "lat": item["lat"], "lon": item["lon"]}
            locations.append(lat_lon)
    return locations


def mytransform(lat, lon):
    """Return list of latitude and longitude of the Spherical/Web Mercator format from EPSG:4326 to EPSG:3857"""
    tran_4326_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857")
    lat, lon = tran_4326_to_3857.transform(lat, lon)
    return [lat, lon]




def get_altitude(lat, long):
    """Return altitude as float value
        """
    with rasterio.open('dtm_100.tif') as src:
        # Get the CRS and transform of the TIF file
        crs = src.crs
        transform = src.transform

        # Convert the latitude and longitude to the TIF file's coordinate system
        x, y = rasterio.transform.xy(transform, long, lat)

        # Read the altitude value for the given location
        row, col = src.index(x, y)
        altitude = src.read(1, window=((row, row + 1), (col, col + 1)))[0][0]

        # Convert the altitude value to a Pandas DataFrame
        df = pd.DataFrame(np.array([[elevation]]), columns=['altitude'])

    return altitude



# Find the latitude and longitude for cities in the list



# get the weather information from yesterday start for the 10 minutes intervals
def get_historic_data(cities_location, interval: int):
    """Return the yesterday weather information for each location in the list regarding the needed interval"""

    base_time = epoch_time()
    historic_data = []
    for city in cities_location:
        baseTime = base_time
        while baseTime <= end_time():
            parameters = {
                "lat": city["lat"],
                "lon": city["lon"],
                "dt": baseTime,
                "lang": "en",
                "units": "metric",
                "appid": openweatherKey,
            }
            history_response = requests.get(HISTORIC_URL, params=parameters).json()
            data = {
                "city": city["city"],
                "data_point": history_response,
            }
            historic_data.append(data)
            baseTime += interval * 60
    return historic_data


# Save the row weather information for the all station

with open('historic_data.json', "w") as f:
    json.dump(get_historic_data(find_location(testCities), 10), f)

'''
with open("historic_data.json") as json_file:
    data = json.load(json_file)

elements = [
    {"name": "temp", "type": "LT", "unit": "\u00b0C", "description": "Lufttemperatur"},
    {"name": "feels_like", "type": "GL", "unit": "\u00b0C", "description": "Gef\u00fchl Lufttemperatur"},
    {"name": "pressure", "type": "LD.RED", "unit": "hPa", "description": "Luftdruck"},
    {"name": "dew_point", "type": "AT", "unit": "\u00b0C", "description": "Atmosph\u00e4rische Temperatur"},
    {"name": "clouds", "type": "T", "unit": "%", "description": "Tr\u00fcbung"},
    {"name": "uvi", "type": "UVi", "unit": "nm", "description": "UV-Index"},
    {"name": "rain", "type": "HR", "unit": "cm", "description": "Regenh\u00f6he"},
    {"name": "snow", "type": "HS", "unit": "cm", "description": "Schneeh\u00f6he"},
    {"name": "humidity", "type": "LF","unit": "%","description": "relative Luftfeuchte"},
    {"name": "wind_speed", "type": "WG", "unit": "m/s", "description": "Windgeschwindigkeit"},
    {"name": "wind_deg", "type": "WR", "unit": "\u00b0 ", "description": "Windrichtung"},
    {"name": "wind_gust", "type": "WG.BOE", "unit": "m/s", "description": "Windgeschwindigkeit B\u00f6e"},


]


# Manipulate the row data with intend of provide the needed structure
# and save each parameters separately in JSON files

for element in elements:
    result = {}
    for item in data:
        city = item["city"]
        if city not in result:
            id = 1
            coordinate = mytransform(
                item["data_point"]["lat"], item["data_point"]["lon"]
            )
            altitude = get_altitude(item["data_point"]["lat"], item["data_point"]["lon"])
            #write the function to find the altitude aqnd add it here
            result[city] = {
                "id": "",
                "name": city,
                "altitude": altitude,
                "coordinate": [coordinate[0], coordinate[1]],
                "sensor": {
                    "type": element["type"],
                    "unit": element["unit"],
                    "description": element["description"],
                    "data_points": [],
                },
            }
        data_points = item["data_point"]["data"]
        result[city]["sensor"]["data_points"].append(data_points)

    output = list(result.values())


    # Extract the timestamp and value for each item
    for item in output:
        for i in range(len(item["sensor"]["data_points"])):
            dt = item["sensor"]["data_points"][i][0]["dt"]
            timestamp = datetime.utcfromtimestamp(dt).isoformat()

            #Checking the availability of rain, snow and wind_gust information and extract them

            if element["name"] == "rain":
                weather_id = item["sensor"]["data_points"][i][0]["weather"][0]["id"]
                if weather_id >= 500 and weather_id <= 531 :
                    value = item["sensor"]["data_points"][i][0][element["name"]]["1h"]
                else:
                    value = 0
                item["sensor"]["data_points"][i] = {
                    "timestamp": timestamp,
                    "value": value,
                }

            elif element["name"] == "snow":
                weather_id = item["sensor"]["data_points"][i][0]["weather"][0]["id"]
                if weather_id >= 600 and weather_id <= 622 :
                    value = item["sensor"]["data_points"][i][0][element["name"]]["1h"]
                else:
                    value = 0
                item["sensor"]["data_points"][i] = {
                    "timestamp": timestamp,
                    "value": value,
                }

            elif element["name"] == "wind_gust":

                try:
                    value = item["sensor"]["data_points"][i][0][element["name"]]
                except:
                    value = 0

                item["sensor"]["data_points"][i] = {
                    "timestamp": timestamp,
                    "value": value,
                }

            else:
                value = item["sensor"]["data_points"][i][0][element["name"]]
                item["sensor"]["data_points"][i] = {
                    "timestamp": timestamp,
                    "value": value,
                }


    # Allocating the unique ID to each station
    structured_json = {"data": {"coordinate_system": "EPSG:3857", "stations": output}}
    for i, station in enumerate(structured_json["data"]["stations"]):
        station["id"] = f"OW{i+1}"

    # Change the timestamp format from UTC to local format (CET)

    cet = pytz.timezone("CET")
    for station in structured_json["data"]["stations"]:
        for data_point in station["sensor"]["data_points"]:
            timestamp = datetime.fromisoformat(data_point["timestamp"])
            timestamp_cet = cet.localize(timestamp)
            data_point["timestamp"] = timestamp_cet.strftime("%Y-%m-%dT%H:%M:%S%Z")

    # write the all element information in seperate json file

    with open(f'{element["name"]}.json', "w") as f:
        json.dump(structured_json, f)

'''
'''

#Read elements json and Plot each element based on all stations
for item in elements:

    data = json.load(open(f"{item['name']}.json", "r"))
    fig, ax = plt.subplots()
    stations = data["data"]["stations"]

    # iterate over stations and plot data
    for station in stations:
        name = station["name"]
        timezone = "CET"
        data_points = station["sensor"]["data_points"]
        times = []
        values = []
        for data_point in data_points:
            time = datetime.fromisoformat(data_point["timestamp"][:-3])
            times.append(time)
            values.append(data_point["value"])
        ax.plot(times, values, label=name)

    # set x-axis label to current timezone and rotate the x-axis label
    timezone_label = pytz.timezone("CET").tzname(datetime.now(pytz.timezone("CET")))
    ax.set_xlabel(f"Timezone: {timezone_label}")
    plt.xticks(rotation=45)

    # add legend, save all plots in Figs folder and show plot
    ax.legend(loc="upper right")
    plt.connect("pick_event", lambda event: print(event))
    plt.savefig(f"Figs/{item['name']}.png")
    #plt.show()
'''
# Open the TIF file using rasterio
