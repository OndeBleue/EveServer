import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

users_schema = {
    'name': {
        'type': 'string',
        'minlength': 3,
        'maxlength': 20,
        'required': True,
    },
    'token': {
        'type': 'string',
        'minlength': 129,
        'maxlength': 129,
    },
    'identifier': {
        'type': 'string',
        'minlength': 5,
        'maxlength': 10,
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
    'resource_methods': ['GET', 'POST'],
    'schema': users_schema,
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
