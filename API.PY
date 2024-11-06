import requests

url = "https://api.cricapi.com/v1/currentMatches"
params = {
    "apikey": "2b50724f-4f36-43ee-93aa-2d6850898612",
    "offset": 0
}

response = requests.get(url, params=params)
data = response.json()

# Displaying the data structure
print(data)