# -*- coding: utf-8 -*-

from bookmarks.models import User
from flask.ext.login import AnonymousUser, LoginManager
from .util import cmp_hash, hash


class Auth:
    def __init__(self, app):
        lm = LoginManager()

        lm.login_view = '/login'
        lm.login_message = 'Login required.'
        lm.login_message_category = 'error'
        lm.anonymous_user = AnonymousUser

        lm.setup_app(app)

        @lm.user_loader
        def user_loader(id):
            try:
                id = int(id)
                user = User.query.filter_by(id=id).first()
            except:
                return None
            return user

        app.login_manager = lm
        app.auth_handler = self.auth_handler

    def auth_handler(self, ident, password):
        user = User.query.filter_by(mail=ident).first()
        if not user:
            return None
        if not cmp_hash(user.password,
                hash(password, user.password_salt)):
            return None
        return user
