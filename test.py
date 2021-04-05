import requests 
import json

url = "https://5ka.ru/api/v2/categories/"
response = requests.get(url)

data = response.json()

print(1)