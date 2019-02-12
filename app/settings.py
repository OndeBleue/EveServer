import os
import pymongo

from os.path import join, dirname
from dotenv import load_dotenv
from eve.auth import BasicAuth
from flask import current_app as app

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG = os.environ.get('MODE') == 'development'
OPLOG = os.environ.get('MODE') == 'development'

class IdentifierAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if resource == 'users' and method == 'GET':
            users = app.data.driver.db['users']
            user = users.find_one({'identifier': username})
            if user and 'identifier' in user:
                self.set_request_auth_value(user['identifier'])
            return user
        else:
            return True


users_schema = {
    'name': {
        'type': 'string',
        'minlength': 3,
        'maxlength': 20,
        'required': True,
    },
    'token': {
        'type': 'string',
        'unique': True,
    },
    'identifier': {
        'type': 'string',
        'unique': True,
    },
}

locations_schema = {
    'user': {
        'type': 'objectid',
        'required': True,
    },
    'coordinates': {
        'type': 'point',
        'required': True,
    },
    'datetime': {
        'type': 'datetime',
        'required': True,
    },
}
    

rendezvous_schema = {
    'user': {
        'type': 'objectid',
        'required': True,
    },
    'coordinates': {
        'type': 'point',
        'required': True,
    },
    'datetime': {
        'type': 'datetime',
        'required': True,
    },
    'address': {
        'type': 'string',
    },
}

users = {
    'resource_methods': ['POST'],
    'public_methods': ['POST'],
    'item_methods': ['GET', 'PATCH'],
    'schema': users_schema,
    'additional_lookup': {
        'url': 'regex("[\d]+")',
        'field': 'identifier',
    },
    'cache_control': 'no-cache',
    'cache_expires': 0,
    'authentication': IdentifierAuth,
    'auth_field': 'identifier',
    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token', 'identifier'],
}

locations = {
    'resource_methods': ['POST'],
    'schema': locations_schema,
    'mongo_indexes': { 
        'coordinates_2dsphere': ([('coordinates', pymongo.GEOSPHERE)], {"sparse": True})
    }
}

aroundme = {
    'resource_methods': ['GET'],
    'datasource': {
        'source': 'locations',
        'aggregation': {
            'pipeline': [
                {"$geoNear": {
                    "spherical": True,
                    "maxDistance": "$distance",
                    "near": {
                        "type": "Point",
                        "coordinates": "$center"
                    },
                    "distanceField": "distance"
                }},
                {"$sort": {"user": 1, "datetime": 1}},
                {"$group": {
                    "_id": "$user",
                    "lastUpdate": {"$last": "$datetime"},
                    "lastPosition": {"$last": "$coordinates"},
                    "locationId": {"$last": "$_id"},
                    "userId": {"$last": "$user"}
                }},
                {"$lookup": {
                    "from": "users",
                    "localField": "userId",
                    "foreignField": "_id",
                    "as": "user"
                }},
                {"$project": {
                    "_id": "$locationId",
                    "user": "$userId",
                    "coordinates": "$lastPosition",
                    "datetime": "$lastUpdate",
                    "userName": "$user.name"
                }}
            ]
        }
    }
}

rendezvous = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'schema': rendezvous_schema,
    'mongo_indexes': { 
        'coordinates_2dsphere': ([('coordinates', pymongo.GEOSPHERE)], {"sparse": True})
    }
}

X_HEADERS = ['Authorization', 'Content-type', 'If-Match']
X_EXPOSE_HEADERS = ['Access-Control-*']
X_DOMAINS = os.environ.get("X_DOMAINS")
MONGO_URI = os.environ.get("MONGO_URI")
DOMAIN = {'users': users, 'locations': locations, 'around-me': aroundme, 'rendez-vous': rendezvous}
