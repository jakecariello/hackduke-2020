#aller-g
from ..shared import db

#aller-g
class Allergy(db.Model):
    #__tablename__ = "allergies"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
