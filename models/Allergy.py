#from ..shared import db
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, ForeignKeyConstraint
from sqlalchemy import *
from app import db

class Allergy(db.Model):
    __tablename__ = "allergies"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    