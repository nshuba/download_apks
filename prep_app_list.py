#!/usr/bin/python3

"""
Creates a CSV file with a list of top 10 free apps from each Google Play category

USAGE:
$ python3 prep_app_list.py <gsfId> <authSubToken> <output.csv>
"""

from gpapi.googleplay import GooglePlayAPI, RequestError

import sys
import os
import itertools
import csv

from constants import Constants

server = GooglePlayAPI("en_US", "UTC")

# Provide tokens as arguments
gsfId = int(sys.argv[1])
authSubToken = sys.argv[2]
output_file = sys.argv[3]

# Running for the second time - use tokens
server.login(None, None, gsfId, authSubToken)

# Keys for app data
top_free_cat = 'apps_topselling_free'
key_agg_rat = 'aggregateRating'

app_limit = 10
categories = server.browse()
with open(output_file, "w", newline="") as writefile:
    # Prepare csv columns
    writer = csv.writer(writefile)
    writer.writerow([Constants.key_pkg_name, Constants.key_app_name, Constants.key_category,
                        Constants.key_rating, Constants.key_num_rat, Constants.key_num_down])
                        
    # Pick 10 apps top free apps from each category
    for c in categories:
        category = c['catId']
        print(category)        
        
        top_free = server.list(category, top_free_cat)
        for app in itertools.islice(top_free, 0, app_limit):
            print("\t" + app[Constants.key_pkg_name])
            agg_rating = app[key_agg_rat]
            downloads = int(app[Constants.key_num_down].split('+')[0].replace(",", ""))
            
            row = [app[Constants.key_pkg_name], app[Constants.key_app_name], category,
                    agg_rating[Constants.key_rating], agg_rating[Constants.key_num_rat], downloads]
            writer.writerow(row)
            