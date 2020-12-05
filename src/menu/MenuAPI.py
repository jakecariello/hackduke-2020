import requests
from urllib.parse import urlencode
import urllib.parse
import json


BASE_URL = "https://api.documenu.com/v2"
RESTAURANTS = "/restaurants"
headers = {
    'x-api-key': "3ca8e4ce233641f08c7d583b9f074842",
    'x-rapidapi-key': "6b4aa70838msh4638925dda8ae1cp172cb7jsn75c6e15c5956",
    'x-rapidapi-host': "documenu.p.rapidapi.com"
}


def getCoordinates(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return [response[0]["lat"], response[0]["lon"]]



def searchRestaurants(address, radius):
    coords = getCoordinates(address)
    query = urlencode({"lat": coords[0], "lon": coords[1], "distance": radius})
    searchrestaurant_url = BASE_URL + RESTAURANTS + "/search/geo?" + query
    response = requests.request("GET", searchrestaurant_url, headers=headers)
    jsonresponse = json.loads(response.text)
    restaurantdata = jsonresponse["data"]
    restaurant_ids =
    return restaurantdata





#response = requests.request("GET", url, headers=headers)


#restaurant_fields = {"address":"164 Shenstone Blvd Garner, NC 27529"}
print(searchRestaurants("1608 Hall Blvd Garner, NC 27529", 3))