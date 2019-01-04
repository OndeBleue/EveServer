# -*- coding: utf-8 -*-

from eve import Eve
from eve.auth import TokenAuth
from flask import current_app as app

class TokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        users = app.data.driver.db['users']
        return users.find_one({'token': token})

if __name__ == '__main__':
    app = Eve(auth=TokenAuth)
    app.run()

