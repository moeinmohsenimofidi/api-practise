import json
import sys
from pprint import pprint as pp
import pandas as pd
import requests

print(sys.executable)
response = requests.get(
    "http://dati.retecivica.bz.it/services/kksSearch/collect/select?q=*:*&fl=*&rows=36&wt=json"
).json()
print(response)
