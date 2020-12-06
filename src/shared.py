import os
import sys
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, Blueprint

# create global db connection instance
db = SQLAlchemy()

# nifty json encoder for SQLAlchemy objects
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


# HTTP methods
class Methods(str, Enum):
    POST = 'POST'
    GET  = 'GET'

    def __str__(self):
            return self.value

# HTTP response codes
class ResponseCodes(int, Enum):
    SUCCESS = 200
    FAILURE = 400


# HTTP response types
class ResponseTypes(str, Enum):
    HTML = 'text/html'
    JSON = 'application/json'
    
    def __str__(self):
            return self.value


# get data from json OR form
from flask import request
def request_data():
    json_available = request.get_json() is not None and len(list(request.get_json().items())) > 0
    form_available = request.form is not None and len(list(request.form.items())) > 0
    args_available = request.args is not None and len(request.args) > 0

    valid_checks = [item for item in [json_available, form_available, args_available] if item]
    print(f'Found {len(valid_checks)} valid source(s) of data in request.')
    assert len(valid_checks) <= 1, 'Multiple data sources found in request. Ensure that only one of (JSON, form, args) are provided.'

    if json_available:
        return request.get_json()
    elif form_available:
        return request.form
    elif args_available: 
        return request.args
    return dict()

from .db_population.queries import create_allergy, create_ingredient_keyword, get_allergies, get_ingredient_keywords
routes = Blueprint('db_routes', __name__)
routes.route('/create_allergy', methods=[Methods.POST])(create_allergy)
routes.route('/create_ingredient_keyword', methods=[Methods.POST])(create_ingredient_keyword)
routes.route('/get_allergies', methods=[Methods.GET])(get_allergies)
routes.route('/get_ingredient_keywords', methods=[Methods.GET])(get_ingredient_keywords)