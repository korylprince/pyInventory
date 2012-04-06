# -*- coding: utf-8 -*-

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('Add'), False, URL('default','add'), []),
    (T('Search'), False, URL('default','search'), [])
    ]
