import os
from os.path import join, dirname
from dotenv import load_dotenv
from eve.auth import BasicAuth

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class IdentifierAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if resource == 'user' and method == 'GET':
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
        'minlength': 64,
        'maxlength': 64,
        'required': True,
        'unique': True,
    },
    'identifier': {
        'type': 'string',
        'minlength': 5,
        'maxlength': 10,
        'required': True,
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
    'item_methods': ['GET'],
    'schema': users_schema,
    'additional_lookup': {
        'url': 'regex("[\d]+")',
        'field': 'identifier',
    },
    'cache_control': '',
    'cache_expires': 0,
    'authentication': IdentifierAuth,
    'auth_field': 'identifier',
}

locations = {
    'resource_methods': ['GET', 'POST'],
    'schema': locations_schema,
}

rendezvous = {
    'resource_methods': ['GET', 'POST'],
    'schema': rendezvous_schema,
}

MONGO_URI = os.environ.get("MONGO_URI")
DOMAIN = {'users': users, 'locations': locations, 'rendezvous': rendezvous}
