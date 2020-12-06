import os
from flask import flash, Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import config
import src.RestaurantMenuAPI as rma

#open sesame
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.secret_key = config.SECRET_KEY
db = SQLAlchemy(app)

#aller-g
class Allergy(db.Model):
    #__tablename__ = "allergies"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)

#table for da ingredients -- what are they??
class IngredientKeyword(db.Model):
    #__tablename__ = "ingredient_keywords"
    ingredient_id = db.Column(db.Integer,primary_key=True) #might need
    keyword = db.Column(db.String)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'),
        nullable=False)
    allergy = db.relationship('Allergy',
        backref=db.backref('ingredient_keywords', lazy=True))

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

@app.route("/", methods=['GET','POST'])
def main_view():
    print(os.getcwd())
    all_allergens = ["Egg","Gluten","Peanuts","Shellfish","Dairy","Mustard"]
    if request.method == 'GET':
        return render_template("search_page_v0.html",allergens=all_allergens)
    address = request.form['address'] #don't have this form set up rn
    allergies = request.form.getlist('selected_allergies')
    session['allergies'] = allergies
    return restaurant_results(address)

@app.route("/restaurant_results")
def restaurant_results(address,radius=3):
    results = []
    restoIDs = rma.getRestaurantIDsInRadius(address, radius)
    for restoid in restoIDs:
        resto = rma.getRestaurant(restoid)
        toAdd = {"name":resto["restaurant_name"],"id":resto["restaurant_id"], "address":resto["address"]["formatted"], "cuisines":resto["cuisines"]}
        results.add( toAdd )
    if not results:
        #flash('No results found!')
        print('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('restaurant_results.html', results=results)

@app.route('/restaurant/<restaurant_id>', methods=['GET'])
def restaurant_page(restaurant_id):
    menu_items = []
    #results = getMenu(restaurant_id)
    menu_items = [("Menu Item 1","Menu Item 1 Description"),("Menu Item 2","Menu Item 2 Description")]
    user_allergies = session['allergies']
    #menu_with_allergens = filterMenu(menu_items,user_allergies)
    return render_template("restaurant_menu_page.html",menu_items=menu_items)


if __name__ == "__main__":
     app.run(host=HOST, port=PORT, debug=True)

