import os
from flask import flash, Flask, render_template, request, redirect, url_for, session, current_app as app, Response
from flask_sqlalchemy import SQLAlchemy
# from config
from sqlalchemy.sql import text

app = Flask(__name__)

try:
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    # db_host = os.environ["INSTANCE_CONNECTION_NAME"]

    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    # items = [db_user, db_pass, db_name, db_socket_dir, cloud_sql_connection_name]
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock={db_socket_dir}>/{cloud_sql_connection_name}/.s.PGSQL.5432'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}?host=/cloudsql/{cloud_sql_connection_name}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@{db_host}/{db_name}'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres+pg8000://{db_user}:{db_pass}@/{db_name}?unix_sock=cloudsql/{cloud_sql_connection_name}/.s.PGSQL.5432'
    print(app.config['SQLALCHEMY_DATABASE_URI'])

except Exception:

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////tmp/test.db'

# This must be set, determine which is best for you
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from sqlalchemy.ext.declarative import DeclarativeMeta
import json
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    try:
                        fields[field] = str(data)
                        try:
                            int(str(data))
                            fields[field] = int(str(data))
                        except Exception:
                            pass
                    except:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


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


@app.route("/test-db", methods=['GET','POST'])
def test_db():
    db.create_all()
    result = db.session.query(Allergy)
    return Response(
        json.dumps([r for r in result], cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )

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
def restaurant_results(address):
    results = []
    #results = getNearbyRestaurants(address)
    results = [
        ("Chipotle",
        1234),
        ("Amy's Kitchen",
        1233)]
    #GO TO LUCAS'S FUNCTIONS
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


HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
