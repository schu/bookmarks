# -*- coding: utf-8 -*

from passlib.utils import consteq, to_bytes
from passlib.utils.pbkdf2 import pbkdf2

def hash(password, salt):
    return pbkdf2(to_bytes(password), to_bytes(salt), 10000).encode('hex')

def cmp_hash(a, b):
    return consteq(to_bytes(a), to_bytes(b))
