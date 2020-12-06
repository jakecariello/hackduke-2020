import requests
from urllib.parse import urlencode
import urllib.parse
import json
import config


BASE_URL = "https://api.documenu.com/v2"
RESTAURANTS = "/restaurants"
RESTAURANT = "/restaurant"
MENU_ITEMS = "/menuitems"
SEARCH_GEO = "/search/geo?"
API_KEY = config.DOCUMENU_API_KEY

headers = {
    "x-api-key": API_KEY
}


"""
RETURNS: latitude and longitude of an address
"""
def getCoordinates(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return response[0]["lat"], response[0]["lon"]

"""
RETURNS: A list of restaurant id's within 'radius' miles of 'address'
"""
def searchRestaurants(address, radius):
    coords = getCoordinates(address)
    query = urlencode({"lat": coords[0], "lon": coords[1], "distance": radius, "fullmenu": ""})
    searchrestaurant_url = BASE_URL + RESTAURANTS + SEARCH_GEO + query
    response = requests.request("GET", searchrestaurant_url, headers=headers)
    print(response.text)
    jsonresponse = json.loads(response.text)
    rest_ids = list()
    # while True:
    #     for restaurant in jsonresponse["data"]:
    #         rest_ids.append(restaurant['restaurant_id'])
    #     if jsonresponse["more_pages"] is True:
    #         nextpage = int(jsonresponse["page"]) + 1
    #         jsonresponse = getPageOfRequest(searchrestaurant_url, nextpage)
    #     else:
    #         break
    return rest_ids

"""
RETURNS: json file of the 'page' page in the documenu request given
"""
def getPageOfRequest(request_url, page):
    request_url += "&page=" + str(page)
    response = requests.request("GET", request_url, headers=headers)
    return json.loads(response.text)


def getRestaurantMenu(restaurant_id):
    restaurant_url = BASE_URL + RESTAURANT + "/" + str(restaurant_id)
    response = requests.request("GET", restaurant_url, headers=headers)
    return response.text

def getMenuItems(address, radius):
    coords = getCoordinates(address)
    query = urlencode({"lat": coords[0], "lon": coords[1], "distance": radius})
    getmenuitems_url = BASE_URL + MENU_ITEMS + SEARCH_GEO + query
    response = requests.request("GET", getmenuitems_url, headers=headers)
    jsonresponse = json.loads(response.text)
    menuitemdata = jsonresponse["data"]
    return jsonresponse


for restid in searchRestaurants("Raleigh, NC", 1):
    print(restid)
#print(getMenuItems("New York, NY", 1))