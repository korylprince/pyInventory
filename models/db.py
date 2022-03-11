# -*- coding: utf-8 -*-
import os
from gluon.tools import Auth, Crud
from gluon.contrib.login_methods.ldap_auth import ldap_auth

# set Title for all pages
response.title = "Bullard ISD Inventory"

# set header for charges report
reportheader = "BISD Technology Equipment Check-in Form"

# set Quick Search fields
searches = ["Inventory_Number", "Serial_Number", "Bag_Tag", "User"]
chargeSearches = ["Inventory_Number", "User"]

# set enumeration fields
userTypes = ("Student", "Teacher", "Administrator", "Other")
deviceTypes = ("Laptop", "Desktop", "Projector", "Printer", "Document Camera", "Scanner", "Interactive Board", "Tablet", "iPod", "Other")
statusTypes = ("Checked Out", "Warranty", "Insurance", "Repair", "Storage", "Missing", "Retired", "MS Loaner", "HS Loaner")
campuses = ("BECS", "BPS", "BES", "BIS", "BMS", "BHS", "PRIDE", "BCO", "T&L", "Transportation", "Operations", "Maintenance")

# connect to database
db = DAL("mysql://{user}:{passwd}@{host}/{dbname}".format(
    user=os.environ["MYSQL_USER"],
    passwd=os.environ["MYSQL_PASS"],
    host=os.environ["MYSQL_HOST"],
    dbname=os.environ["MYSQL_DATABASE"],
), migrate=False)

# define device table
db.define_table("devices",
Field("Inventory_Number", "string",unique=True),\
Field("Serial_Number", "string",unique=True),\
Field("Bag_Tag", "string"),\
Field("Status", "string",requires=IS_IN_SET(statusTypes,zero="Choose Status")),\
Field("User", "string"),\
Field("Device_Type", "string",requires=IS_IN_SET(deviceTypes,zero="Choose Type")),\
Field("Manufacturer", "string"),\
Field("Model", "string"),\
Field("Campus", "string", requires=IS_EMPTY_OR(IS_IN_SET(campuses))),\
Field("Room", "string"),\
Field("Notes", "text"),\
Field("Flags", "text", writable=False, represent=lambda val, row: [v.strip() for v in val.strip().split(",")])\
)

class IS_CHARGE(object):
    def __init__(self):
        pass
    def __call__(self, value):
        try:
            if value == "":
                return (value, None)
            line = value.split(":")
            if len(line) != 2:
                raise RuntimeError, "Incorrect number of :"
            float(line[1])
            return (value, None)
        except:
            return (value, "Must be <text description>:<numeric cost>")

# define charge table
db.define_table("charges",
Field("Inventory_Number", "string", requires=[IS_IN_DB(db,"devices.Inventory_Number")]),\
Field("User", "string", requires=IS_NOT_EMPTY()),\
Field("Amount_Paid", "double", default=0.0, requires=IS_NOT_EMPTY()),\
Field("Charges", "list:string", requires=IS_LIST_OF(IS_CHARGE())),\
Field("Notes", "text")
)

# define verifications table
db.define_table("verifications",
Field("date", "datetime", requires=IS_NOT_EMPTY()),\
Field("username", "string", requires=IS_NOT_EMPTY()),\
Field("device_id", "integer", requires=[IS_IN_DB(db,"devices.id")]),\
)

# authentication - http://www.web2pyslices.com/slice/show/1468/how-to-set-up-web2py-ldap-with-windows-active-directory
auth = Auth(db, hmac_key=Auth.get_or_create_key())
auth.define_tables(username=True)
auth.settings.create_user_groups=False

# all we need is login
auth.settings.actions_disabled=["register", "change_password", "request_reset_password", "retrieve_username", "profile"]

# you don't have to remember me
auth.settings.remember_me_form = False

auth.settings.expiration = int(os.environ.get("INVENTORY_SESSION_EXPIRATION", 3600))

# ldap authentication and not save password on web2py
auth.settings.login_methods = [ldap_auth(
    mode="ad",
    allowed_groups = [g.strip() for g in os.environ["AD_ALLOWED_GROUPS"].split(",")],
    server=os.environ["AD_HOST"],
    base_dn=os.environ["AD_BASE_DN"],
    bind_dn=os.environ["AD_BIND_USER"],
    bind_pw=os.environ["AD_BIND_PASS"],
    group_dn=os.environ["AD_GROUP_DN"],
    group_name_attrib="cn",
    group_member_attrib="member",
    group_filterstr="objectClass=Group",
)]

# set up special user permissions
def view_only_create(form):
    form.errors.Inventory_Number = "User cannot create record"

def view_only_update(form):
    form.errors.Inventory_Number = "User cannot update record"

# allow login with API key
def requires_login_or_key():
    if request.env.http_x_api_key == os.environ["REPORT_API_KEY"]:
        return lambda fn: fn
    return auth.requires_login()

crud = Crud(db)

try:
    if auth.user.username in [u.strip() for u in os.environ.get("INVENTORY_DELETE_USERS", "").split(",")]:
        crud.settings.update_deletable = True
    else:
        crud.settings.update_deletable = False
    if auth.user.username in [u.strip() for u in os.environ.get("INVENTORY_VIEW_ONLY_USERS", "").split(",")]:
        crud.settings.create_onvalidation = view_only_create
        crud.settings.update_onvalidation = view_only_update
# no user
except AttributeError:
    pass
