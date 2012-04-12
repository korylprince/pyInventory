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
    return dict(url=URL('search'),addurl=URL('add'),forms=forms,totalrecs=totalrecs)

@auth.requires_login()
def search():
    response.subtitle = 'This ain\'t Yo Momma\'s Search.'
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
    #Make sure the variables get passed so delete works properly
    if 'search' not in request.get_vars.keys() :
        # puts POST vars in GET
        redirect(URL('edit',vars=request.vars))
    try:
        foundID = db(db.devices[request.vars['type']]==request.vars['search']).select()[0]['id']
    except IndexError:
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
