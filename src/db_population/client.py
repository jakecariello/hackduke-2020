import json
from typing import List
import requests
import csv

HOST = 'http://localhost:8080'
CREATE_ALLERGY_ENDPOINT = '/create_allergy'
GET_ALLERGIES_ENDPOINT = '/get_allergies'
CREATE_INGREDIENT_ENDPOINT = '/create_ingredient_keyword'
RESET_ENDPOINT = '/reset-db'
CSV_FILE = 'FoodData.csv'

allergies: List[str] = []
ingredient_keywords: dict = {}

# extract data from CSV
with open(CSV_FILE, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    first_line = True
    for row in csv_reader:
        if first_line:
            print(f'Column names are {", ".join(row)}')
            first_line = False

        else:
            allergy = row['Allergy']
            ingredient_keyword = row['Food']

            if 'allergy' in allergy.lower() and 'syndrome' not in allergy.lower():

                for substring in ['allergy ', 'Allergy ', 'allergy', 'Allergy']:
                    allergy = allergy.replace(substring,'')
                allergy = allergy.strip()

                if allergy not in allergies:
                    allergies.append(allergy)

                if not allergy in ingredient_keywords.keys():
                    ingredient_keywords[allergy] = []

                ingredient_keywords[allergy].append(ingredient_keyword)

# reset DB
requests.get(HOST + RESET_ENDPOINT)

# populate allergies
for allergy in allergies:
    r = requests.post(HOST + CREATE_ALLERGY_ENDPOINT, data={'name': allergy})
    print(f'Successfully added allergy: {r.content}')

# get list of allergies with id's
r = requests.get(HOST + GET_ALLERGIES_ENDPOINT)
allergies = r.json()
print(json.dumps(allergies, indent=4))

# populate ingredients
for allergy_name, associated_keywords in ingredient_keywords.items():
    allergy_id = None
    for allergy in allergies:
        if allergy['name'] == allergy_name:
            allergy_id = allergy['id']
            break
    assert allergy_id is not None

    for keyword in associated_keywords:
        r = requests.post(HOST + CREATE_INGREDIENT_ENDPOINT, data={
            'allergy_id': allergy_id,
            'keyword': keyword
        })
        print(f'Successfully added keyword: {r.content}')