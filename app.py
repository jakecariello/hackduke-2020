import os
from flask import flash, Flask, render_template, request, redirect, url_for, session, current_app as app, Response
from flask_sqlalchemy import SQLAlchemy
import config
import src.RestaurantMenuAPI as rma
from sqlalchemy.sql import text
import json
from src.shared import AlchemyEncoder, db, Methods as M
from src.models import Allergy, IngredientKeyword
import usda

# create app
app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

# fetch db connection information
try:

    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_host = os.environ["DB_HOST"]
    db_name = os.environ["DB_NAME"]
    cloud_sql_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}?host=/cloudsql/{cloud_sql_connection_name}'

except Exception as e:

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////tmp/test.db'

    print(str(e))
    print('WARNING: Failed to connect to Google Cloud Database')
    print('Connecting to: {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

# initialize db connection with above information
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/test-db", methods=[M.GET, M.POST])
def test_db():
    print(os.environ, flush=True)
    db.create_all()
    result = db.session.query(Allergy)
    return Response(
        json.dumps([r for r in result], cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )

@app.route("/", methods=[M.GET, M.POST])
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
    for restoid in restoIDs[:10]:
        resto = rma.getRestaurant(restoid)
        toAdd = {"name":resto["restaurant_name"],"id":resto["restaurant_id"], "address":resto["address"]["formatted"], "cuisines":resto["cuisines"]}
        results.append( toAdd )
    if not results:
        #flash('No results found!')
        print('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('restaurant_results.html', results=results)

@app.route('/restaurant/<restaurant_id>', methods=[M.GET])
def restaurant_page(restaurant_id):
    menu_items = []
    #results = getMenu(restaurant_id)
    #menu_items = [("Menu Item 1","Menu Item 1 Description"),("Menu Item 2","Menu Item 2 Description")]
    user_allergies = session['allergies']
    menu_items = rma.getMenuItems(restaurant_id)
    full, good = usda.bigBlackBox(menu_items, user_allergies)
    return render_template("restaurant_menu_page.html",menu_items=good)


HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == "__main__":
     app.run(host=HOST, port=PORT, debug=True)

