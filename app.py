import requests
import json

with open('data.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)
    print(fcc_data)
url = 'http://localhost:8000/data'
# data = {'name': 'somevalue'}

x = requests.post(url, json=fcc_data)

print(x.text)