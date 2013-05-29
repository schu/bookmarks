# -*- coding: utf-8 -*-

from bookmarks.models import Tag
from flask.ext.wtf import (BooleanField, Form, Length, PasswordField,
                           Required, Regexp, SelectMultipleField,
                           TextAreaField, TextField, URL)


class BookmarkForm(Form):
    url = TextField("URL", [Required(), URL(require_tld=True)])
    description = TextAreaField('Description')
    tags = SelectMultipleField('Tags')
    public = BooleanField('Public?')

    def __init__(self, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(t.name, t.name) for t in Tag.query.all()]


class LoginForm(Form):
    mail = TextField('E-Mail', [Required()])
    password = PasswordField('Password', [Required()])


class TagForm(Form):
    name = TextField('Name',
            [Required(), Length(min=2, max=32),
                Regexp('^[a-z]+$', message='Tags must be [a-z].')])


class DummyForm(Form):
    pass
