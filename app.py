import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#open sesame
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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

@app.route("/", methods=['GET'])
def main_view():
    print(os.getcwd())
    return render_template("main_page.html")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
