from flask import session

# db instance
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def build_route(parts):
    return '/'.join([p for p in parts])

# route for using the api
from enum import Enum
class ApiRoutes(str, Enum):

    BASE = '/api'

    # recipe
    RECIPE_BASE = '/recipe'
    RECIPE_FILTER = build_route([
        BASE, RECIPE_BASE, '/filter'
    ])
    RECIPE_CREATE = build_route([
        BASE, RECIPE_BASE, '/create'
    ])

    # ingredient
    INGREDIENT_BASE = '/ingredient'
    INGREDIENT_FILTER = build_route([
        BASE, INGREDIENT_BASE, '/filter'
    ])
    INGREDIENT_CREATE = build_route([
        BASE, INGREDIENT_BASE, '/create'
    ])

    # photo
    PHOTO_BASE = '/photo'
    PHOTO_CREATE_PHOTO = build_route([
        BASE, PHOTO_BASE, '/create'
    ])

    # ingredient in recipe
    INGREDIENT_IN_RECIPE_BASE = '/ingredient_in_recipe'
    INGREDIENT_IN_RECIPE_FILTER = build_route([
        BASE, INGREDIENT_IN_RECIPE_BASE, '/filter'
    ])
    INGREDIENT_IN_RECIPE_CREATE = build_route([
        BASE, INGREDIENT_IN_RECIPE_BASE, '/create'
    ])
    INGREDIENT_IN_RECIPE_DELETE = build_route([
        BASE, INGREDIENT_IN_RECIPE_BASE, '/delete'
    ])
    
    # tag
    TAG_BASE = '/tag'
    TAG_LIST_ALL = build_route([
        BASE, TAG_BASE, '/list-all'
    ])

    # review
    REVIEW_BASE = '/review'
    REVIEW_CREATE_REVIEW = build_route([
        BASE, REVIEW_BASE, '/create_review'
    ])
    REVIEW_DELETE_REVIEW = build_route([
        BASE, REVIEW_BASE, '/delete_review'
    ])
    REVIEW_GET_BY_ID = build_route([
        BASE, REVIEW_BASE, '/get_review_by_id'
    ])
    REVIEW_GET_BY_RECIPE_ID = build_route([
        BASE, REVIEW_BASE, '/get_review_by_recipe_id'
    ])

    # recipe_action
    RECIPE_ACTION_BASE = '/recipe_action'
    RECIPE_ACTION_CREATE = build_route([
        BASE, RECIPE_ACTION_BASE, '/create'
    ])
    RECIPE_ACTION_LIKE = build_route([
        BASE, RECIPE_ACTION_BASE, '/like'
    ])
    RECIPE_ACTION_FAVORITE = build_route([
        BASE, RECIPE_ACTION_BASE, '/favorite'
    ])
    RECIPE_ACTION_DELETE = build_route([
        BASE, RECIPE_ACTION_BASE, '/delete'
    ])
    RECIPE_ACTION_UNLIKE = build_route([
        BASE, RECIPE_ACTION_BASE, '/unlike'
    ])
    RECIPE_ACTION_COOK= build_route([
        BASE, RECIPE_ACTION_BASE, '/cook'
    ])
    
    GET_RECIPE_ACTIONS = build_route([
        BASE, RECIPE_ACTION_BASE, '/get_action_create'
    ])
    RECIPE_ACTION_GET_COOK = build_route([
        BASE, RECIPE_ACTION_BASE, '/get_cook'
    ])

    RECIPE_ACTION_GET_CREATE = build_route([
        BASE, RECIPE_ACTION_BASE, '/get_create'
    ])

    RECIPE_ACTION_GET_FAVORITE = build_route([
        BASE, RECIPE_ACTION_BASE, '/get_favorite'
    ])

    

    # user
    USER_BASE = '/user'
    USER_CREATE_USER = build_route([
        BASE, USER_BASE, '/create_user'
    ])
   
   

    def __str__(self):
            return self.value


class Methods(str, Enum):
    POST = 'POST'
    GET  = 'GET'

    def __str__(self):
            return self.value


class ResponseCodes(int, Enum):
    SUCCESS = 200
    FAILURE = 400


class ResponseTypes(str, Enum):
    HTML = 'text/html'
    JSON = 'application/json'
    
    def __str__(self):
            return self.value


# json encoder
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

def verify_user():
    data = request_data()
    session_user = json.loads(session.get('user', None))
    assert session_user is not None, 'There must be a user logged in to perform this action.'
    session_uid = session_user['uid']

    request_uid = data.get('uid')
    if request_uid is not None:
        assert session_uid == request_uid, 'Logged in and requested users must match.'
    return session_uid
