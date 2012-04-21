# coding: utf8
# database stuff
from gluon.tools import Crud
crud = Crud(db)

@auth.requires_login()
def index():
    response.subtitle = 'What next?'
    forms = []
    for search in searches:
        forms.append(FORM(search.replace('_',' ') + ': ', INPUT(_name='search'), INPUT(_type='submit', _value='Submit'), _action=URL('edit',vars=dict(type=search))))
    totalrecs = db.executesql('select count(*) from devices')[0][0] 
    return dict(forms=forms,totalrecs=totalrecs)

@auth.requires_login()
def search():
    response.subtitle = 'This ain\'t Yo Momma\'s Search.'
    if request.vars['type'] == 'all':
        return dict(records=db(db.devices).select())
    for col in db.devices.fields:
        request.vars['chk'+col] = 'on'
    form, records = crud.search(db.devices)
    #Check if no devices found
    if len(records) == 0 and records != []:
        response.flash = 'No Matching Devices Found'
    return dict(form=form, records=records)

@auth.requires_login()
def edit():
    response.subtitle = 'Be careful now, Ya Hear?'
    # Make sure search isn't empty
    if request.vars['search'] == '':
        session.flash=T("Device Not Found!")
        redirect(URL('index'))
    # Make sure the variables get passed so delete works properly
    if 'search' not in request.get_vars.keys() :
        # puts POST vars in GET
        redirect(URL('edit',vars=request.vars))
    # see if any records contain the search text
    found = db(db.devices[request.vars['type']].like('%'+request.vars['search']+'%')).select()
    # Multiple records returned so show search page
    if len(found)>1:
        response.view = 'default/search.html'
        return dict(records=found)
    # Just one found so show edit page
    elif len(found) == 1:
        foundID = found[0]['id']
    # None found - stay at index
    else:
        session.flash=T("Device Not Found!")
        redirect(URL('index'))
    return dict(form=crud.update(db.devices,foundID))

@auth.requires_login()
def add():
    response.subtitle = 'Are you sure about this?'
    return dict(form=crud.create(db.devices))


def user():
    response.subtitle = 'What\'s the Secret Password?'
    return dict(form=auth())
