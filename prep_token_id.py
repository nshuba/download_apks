#!/usr/bin/python3

"""
Creates authentication token and gsfId

USAGE:
$ python3 prep_token_id.py
"""

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
            