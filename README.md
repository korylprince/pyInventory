This is a custom Web Interface for Bullard ISD's inventory system written in web2py.
The backend will probably change rapidly over the next few weeks.
I am putting it out here in case anyone finds it of use.

pyInventory
https://github.com/korylprince/pyInventory

#Installing#

Simply add the application folder to your web2py application folder, and copy db.py.def to db.py.

This file contains all configuration options (not very many at the momement.)

If you are installing this for a new database, you need to set migrate=True in the model db.py.
After the tables are created set migrate back to False.

If you are installing over an existing database, but your database metadata got deleted, set migrate=False,fake\_migrate\_all=True to create metadata then remove the fake\_migrate\_all.

To use Active Directory with allowed groups, currently web2py must be patched.
Please see http://www.web2pyslices.com/slice/show/1493/active-directory-ldap-with-allowed-groups on how to set that up.

If you have any issues or questions, email the email address below, or open an issue at:
https://github.com/korylprince/pyInventory/issues

#Usage#

Really, this is just a simplified app similar to web2py's default appadmin, with a few different features.

#Copyright Information#

Some of the css and javascript files have their own third-party licenses.

All other code is Copyright 2012 Kory Prince (korylprince at gmail dot com.) This code is licensed under the GPL v3 which is included in this distribution. If you'd like it licensed under another license then send me an email.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
