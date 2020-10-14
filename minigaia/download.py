#!/usr/bin/env python3
#
# minigaia_download.py - Víctor R. Ruiz <rvr@infoastro.com>
# Downloads Gaia DR2 database
#

import argparse
import re
import os
import path
import urllib.request

from urllib.parse import urljoin
from time import sleep


def download_gaia(dest_path, files):
    """ Download Gaia DR2 CSV files to destination path """
    for f in files:
        # Get URL and file name
        file_url, file_name = f
        print(file_name)
        file_path = os.path.join(path, file_name)
        # Download data (if not already)
        if (not os.path.exists(file_path) and not os.path.isfile(file_path)):
            print("Downloading {}...".format(file_name))
            response = urllib.request.urlopen(file_url)
            data = response.read()
            tar_gz = open(file_path, 'wb')
            tar_gz.write(data)
            tar_gz.close()
            # Be nice
            sleep(1)


def download_index(gaia_index):
    """ Read index page and extract file list to download (URL, file name) """
    # Create regex to extract URL and file name
    reFile = re.compile(r'<a href="(.*(GaiaSource.*gz))"\>')
    # Open Gaia HTML index file
    response = urllib.request.urlopen(gaia_index)
    # Read content
    files = []
    page = response.readlines()
    # Extract URLs from the page
    for line in page:
        line = line.decode('utf-8')
        # Extract URLs
        f = reFile.findall(line)
        if (f):
            f = f[0]
            if (f[0].startswith('http')):
                # Absolute path
                files.append((f[0], f[1]))
            else:
                # Relative path
                files.append((urljoin(gaia_index, f[0]), f[1]))
    if len(files) == 0:
        print(f"Couldn't extract file names from the index page.\nCheck URL: {gaia_index}")
        exit(1)
    return files


def main():
    # Parse the arguments
    # Example:
    # $ minigaia_download -p /tmp/gaiadr2/
    gaia_index = 'http://cdn.gea.esac.esa.int/Gaia/gdr2/gaia_source/csv/'
    parser = argparse.ArgumentParser(description='Reads Mini Gaia DR2 database.')
    parser.add_argument('-p', '--path', help='Destination of files', required=False, default='.')
    parser.add_argument('-u', '--url', help='Gaia DR2 index URL', required=False, default=gaia_index)
    args = parser.parse_args()
    gaia_path = args.path
    gaia_url = args.url

    # Check whether destionation path exists
    if not os.path.exists(gaia_path):
        print(f"Destination path {path} doesn't exist. Existing path is required.")
        exit(1)

    # Get list of files (URLs)
    gaia_files = download_index(gaia_url)
    # Download list
    download_gaia(gaia_path, gaia_files)


if (__name__ == '__main__'):
    main()
