# -*- coding: utf-8 -*-

import datetime
import random
import string
from bookmarks import db
from sqlalchemy.ext.hybrid import hybrid_property
from .util import hash


bookmarks_tags_rel = db.Table('bookmarks_tags_rel',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmarks.id'))
)


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), unique=True)
    title = db.Column(db.String(1024))
    description = db.Column(db.Text)
    public = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime)
    t = db.relationship('Tag', secondary=bookmarks_tags_rel,
            backref=db.backref('bookmarks', lazy='select'))

    def __init__(self, url, title, description='', tags=[], public=False):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags
        self.public = public
        self.timestamp = datetime.datetime.utcnow()

    @hybrid_property
    def tags(self):
        return self.t

    @tags.setter
    def tags(self, tagz=[]):
        tags = []
        for tag in tagz:
            tags.append(Tag.query.filter_by(name=tag).first())
        self.t = tags


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    mail = db.Column(db.String(256))
    password_salt = db.Column(db.String(32))
    password_hash = db.Column(db.String(256))

    def __init__(self, mail, password, is_admin=False):
        self.is_admin = is_admin
        self.mail = mail
        self.password_salt = ''.join(random.choice(
                    string.letters + string.digits) for i in range(16))
        self.password = password

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = hash(password, self.password_salt)

    def set_last_login(self):
        self.last_login = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def get_id(self):
        return self.id

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
