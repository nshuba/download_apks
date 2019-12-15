#!/usr/bin/python3

"""
Creates authentication token and gsfId

USAGE:
$ python3 prep_token_id.py
"""

#  This file is part of NoMoATS <http://athinagroup.eng.uci.edu/projects/nomoads/>.
#  Copyright (C) 2019 Anastasia Shuba.
#
#  NoMoATS is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  NoMoATS is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NoMoATS.  If not, see <http://www.gnu.org/licenses/>.

from gpapi.googleplay import GooglePlayAPI, RequestError

server = GooglePlayAPI("en_US", "UTC")

# Fill in your Google email and password and then run
# Note: you may get an error when running this for the first time
# For me, it worked on the second time
server.login(str("youremail@gmail.com"), str("yourpassword"), None, None)

print("Loggin success. gsfId:")
print(server.gsfId)
print("\nauthSubToken:")
print(server.authSubToken)
            