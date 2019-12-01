#!/usr/bin/python3

"""
Downloads APKs based on the provided CSV file

USAGE:
$ python3 download_apks.py <gsfId> <authSubToken> <apps.csv> <output_dir>
"""
from gpapi.googleplay import GooglePlayAPI, RequestError

import sys
import os
import itertools
import csv

from constants import Constants

server = GooglePlayAPI("en_US", "UTC")

gsfId = int(sys.argv[1])
authSubToken = sys.argv[2]
apps_file = sys.argv[3]
output_dir = sys.argv[4]

server.login(None, None, gsfId, authSubToken)

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
