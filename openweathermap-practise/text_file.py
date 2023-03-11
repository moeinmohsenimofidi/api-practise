import json
import datetime as datetime

with open('historic_data', "r") as f:
    data = json.load(f)

# create new list with city and data points
result = {}
weather_data = []
for item in data:
    city = item['city']
    if city not in result:
        result[city] = {'id': "",
                        'city': city,
                        'altitude': "",
                        'coordinate': ["","",""],
                        'sensor':{"type":"LT",
                                  "unit": "°c",
                                  "description": "Lufttemperatur",
                                  "data_points": []}
                        }
    data_points = item['data_point']['data']
    result[city]["sensor"]['data_points'].append(data_points)
output_list = list(result.values())
for i in range(len(output_list)):
    for item in output_list:
        dt = item["sensor"]["data_points"][i][0]["dt"]
        timestamp = datetime.datetime.utcfromtimestamp(dt).isoformat()
        value = item["sensor"]["data_points"][i][0]["temp"]
        item["sensor"]["data_points"][i] = {"timestamp": timestamp,
                                            "value": value}

structured_json = {"data": {"coordinate_system": "EPSG:3857",
                           "stations": output_list}}
print(structured_json)
