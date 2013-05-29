# -*- coding: utf-8 -*-

# Code adapted from Shiva
# Copyright © 2013 Alvaro Mouriño
# Author: Alvaro Mouriño <alvaro@mourino.net>
# URL: <https://github.com/tooxie/shiva-server>

from flask.ext.restful import fields, marshal

class ManyToManyField(fields.Raw):
    def __init__(self, foreign_obj, nested, attribute=None):
        self.foreign_obj = foreign_obj
        self.nested = nested

        super(ManyToManyField, self).__init__(attribute=attribute)

    def output(self, key, obj):
        items = list()
        for item in getattr(obj, key):
            items.append(marshal(item, self.nested))

        return items
