from ..shared import db

#table for da ingredients -- what are they??
class IngredientKeyword(db.Model):
    __tablename__ = "ingredient_keyword"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String)
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'), nullable=False)
    
    allergy = db.relationship('Allergy', backref=db.backref('ingredient_keywords', lazy=True))
