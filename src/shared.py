from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

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