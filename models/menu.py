# -*- coding: utf-8 -*-

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
if auth.is_logged_in():
    response.menu = [
        (T('Home'), False, URL('default','index'), []),
        (T('Add'), False, URL('default','add'), []),
        (T('Search'), False, URL('default','search'), []),
        (T('Help'), False, URL('default','help'), [])
        ]
else:
    response.menu = [(T('Home'), False, URL('default','index'), [])]
