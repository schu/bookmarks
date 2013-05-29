#!/usr/bin/env python2
import path
import bookmarks
import sys

if len(sys.argv) < 3:
    sys.exit('usage: %s <email> <passphrase> [<is_admin>]' % sys.argv[0])

if len(sys.argv) > 3:
    is_admin = True
else:
    is_admin = False

user = bookmarks.models.User(sys.argv[1], sys.argv[2], is_admin)

bookmarks.db.session.add(user)
bookmarks.db.session.commit()
