import os

from os.path import join, dirname
from dotenv import load_dotenv
from eve.auth import BasicAuth
from flask import current_app as app

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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
        'source': 'users',
    },
    'coordinates': {
        'type': 'point',
    },
    'datetime': {
        'type': 'datetime',
    },
}
    

rendezvous_schema = {
    'user': {
        'source': 'users',
    },
    'coordinates': {
        'type': 'point',
    },
    'datetime': {
        'type': 'datetime',
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
    'cache_control': '',
    'cache_expires': 0,
    'authentication': IdentifierAuth,
    'auth_field': 'identifier',
    # Allow 'token' to be returned with POST responses
    'extra_response_fields': ['token', 'identifier'],
}

locations = {
    'resource_methods': ['GET', 'POST'],
    'schema': locations_schema,
}

rendezvous = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH'],
    'schema': rendezvous_schema,
}

X_HEADERS = ['Authorization', 'Content-type', 'If-Match']
X_EXPOSE_HEADERS = ['Access-Control-*']
X_DOMAINS = os.environ.get("X_DOMAINS")
MONGO_URI = os.environ.get("MONGO_URI")
DOMAIN = {'users': users, 'locations': locations, 'rendezvous': rendezvous}
