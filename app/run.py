# -*- coding: utf-8 -*-
import uuid
import random
import os

from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app

    
class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        users = app.data.driver.db['users']
        return users.find_one({'token': token})
    
def add_token_and_identifier(documents):
    count = app.data.driver.db['users'].count_documents({})
    for document in documents:
        document['token'] = uuid.uuid4().hex + uuid.uuid4().hex
        document['identifier'] = str(1000000000 + (count * 100000) + int(random.random() * 10000))

app = Eve(__name__, settings=os.path.abspath('settings.py'), auth=TokenAuth)

with app.app_context():
    app.on_insert_users += add_token_and_identifier

if os.environ.get('MODE') == 'development' and __name__ == '__main__':
    app.on_insert_users += add_token_and_identifier
    app.run(debug=True)
