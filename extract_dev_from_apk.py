#!/usr/bin/python

import argparse
import os, sys, csv
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + "..")
from utils import utils

CERT_FILE_DIR = "META-INF/"
EXPECTED_CERT_FILE_NAME = "CERT"
CERT_FILE_EXT = ".RSA"
EXPECTED_CERT_FILE = EXPECTED_CERT_FILE_NAME + CERT_FILE_EXT
CERT_FILE_PATH = os.path.join(CERT_FILE_DIR, EXPECTED_CERT_FILE)

# $ sudo apt install openjdk-8-jre-headless
def write_unknown(package_name, csv_writer):
    row = [package_name, "", "", ""]
    csv_writer.writerow(row)

def process_app(apk_file, info_dir, csv_writer):
    if not os.path.isdir(info_dir):
        os.mkdir(info_dir)

    # Because of a bug, use a trimmed package name for easier SQL later
    trimmed_pkg_name = apk_file[:apk_file.index(".apk")-1]
    print trimmed_pkg_name

    expected_cert_fp = os.path.join(info_dir, EXPECTED_CERT_FILE)
    if not os.path.isfile(expected_cert_fp):
        apk_full_path = os.path.join(args.apps_dir, apk_file)

        proc = subprocess.Popen(['unzip', "-l", apk_full_path], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # Skip first line
        last_item = 3
        actual_cert_file = CERT_FILE_PATH
        for line in proc.stdout.readlines():
            #print line.rstrip()
            items = line.split()
            if len(items) < last_item:
                continue
            file_info = items[last_item]
            if file_info.startswith(CERT_FILE_DIR) and (file_info.endswith(CERT_FILE_EXT) or
                    file_info.endswith(".DSA")):
                print file_info
                actual_cert_file = file_info
                break

        proc = subprocess.Popen(['unzip', "-j", apk_full_path, actual_cert_file, "-d", info_dir],
                                stderr=subprocess.PIPE)
        if proc.wait() != 0:
            print "\tError occurred during unzipping"
            write_unknown(trimmed_pkg_name, csv_writer)
            return True
        # Save all certs with the same name:
        actual_cert_fp = os.path.join(info_dir, os.path.basename(actual_cert_file))
        if actual_cert_fp != expected_cert_fp:
            os.system('mv %s %s' % (actual_cert_fp, expected_cert_fp))
    else:
        print "\t" + EXPECTED_CERT_FILE + " already extracted, skipping."

    cert_file_path = os.path.join(info_dir, "keytool_output.txt")
    if not os.path.isfile(cert_file_path):
        with open(cert_file_path, "w+") as cert_file:
            proc = subprocess.Popen(['keytool', "-printcert", "-file", expected_cert_fp],
                                    stdout=cert_file)
            if proc.wait() != 0:
                print "\tError occurred during certificate parsing. Exiting."
                write_unknown(trimmed_pkg_name, csv_writer)
                return True
    else:
        print "\tCertificate already extracted, skipping."

    with open(cert_file_path, "r") as cert_file:
        # Parse out owner CN as author, but keep both full lines just in case
        owner_line = None
        issuer_line = None
        for line in cert_file.readlines():
            if line.startswith("Owner: "):
                owner_line = line.rstrip()
                print "\t" + owner_line
            elif line.startswith("Issuer: "):
                issuer_line = line.rstrip()
            if owner_line is not None and issuer_line is not None:
                break
        cn_prefix = " CN="
        o_prefix = " O="
        if o_prefix in owner_line:
            developer = owner_line.split(o_prefix, 1)[1].split(",", 1)[0]
        elif cn_prefix in owner_line:
            developer = owner_line.split(cn_prefix, 1)[1].split(",", 1)[0]

        print developer

        row = [trimmed_pkg_name, developer, owner_line, issuer_line]
        csv_writer.writerow(row)

    return True

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Extracts the developer name from given APK')
    ap.add_argument('apps_dir', type=utils.readable_dir, help='directory containing apks')
    ap.add_argument('out_csv', help='CSV file to write to')
    args = ap.parse_args()

    parent_dir = os.path.dirname(os.path.abspath(args.apps_dir))
    zip_parent_dir = os.path.join(parent_dir, 'unzipped_apks')
    if not os.path.isdir(zip_parent_dir):
        os.makedirs(zip_parent_dir)

    with open(args.out_csv, "wb") as f:
        header_row = [utils.json_key_package_name, "developer", "owner", "issuer"]
        csv_writer = csv.writer(f)
        csv_writer.writerow(header_row)

        for apk_file in os.listdir(args.apps_dir):
            info_dir = os.path.join(zip_parent_dir, apk_file[:apk_file.index(".apk")])
            if not process_app(apk_file, info_dir, csv_writer):
                break
