import requests
import json
import config
from urllib.parse import urlencode
from app import Allergy, IngredientKeyword, app
from src.shared import db


BASE_URL = "https://api.nal.usda.gov/fdc/v1"
app.app_context().push()

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
    try: 
        foods = jsonresponse["foods"]
        top_match = foods[0]
        return top_match
    except:
        return

"""
RETURNS: ingredients for survey food by fdc_id its lit
"""
def getIngredients(fdc_id):
    url = BASE_URL + "/food/" + str(fdc_id) + "?api_key=" + config.USDA_API_KEY 
    response = requests.get(url)
    if response.status_code == 200:
        jsonresponse = json.loads(response.text)
        ingredients = jsonresponse["inputFoods"] #"inputFoods" throws error for survey foods, which have "ingredients"
        ingredients = [x['ingredientDescription'] for x in ingredients]
        return ingredients
    else:
        print("ERROR " + str(response.status_code) )
        return

def allergyCheck(allergy_keywords, ingredients):
    if not ingredients:
        return set()

    allergies_found = False
    ingredients_str = ' '.join(ingredients).lower()

    for kword in allergy_keywords:
        if kword.keyword.lower() in ingredients_str:
            # allergies_found.add(kword)
            allergies_found = True

    return allergies_found

#pass in ALL the menu items, one by one, into allergyCheck, along with the set of all allergens ... 
#is it necessary to pass in all allergens as a variable? why not keep global? nvm maybe not cause it changes per search

def bigBlackBox(menu, allergies):
    #list of meals from this restaurant, which we then populate with their allergen info
    full = []
    good = []
    allergy_keywords = list()
    for allergy in allergies:
        keywords = list()
        allergy_obj = Allergy.query.filter_by(name=allergy.lower()).first()

        if allergy_obj:
            keywords = IngredientKeyword.query.filter_by(allergy_id=allergy_obj.id)

        #allergy_keywords[allergy] = keywords
        allergy_keywords.extend(keywords)

    for meal in menu:
        #find the ingredients for this meal according to API and return it
        food_match = searchFoods(meal)
        if food_match:
            this_meal_ingredients = getIngredients(food_match["fdcId"])

            #check against our allergens and add the allergens that VIOLATE our HEALTH
            gotallergies = allergyCheck(allergy_keywords, this_meal_ingredients)
            #add to full list (check if works?)
            full.append(meal)

            #add to good list
            if not gotallergies:
                good.append(meal)

    return full, good

# Example
#meal_name = "Pad Thai"
#food_match = searchFoods(meal_name)
#meal_ingredients = getIngredients(food_match["fdcId"])

##USER INPUT HERE
# my_allergies = ["Dairy","Egg","Gluten","Bananas","Mustard"]
# #AND HERE TOO
# the_menu = ["Cheese Puffs", "Strawberry Milkshake", "Banana Pie"]
#lucas is giving these with descriptions
# if there is a description, append that with this meal ingredients
#otherwise ignore, (or still append)
# find them

#turn the_menu into tuples 
#the_menu 

# [ (“Cheese Puffs”, “description”), (“Strawberry milkshake”, “description”) ]


#print( allergyCheck(my_allergies,meal_ingredients) )
# print( bigBlackBox(the_menu, my_allergies))
