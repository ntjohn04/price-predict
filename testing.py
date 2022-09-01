import requests
import json
import pandas as pd


headers = {
    'accept': 'application/json',
}

params = {
    'key': '62ba0e9adc5dd1cfcc0d290c',
}

responset = requests.get('https://backpack.tf/api/IGetPrices/v4?raw=1&key=62ba0e9adc5dd1cfcc0d290c', params=params, headers=headers)



with open('apidata.json', 'w') as f:
    json.dump(responset.json(), f)

