#from ..shared import db
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, ForeignKeyConstraint
from sqlalchemy import *

#chat
#### Rohin:
### 

#### Luiza:
###

class IngredientKeyword(db.model):
    __tablename__ = "ingredient_keywords"
    id = Column(Integer,primary_key=True) #might need
    name = Column(String)
    allergy_id = Column(Integer)
    