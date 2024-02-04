import requests

# replace the "demo" apikey below with your own key
url = "https://mboum.com/api/v1/ne/news/?symbol=AAPL&apikey=demo"
r = requests.get(url)
data = r.json()

print(data)