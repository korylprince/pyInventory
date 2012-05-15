# coding: utf8
# database stuff
from gluon.tools import Crud
crud = Crud(db)

@auth.requires_login()
def index():
    response.subtitle = 'Time to pay...'
    response.view = 'default/index.html'
    forms = []
    for search in chargeSearches:
        forms.append(FORM(SPAN(search.replace('_',' ') + ': '), INPUT(_name='search'), INPUT(_type='submit', _value='Submit'), _action=URL('edit',vars=dict(type=search))))
    totalrecs = db.executesql('select count(*) from charges')[0][0] 
    return dict(forms=forms,totalrecs=totalrecs)

@auth.requires_login()
def search():
    response.subtitle = 'Show me the money.'
    response.view = 'default/search.html'
    if request.vars['type'] == 'all':
        records=db(db.charges).select()
        if len(records)<1:
            session.flash = 'No Matching Devices Found'
            redirect('index')
        return dict(records=db(db.charges).select())
    for col in db.charges.fields:
        request.vars['chk'+col] = 'on'
    form, records = crud.search(db.charges)
    #Check if no devices found
    if len(records) == 0 and records != []:
        response.flash = 'No Matching Devices Found'
    return dict(form=form, records=records)

@auth.requires_login()
def edit():
    response.subtitle = '1 + 1 = 2, Right?'
    # Make sure search isn't empty
    if request.vars['search'] == '':
        session.flash=T("Device Not Found!")
        redirect(URL('index'))
    # Make sure the variables get passed so delete works properly
    if 'search' not in request.get_vars.keys() :
        # puts POST vars in GET
        redirect(URL('edit',vars=request.vars))
    # see if any records contain the search text
    found = db(db.charges[request.vars['type']].like('%'+request.vars['search']+'%')).select()
    # Multiple records returned so show search page
    if len(found)>1:
        response.view = 'default/search.html'
        return dict(records=found)
    # Just one found so show edit page
    elif len(found) == 1:
        response.view = 'default/edit.html'
        foundID = found[0]['id']
    # None found - stay at index
    else:
        session.flash=T("Device Not Found!")
        redirect(URL('index'))
    links = [A('Generate Report', _href=URL('report',vars=dict(id=foundID))),A('Inventory Reference', _href=URL('default','edit',vars=dict(type='Inventory_Number',search=found[0].Inventory_Number)))]
    return dict(form=crud.update(db.charges,foundID, next=URL('report',vars=dict(id=foundID))),links=links)
@auth.requires_login()
def add():
    response.subtitle = 'Another customer, huh?'
    response.view = 'default/edit.html'
    form=crud.create(db.charges)
    if 'Charges' in form.errors:
        response.flash = 'Problem with Charges syntax'
    if form.vars.id != None:
        redirect(URL('report',vars=dict(id=form.vars.id)))
    return dict(form=form)

@auth.requires_login()
def report():
    response.view = 'charges/report.html'
    if 'id' not in request.vars:
        session.flash = 'Record not Found'
        redirect(URL('index'))
    record = db(db.charges.id == request.vars['id']).select()
    if len(record) != 1:
        session.flash = 'Record not Found'
        redirect(URL('index'))
    return dict(record = record[0])

@auth.requires_login()
def help():
    response.subtitle = 'This here\'s the help.'
    response.view = 'default/help.html'
    return dict()
