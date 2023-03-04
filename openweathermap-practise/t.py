#Note! For the code to work you need to replace all the placeholders with
#Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = "7c4eee685c6df3c00bad590475c14e5d"


weather_params = {
    "lat": "46.4981125",
    "lon": "11.3547801",
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid=8b1babc59e527ddcd3d9a62f863bfd77")
weather_data = response.json()
print(weather_data)
#weather_slice = weather_data["hourly"][:12]



