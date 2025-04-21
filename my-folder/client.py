import requests

API_URL = "http://35.239.220.200:5000/api/time"
TOKEN = "supersecrettoken123"
CITY = "Tokyo"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

params = {
    "city": CITY
}

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Failed:", response.status_code, response.text)
