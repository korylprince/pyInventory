# -*- coding: utf-8 -*-

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################
if auth.is_logged_in():
    if request.controller == 'default':
        response.menu = [
            (SPAN('Inventory', _style='color:#fff;font-size:13pt;'), False, URL('default','index'), []),
            ('Add', False, URL('default','add'), []),
            ('Search', False, URL('default','search'), []),
            ('Charges', False, URL('charges','index'), []),
            ('Help', False, URL('default','help'), [])
            ]
    else:
        response.menu = [
            (SPAN('Charges', _style='color:#fff;font-size:13pt;'), False, URL('charges','index'), []),
            ('Add', False, URL('charges','add'), []),
            ('Search', False, URL('charges','search'), []),
            ('Inventory', False, URL('default','index'), []),
            ('Help', False, URL('charges','help'), [])
            ]
else:
    response.menu = []
