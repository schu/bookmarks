# -*- coding: utf-8 -*-

from bookmarks import app
from bookmarks.models import Bookmark, Tag, User
from .fields import ManyToManyField
from flask import request, Response
from flask.ext import restful
from flask.ext.restful import abort, Api, fields, marshal
from functools import wraps


def authenticate(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not app.auth_handler(auth.username, auth.password):
            return abort(401, message='Access denied')
        return f(*args, **kwargs)
    return decorated


class Resource(restful.Resource):
    method_decorators = [authenticate]


class BookmarkResource(Resource):

    _fields = {
        'id': fields.Integer,
        'url': fields.String,
        'description': fields.String,
        'public': fields.Boolean,
        'tags': ManyToManyField(Tag, {
            'id': fields.Integer,
            'name': fields.String
        }, attribute='t')
    }

    def get(self, id=None):
        if not id:
            return list(self.get_all())
        bookmark = Bookmark.query.filter_by(id=id).first()
        if not bookmark:
            abort(404)
        return marshal(bookmark, self._fields)

    def get_all(self):
        for bookmark in Bookmark.query.all():
            yield marshal(bookmark, self._fields)


class TagResource(Resource):

    _fields = {
        'id': fields.Integer,
        'name': fields.String,
        'bookmarks': ManyToManyField(Bookmark, {
            'id': fields.Integer,
            'url': fields.String
        })
    }

    def get(self, id=None):
        if not id:
            return list(self.get_all())
        tag = Tag.query.filter_by(id=id).first()
        if not tag:
            abort(404)
        return marshal(tag, self._fields)

    def get_all(self):
        for tag in Tag.query.all():
            yield marshal(tag, self._fields)


api = Api(app, prefix='/api')

api.add_resource(BookmarkResource,
                 '/bookmarks',
                 '/bookmark/<int:id>')

api.add_resource(TagResource,
                 '/tags',
                 '/tag/<int:id>')
