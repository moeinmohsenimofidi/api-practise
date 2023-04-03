import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import pyproj
import rasterio
import time
import pytz
import json


openweatherKey = "702aaee7581400652b3e4dca17874e95"
END_POINT = "http://api.openweathermap.org/geo/1.0/reverse"
input_file = "Custom_location_46_4423_11_2525_63fc88e098a8260007094a1e.json"


params ={
    "lat": 46.4423,
    "lon": 11.2525,
    "appid": openweatherKey
}

elements = [
        {"name": "temp", "type": "LT", "unit": "\u00b0C", "description": "Lufttemperatur"},
        {"name": "temp_min", "type": "MinT", "unit": "\u00b0C", "description": "Mindest Temperatur"},
        {"name": "temp_max", "type": "MaxT", "unit": "\u00b0C", "description": "maximale Temperatur"},
        {"name": "feels_like","type": "GL","unit": "\u00b0C","description": "Gef\u00fchl Lufttemperatur",},
        {"name": "pressure", "type": "LD.RED", "unit": "hPa", "description": "Luftdruck"},
        {"name": "dew_point","type": "AT","unit": "\u00b0C","description": "Atmosph\u00e4rische Temperatur",},
        {"name": "clouds", "type": "T", "unit": "%", "description": "Tr\u00fcbung"},
        {"name": "visibility", "type": "S", "unit": "m", "description": "Sichtbarkeit"},
        {"name": "rain", "type": "HR", "unit": "cm", "description": "Regenh\u00f6he"},
        {"name": "snow", "type": "HS", "unit": "cm", "description": "Schneeh\u00f6he"},
        {"name": "precipitation", "type": "N", "unit": "mm", "description": "Niederschlag"},
        {"name": "humidity","type": "LF","unit": "%","description": "relative Luftfeuchte",},
        {"name": "wind_speed","type": "WG","unit": "m/s","description": "Windgeschwindigkeit",},
        {"name": "wind_deg","type": "WR","unit": "\u00b0 ","description": "Windrichtung",},
        {"name": "wind_gust","type": "WG.BOE","unit": "m/s","description": "Windgeschwindigkeit B\u00f6e",},
    ]


def format_transform(lat, lon):
    """Return list of latitude and longitude of the Spherical/Web Mercator format from EPSG:4326 to EPSG:3857"""
    tran_4326_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857")
    lat, lon = tran_4326_to_3857.transform(lat, lon)
    return [lat, lon]


def get_altitude(lat, lon):
    """ Return float value as altitude for the requested latitude and longitude
         """
    with rasterio.open("dtm_100.tif") as src:
        # Get the image transform
        transform = src.transform
        # Get the image data as a NumPy array
        data = src.read(1)
    df = pd.DataFrame(data)
    #change Spherical/Web Mercator format from EPSG:4326 to EPSG:32632
    tran_4326_to_3857 = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32632")
    latitude, longitude = tran_4326_to_3857.transform(lat, lon)

    col, row = ~transform * (latitude, longitude)
    # Round the pixel coordinates to the nearest integer
    col, row = int(round(col)), int(round(row))
    altitude = df.iloc[row, col]
    return int(round(altitude))


