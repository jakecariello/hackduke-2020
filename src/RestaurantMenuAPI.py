import requests
from urllib.parse import urlencode
import urllib.parse
import config
import json


BASE_URL = "https://us-restaurant-menus.p.rapidapi.com"
RESTAURANTS = "/restaurants"
RESTAURANT = "/restaurant"
MENU_ITEMS = "/menuitems"
SEARCH_GEO = "/search/geo"
API_KEY = config.US_MENU_API_KEY
RAPIDAPI_KEY = config.RAPIDAPI_KEY
RAPIDAPI_HOST = config.RAPIDAPI_HOST

headers = {
    'x-api-key': API_KEY,
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': RAPIDAPI_HOST
    }


def getRequestPage(url, querystring, page):
    querystring["page"] = page
    response = requests.request("GET", url, headers=headers, params=querystring)
    return json.loads(response.text)["result"]



def getRestaurantIDsInRadius(address, radius):
    coords = getCoordinates(address)
    querystring = {"lat": coords[0], "lon": coords[1], "distance": radius}
    search_restaurant_url = BASE_URL + RESTAURANTS + SEARCH_GEO
    response = requests.request("GET", search_restaurant_url, headers=headers, params=querystring)
    jsonresponse = json.loads(response.text)["result"]
    rest_ids = list()
    while True:
        for restaurant in jsonresponse["data"]:
            rest_ids.append(restaurant['restaurant_id'])
        if jsonresponse["morePages"] is True:
            nextpage = int(jsonresponse["page"]) + 1
            jsonresponse = getRequestPage(search_restaurant_url, querystring, nextpage)
        else:
            break
    return rest_ids

def getRestaurant(id):
    rest_url = BASE_URL + RESTAURANT + "/" + str(id)
    response = requests.request("GET", rest_url, headers=headers)
    return json.loads(response.text)['result']

def getMenuItems(id):
    menu_url = BASE_URL + RESTAURANT + "/" + str(id) + MENU_ITEMS
    response = requests.request("GET", menu_url, headers=headers)
    jsonresponse = json.loads(response.text)['result']
    menuitems = list()
    while True:
        for menuitem in jsonresponse["data"]:
            menuitems.append((menuitem['menu_item_name'], menuitem['menu_item_description']))
        if jsonresponse["morePages"] is True:
            nextpage = int(jsonresponse["page"]) + 1
            jsonresponse = getRequestPage(menu_url, {}, nextpage)
        else:
            break
    return menuitems




"""
RETURNS: latitude and longitude of an address
"""
def getCoordinates(address):
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return response[0]["lat"], response[0]["lon"]


