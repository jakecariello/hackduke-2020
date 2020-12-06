from typing import List
import requests
import csv

HOST = 'http://localhost:8080'
ALLERGY_ENDPOINT = '/create_allergy'
INGREDIENT_ENDPOINT = '/create_ingredient_keyword'
CSV_FILE = 'FoodData.csv'

allergies: List[str] = []
ingredient_keywords: List[dict] = []

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

                if allergy not in allergies:
                    allergies.append(allergy)

                ingredient_keywords.append({
                    'allergy': allergy,
                    'keyword': ingredient_keyword
                })

print(allergies)
print(ingredient_keywords)

for allergy in allergies:
    r = requests.post(HOST + ALLERGY_ENDPOINT, data={'name': allergy})