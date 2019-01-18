# -*- coding: utf-8 -*-

from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app
import uuid

    
class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        users = app.data.driver.db['users']
        return users.find_one({'token': token})
    
def add_token(documents):
    for document in documents:
        document["token"] = uuid.uuid4().hex + uuid.uuid4().hex

if __name__ == '__main__':
    app = Eve(auth=TokenAuth)
    app.on_insert_users += add_token
    app.run()

