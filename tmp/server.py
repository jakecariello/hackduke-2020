from flask import *
import os
import sys
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from api.shared import ResponseCodes, ResponseTypes, db, request_data, verify_user
from api.queries.review import create_review
from api.queries.user import create_user
from api.queries.photo import create_photo
from api.queries.ingredient_in_recipe import get_ingredient_in_recipe_info
import random
from api.models import Recipe, User, Review, Photo, IngredientInRecipe, Ingredient
from datetime import datetime
from werkzeug.utils import secure_filename


from api.shared import AlchemyEncoder

# models!
from api.routes import routes as api_routes

# templatestuff
from flask import render_template

os.environ['UPLOAD_FOLDER'] = '/app/static/img/photos/'

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
print(app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)
print(db)
app.config['SECRET_KEY'] = b'L\x8e\x8a\xef\x15\xc6ZN\x97>\n\xeed\xcd:\x01'

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_FOLDER'] = '/app/static/img/photos/'

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now handling non-HTTP exceptions, so attempt to create db
    db.create_all()

@app.route('/initdb')
def init_db():
    db.create_all()
    return 'Done', 200


@app.route("/")
def hello_world():
    if not 'user' in session:
        return redirect(url_for('login'))
    return render_template("main-page.html",user=json.loads(session.get('user')))


@app.route("/recipe/<cid>", methods = ["GET","POST"])
def recipe_page(cid):
    try:
        uid  = json.loads(session.get('user')).get('uid')
        cidnew = cid
        recipe = Recipe.query.filter(Recipe.cid == cidnew).one()
        pid = recipe.pid
        if pid is None:
            pid = -1
        #selected_ingredients = get_ingredient_in_recipe_info(cidnew)
        # ing = Ingredient.query.join(selected_ingredients, Ingredient.iid == selected_ingredients.iid).one()
        # i = Ingredient.query.first()
        # ing = Ingredient.query.join(IngredientInRecipe, Ingredient.iid == IngredientInRecipe.iid).filter(IngredientInRecipe.cid == cidnew).first()
        # ing = IngredientInRecipe.query.join(Ingredient, Ingredient.iid == IngredientInRecipe.iid).filter(IngredientInRecipe.cid == cidnew).first()
        # a = session.query(IngredientInRecipe).filter(IngredientInRecipe.cid == cidnew).all()
        if request.form:
            create_review(cidnew)
        return render_template("recipe.html", 
            recipe = Recipe.query.filter(Recipe.cid == cidnew).one(),
            reviews = Review.query.filter(Review.cid == cidnew).all(),
            cidroute = "/recipe/" + str(cidnew), 
            cookroute = "/api/recipe_action/cook?cid=" + str(cidnew), 
            favoriteroute = "/api/recipe_action/favorite?cid=" + str(cidnew),
            pidroute = "../static/img/photos/" + str(pid) + ".png"
        ) 
    except Exception as ex:
        print(ex)
        return Response(
            json.dumps({'error': str(ex)}),
            status=ResponseCodes.FAILURE,
            mimetype=str(ResponseTypes.JSON)
        )


@app.route("/review", methods = ["GET","POST"])
def review_page():
    if request.form:
        create_review()
    return render_template(
        "review.html",
        reviews = Review.query.all(),
        title="Show Reviews"
    )

@app.route("/uppic", methods = ["GET","POST"])
def upload_pic():
    #if request.files:
        #new_photo = Photo()
        #db.session.add(new_photo)
        #db.session.commit()

    #uploaded_file = request.files['file']
    #if uploaded_file.filename != '':
    #    uploaded_file.save(uploaded_file.filename)

    if request.files:
        create_photo()
        new_photo = Photo()
        db.session.add(new_photo)
        db.session.commit()

        file = request.files['file']
        filename = secure_filename(file.filename)
        file.filename = str(new_photo.pid) + '.png'
        path = os.path.join(os.environ['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        return path


        

    return render_template(
        "upload-pic.html"
    )



@app.route("/recipe-book")
def user_history_page():
	return render_template("user-history.html", user=json.loads(session.get('user')))

@app.route("/thankyou", methods = ["GET","POST"])
def thankyou():
    return "Thank you for submitting a review!"

@app.route("/search-results", methods = ["GET"])
def results_page():
	# data = JSON.parsestr(data)
	return render_template(
		"results-page.html",
		results = request_data()
		)


@app.route('/sign-up',methods = ["GET","POST"])
def sign_up():

   if request.method == "POST":
       
        req = request.form

        username = req.get("username")
        firstname = req.get("firstname")
        lastname = req.get("lastname")
        password = req.get("password")

        if username == '':
            flash("Input a valid username")
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("username already taken!")
        elif firstname == '':
            flash("Input a valid first name")
        elif lastname == '':
            flash("Input a valid lastname")
        elif password == '':
            flash("Input a valid password")
        else:
            pid = 0
            if request.files:
                new_photo = Photo()
                db.session.add(new_photo)
                db.session.commit()

                pid = new_photo.pid
                print(pid)
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.filename = str(new_photo.pid) + '.png'
                path = os.path.join(os.environ['UPLOAD_FOLDER'], file.filename)
                file.save(path)
            
            current_user = create_user(pid)
            session['user'] = json.dumps(current_user, cls=AlchemyEncoder)
            return redirect(url_for('hello_world'))

        return render_template("/signup.html")
   return render_template("/signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    db.create_all()

    if request.method=="POST":

        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()
        
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user'] = json.dumps(user, cls=AlchemyEncoder)

            return redirect(url_for("hello_world"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout", methods=["POST","GET"])
def logout():
    if request.method == "POST":
        username = json.loads(session.get('user')).get('username')
        session.pop('user', None)
        flash(username + " successfully logged out.")
        return redirect(url_for('login'))


@app.route("/results-page" , methods = ["GET" , "POST"])
def return_results(results): 
    return render_template("results-page.html" , results = results)


@app.route('/create-recipe')
def create_recipe_page():
    return(render_template('create-recipe.html'))


@app.route('/create-ingredient')
def create_ingredient_page():
    return(render_template('create-ingredient.html'))

   
app.register_blueprint(api_routes)


app.run(host=HOST, port=PORT, debug=True)
print(f'RECIPESPACE is now listening on {HOST}:{PORT}')