def json_transform(data):


    # Manipulate the row data with intend of provide the needed structure
    # and save each parameter separately in JSON files

    for element in elements:
        result = {}
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        coordinates = format_transform(lat, lon)
        altitude = get_altitude(lat, lon)
        response = requests.get(END_POINT, params=params).json()
        city_name = response[0]["local_names"]["it"]
        for item in data:
            city = city_name
            if city not in result:
                result[city] = {
                    "id": "",
                    "name": city,
                    "altitude": altitude,
                    "coordinates": [coordinates[0], coordinates[1]],
                    "sensor": {
                        "type": element["type"],
                        "unit": element["unit"],
                        "description": element["description"],
                        "data_points": [],
                    },
                }
            data_points = item
            result[city]["sensor"]["data_points"].append(data_points)

        output = list(result.values())

        # Extract the timestamp and value for each item
        for item in output:
            for i in range(10):  # (len(item["sensor"]["data_points"])):
                dt = item["sensor"]["data_points"][i]["dt"]
                timestamp = datetime.utcfromtimestamp(dt).isoformat()
                # Checking the availability of rain, snow and wind_gust information and extract them

                if element["name"] == "temp":
                    value = item["sensor"]["data_points"][i][0][element["name"]]
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": str(value),
                    }

                elif element["name"] == "rain":
                    weather_id = item["sensor"]["data_points"][i]["weather"][0]["id"]
                    if weather_id >= 500 and weather_id <= 531:
                        value = item["sensor"]["data_points"][i][element["name"]]["1h"]
                    else:
                        value = 0
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }

                elif element["name"] == "snow":
                    weather_id = item["sensor"]["data_points"][i]["weather"][0]["id"]
                    if weather_id >= 600 and weather_id <= 622:
                        value = item["sensor"]["data_points"][i][element["name"]]["1h"]
                    else:
                        value = 0
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }
                elif element["name"] == "precipitation":
                    try:
                        weather_id = item["sensor"]["data_points"][i]["weather"][0]["id"]
                        if weather_id >= 500 and weather_id <= 531:
                            rain = item["sensor"]["data_points"][i][element["name"]]["1h"]
                        else:
                            rain = 0
                        if weather_id >= 600 and weather_id <= 622:
                            snow = item["sensor"]["data_points"][i][element["name"]]["1h"]
                        else:
                            snow = 0
                        value = rain + snow
                    except:
                        value = 0
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }
                elif element["name"] == "clouds":
                    try:
                        value = item["sensor"]["data_points"][i][element["name"]["all"]]
                    except:
                        value = 0

                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }

                elif element["name"] == "wind_speed":
                    value = item["sensor"]["data_points"][i]["wind"]["speed"]
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }
                elif element["name"] == "wind_deg":
                    value = item["sensor"]["data_points"][i]["wind"]["deg"]
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }

                elif element["name"] == "wind_gust":
                    try:
                        value = item["sensor"]["data_points"][i]["wind"][element["name"]]
                    except:
                        value = 0

                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }
                elif element["name"] == "visibility":
                    try:
                        value = item["sensor"]["data_points"][i][element["name"]]
                    except:
                        value = 0
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }

                else:
                    value = item["sensor"]["data_points"][i]["main"][element["name"]]
                    item["sensor"]["data_points"][i] = {
                        "timestamp": timestamp,
                        "value": value,
                    }

        # Allocating the unique ID to each station and save each element separately
        structured_json = {"data": {"coordinate_system": "EPSG:3857", "stations": output}}
        for i, station in enumerate(structured_json["data"]["stations"]):
            station["id"] = f"OW{i + 1}"


        # Change the timestamp format from UTC to local format (CET)
        cet = pytz.timezone("CET")
        for station in structured_json["data"]["stations"]:
            for data_point in station["sensor"]["data_points"]:
                timestamp = datetime.fromisoformat(data_point["timestamp"])
                timestamp_cet = cet.localize(timestamp)
                data_point["timestamp"] = timestamp_cet.strftime("%Y-%m-%dT%H:%M:%S%Z")

    return structured_json
'''
        # write the all element information in separate json file
        if not os.path.exists(f"{element['description']}"):
            os.makedirs(f"{element['description'].title()}")
        with open(f'{element["description"]}/{date}.json', "w") as f:
            json.dump(structured_json, f)
'''




with open(input_file, 'r') as input_f:
    data = json.load(input_f)

converted_json = json_transform(data)
for element in elements:
    daily_data = {}
    for item in converted_json:
        date = item["data"]["stations"][0]["sensor"]["data_points"]["timestamp"].split("T")[0]
        if date not in daily_data:
            daily_data[date] = []
        daily_data[date].append(item)
    
    # Write each group to a separate file with title as same as the description of file
    
        if not os.path.exists(f"daily_historic_elements/{element['description']}"):
            os.makedirs(f"daily_historic_elements/{element['description'].title()}")
        for date, items in daily_data.items():
            with open(f'daily_historic_elements/{element["description"]}/{date}.json', 'w') as file:
                json.dump(items, file)


