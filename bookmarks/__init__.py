# -*- coding: utf-8 -*-

import config
import re
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from jinja2 import evalcontextfilter, Markup, escape

app = Flask(__name__)
app.config.from_object(config)

# http://flask.pocoo.org/snippets/28
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(p.replace('\n', '<br>\n') \
            for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

db = SQLAlchemy(app)

from auth import Auth
Auth(app)

import api
import views
