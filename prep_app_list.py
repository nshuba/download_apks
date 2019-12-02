#!/usr/bin/python3

"""
Creates a CSV file with a list of top 10 free apps from each Google Play category

USAGE:
$ python3 prep_app_list.py <gsf_id> <auth_sub_token> <apps.csv>
"""

import argparse
import itertools
import csv

from gpapi.googleplay import GooglePlayAPI, RequestError
from constants import Constants

def prep_app_list(gsf_id, auth_sub_token, apps_csv):
    server = GooglePlayAPI("en_US", "UTC")

    # Running for the second time - use tokens
    server.login(None, None, gsf_id, auth_sub_token)

    # Keys for app data
    top_free_cat = 'apps_topselling_free'
    key_agg_rat = 'aggregateRating'

    app_limit = 10
    categories = server.browse()[Constants.key_category]

    with open(apps_csv, "w", newline="") as writefile:
        # Prepare csv columns
        writer = csv.writer(writefile)
        writer.writerow([Constants.key_pkg_name,
                             Constants.key_app_name,
                             Constants.key_developer,
                             Constants.key_category,
                             Constants.key_rating,
                             Constants.key_num_rat,
                             Constants.key_num_down])

        # Pick 10 apps top free apps from each category
        for c in categories:
            category = c["unknownCategoryContainer"]["categoryIdContainer"]["categoryId"]
            print("Fetching apps for category %s" % category)

            top_free = server.list(category, top_free_cat)
            for app in itertools.islice(top_free, 0, app_limit):
                print("\t" + app[Constants.key_pkg_name])

                agg_rating = app[key_agg_rat]
                downloads_line = app['details']['appDetails'][Constants.key_num_down]
                downloads = int(downloads_line.split('+')[0].replace(",", ""))

                row = [app[Constants.key_pkg_name],
                        app[Constants.key_app_name],
                        app[Constants.key_developer],
                        category,
                        agg_rating.get(Constants.key_rating, None),
                        agg_rating.get(Constants.key_num_rat, None),
                        downloads]
                writer.writerow(row)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=
            "Creates a CSV file with a list of top 10 free apps from each Google Play category")
    ap.add_argument('gsf_id', type=int, help="gsfId from the prep_token_id script")
    ap.add_argument('auth_sub_token', help="authSubToken from the prep_token_id script")
    ap.add_argument('apps_csv', help='CSV file to write app data to')
    args = ap.parse_args()

    prep_app_list(args.gsf_id, args.auth_sub_token, args.apps_csv)


            