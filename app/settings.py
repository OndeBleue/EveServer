import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


print dir(os.getenv('MONGO_URI'))

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

users = {
    'resource_methods': ['GET', 'POST'],
    'schema': users_schema,
}

locations = {
    'resource_methods': ['GET', 'POST'],
    'schema': locations_schema,
}

MONGO_URI=os.getenv('MONGO_URI')
DOMAIN = {'users': users, 'locations': locations}