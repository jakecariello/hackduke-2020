import requests
import json
import config
from urllib.parse import urlencode
from app import Allergy, IngredientKeyword, db

BASE_URL = "https://api.nal.usda.gov/fdc/v1"

"""
Searches FoodData Central for foods that match keyword description 
RETURNS: top match for keyword search, filtered by "survey" datatype (as opposed to "branded")
"""
def searchFoods(keywords):
    #filters by survey, vs branded foods
    query = urlencode({"query":keywords, "dataType":"Survey (FNDDS)"})
    getfoods_url = BASE_URL + "/foods/search?" + "api_key=" + config.USDA_API_KEY + "&" + query
    response = requests.get(getfoods_url)
    jsonresponse = json.loads(response.text)
    foods = jsonresponse["foods"]
    top_match = foods[0]
    return top_match

"""
RETURNS: ingredients for survey food by fdc_id its lit
"""
def getIngredients(fdc_id):
    url = BASE_URL + "/food/" + str(fdc_id) + "?api_key=" + config.USDA_API_KEY 
    response = requests.get(url)
    jsonresponse = json.loads(response.text)
    print(response.status_code)
    ingredients = jsonresponse["inputFoods"] #"inputFoods" throws error for survey foods, which have "ingredients"
    ingredients = [x['ingredientDescription'] for x in ingredients]
    return ingredients

def allergyCheck(allergies, ingredients):
    allergies_found = set()
    ingredients_str = ' '.join(ingredients).lower()
    for allergy in allergies:

        if allergy.lower() in ingredients_str:
            allergies_found.add(allergy)

        keywords = []
        allergy_obj = Allergy.query.filter_by(name=allergy.lower()).first()
        if allergy_obj:
            keywords = IngredientKeyword.query.filter_by(allergy_id=allergy_obj.id)

        for keyword in keywords:
            ingredient = keyword.keyword
            if ingredient.lower() in ingredients_str:
                allergies_found.add(allergy)

    return allergies_found

# Example
meal_name = "Pad Thai"
food_match = searchFoods(meal_name)
meal_ingredients = getIngredients(food_match["fdcId"])
my_allergies = ["Dairy","Egg","Gluten","Bananas","Mustard"]
print( allergyCheck(my_allergies,meal_ingredients) )

