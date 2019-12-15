#!/usr/bin/python3

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

import argparse
import os
import itertools
import csv

from gpapi.googleplay import GooglePlayAPI, RequestError
from constants import Constants

def prep_app_list(server, apps_csv):
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

def download_apks(server, apps_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(apps_file, "r", newline="") as readfile:
        # Get headers
        reader = csv.reader(readfile, delimiter=',')
        header_row = next(reader)
        pkg_name_idx = header_row.index(Constants.key_pkg_name)

        for row in reader:
            pkg_name = row[pkg_name_idx]

            # Download
            print('Attempting to download %s' % pkg_name)
            apk_file_path = output_dir + "/" + pkg_name + '.apk'
            if os.path.isfile(apk_file_path):
                print('\tSkipping - already exists')
                continue
            fl = server.download(pkg_name)
            with open(apk_file_path, 'wb') as apk_file:
                for chunk in fl.get('file').get('data'):
                    apk_file.write(chunk)
                print('\tDownload successful')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="If you don't use the option parameter `output_dir`," +
            " then this script creates a CSV file with a list of top 10 free apps from each" +
            " Google Play category. Otherwise, it downloads the APKs corresponding to apps in the" +
            " provided `apps_csv` parameter.")
    ap.add_argument('gsf_id', type=int, help="gsfId from the prep_token_id script")
    ap.add_argument('auth_sub_token', help="authSubToken from the prep_token_id script")
    ap.add_argument('apps_csv', help='CSV file to write/read app data to/from')
    ap.add_argument('--output_dir',
                    help='Directory to which you want to save APKs corresponding to package names' +
                         ' in `apps_csv`. Use this argument when ready to download APKs.')
    args = ap.parse_args()

    server = GooglePlayAPI("en_US", "UTC")
    server.login(None, None, args.gsf_id, args.auth_sub_token)

    if not args.output_dir:
        prep_app_list(server, args.apps_csv)
    else:
        download_apks(server, args.apps_csv, args.output_dir)


            