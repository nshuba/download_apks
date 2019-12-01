#!/usr/bin/python3

"""
Downloads APKs based on the provided CSV file

USAGE:
$ python3 download_apks.py <gsfId> <authSubToken> <apps.csv> <output_dir>
"""
from gpapi.googleplay import GooglePlayAPI, RequestError

import argparse, time
import csv

from constants import Constants

key_dev = "author"

server = GooglePlayAPI("en_US", "UTC")

def process_csv(csv_reader, csv_writer):
    header_row = next(csv_reader)
    pkg_name_idx = header_row.index(Constants.key_pkg_name)
    apps_set = set()
    for row in csv_reader:
        apps_set.add(row[pkg_name_idx])

    apps_list = list(apps_set)
    app_details = server.bulkDetails(apps_list)

    missed_apps = []
    for i in range(len(apps_list)):
        pkg_name = apps_list[i]
        print('Processing %s' % pkg_name)

        app_info = app_details[i]
        dev = "" if app_info is None else app_info[key_dev]
        if dev is None or len(dev) == 0:
            #print("\tCould not find info. App may have been deleted.")
            missed_apps.append(pkg_name)
            continue

        # Because of a bug, also write down a trimmed package name for easier SQL later
        row = [pkg_name, pkg_name[:len(pkg_name)-1], dev]
        csv_writer.writerow(row)

    # Try to fetch missed apps again, after a pause (sometimes Google APIs fail randomly)
    print("\nAttempting to re-fetch missed apps...")
    time.sleep(10)
    for pkg_name in missed_apps:
        try:
            app_info = server.details(pkg_name)
            dev = app_info[key_dev]
        except RequestError:
            print("\tCould not find info. App has been deleted.")
            dev = ""

        # Because of a bug, also write down a trimmed package name for easier SQL later
        row = [pkg_name, pkg_name[:len(pkg_name)-1], dev]
        csv_writer.writerow(row)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Gets developer data about provided apps")
    ap.add_argument('gsf_id', type=int)
    ap.add_argument('auth_sub_token')
    ap.add_argument('apps_csv', help='CSV file containing package names of apps of interest')
    ap.add_argument('out_csv', help='CSV file to write to')
    args = ap.parse_args()

    server.login(None, None, args.gsf_id, args.auth_sub_token)

    with open(args.apps_csv, "r", newline="") as read_file, \
         open(args.out_csv, "w", newline="") as write_file:
        csv_reader = csv.reader(read_file, delimiter=',')
        header_row = [Constants.key_pkg_name, "package_name", key_dev]
        csv_writer = csv.writer(write_file)
        csv_writer.writerow(header_row)
        process_csv(csv_reader, csv_writer)

