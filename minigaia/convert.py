#!/usr/bin/env python3
#
# minigaia_convert.py - Víctor R. Ruiz <rvr@infoastro.com>
# Converts Gaia DR2 CSV files to binary format
#
import argparse
import csv
import gzip

from pathlib import Path
from struct import pack

from minigaia.dr2 import columns as gaia_dr2_columns

gaia_pack_types = {
    'boolean': '?',
    'byte': 'B',
    'short': 'h',
    'int': 'i',
    'long': 'L',
    'float': 'f',
    'double': 'd',
    'string': '255p',  # Pascal string: https://docs.python.org/3/library/struct.html
}


def gaia_pack_format(columns):
    """ Returns the pack string """
    pack_string = ''
    # Read columns
    for column in columns:
        if column not in gaia_dr2_columns:
            # There is a column that doesn't exist in Gaia DR2
            return None
        column_type = gaia_dr2_columns[column][1]
        if column_type not in gaia_pack_types:
            # Type not supported
            print(f"Type {column_type} of column {column} not supported")
            exit(1)
        # Add type to pack format string
        pack_string += gaia_pack_types[column_type]
    return pack_string


def string_to_binary(string, to_type):
    """ Converts a string into the desired type """
    b = None
    if to_type == 'b':
        # Boolean
        b = int(string)
    elif to_type == 'B':
        # Byte
        b = int(string)
    elif to_type == 'h':
        # Short
        b = int(string)
    elif to_type == 'i':
        # Integer
        b = int(string)
    elif to_type == 'L':
        # Long
        b = int(string)
    elif to_type == 'f':
        # Float
        b = float(string)
    elif to_type == 'd':
        # Double
        b = float(string)
    elif to_type == '255p':
        # String
        b = string
    else:
        print(f"Unsupported type \"{to_type}\" for value \"{string}\".")
        exit(1)
    return b


def gaia2db(path, db_file, columns):
    """ Reads Gaia DR2 csv.gz files and convert them to binary format """
    # Check columns
    db_format = gaia_pack_format(columns)
    column_names = ' '.join(columns)
    if (len(column_names) > 255):
        print('Warning: Not all column names can be stored in the db header (>255 characters).')
    # Create database
    db_file = open(db_file, 'wb')
    # Headers
    db_file.write(pack('256p', 'Mini Gaia DB 1.0'.encode('ascii')))
    db_file.write(pack('256p', db_format.encode('ascii')))
    db_file.write(pack('256p', column_names.encode('ascii')))
    # Open list of Gaia DR2 files
    gaia_path = Path(path)
    for file_name in gaia_path.glob('*.csv.gz'):
        # Read CSV gzipped file
        with gzip.open(file_name, 'rt') as csvfile:
            print(file_name)
            reader = csv.DictReader(csvfile)
            n = 0
            # Read rows (stars)
            for row in reader:
                binary_values = []
                for column in columns:
                    # Convert column values
                    binary_values.append(string_to_binary(row[column], gaia_pack_types[gaia_dr2_columns[column][1]]))
                # Pack values
                s = pack(db_format, *binary_values)
                # Write
                db_file.write(s)
                n += 1
            # Display number of stars read
            print(n)
    db_file.close()


def main():
    # Parse the arguments
    # Example:
    # $ minigaia_convert -p /home/rvr/gaia/ -o gaia2pos.db -c source_id ra dec
    parser = argparse.ArgumentParser(description='Process Gaia DR2 database to create a binary format file.')
    parser.add_argument('-p', '--path', help='Path to Gaia DR2 files (csv.gz).', required=True)
    parser.add_argument('-o', '--output', help='Name file of the output.', required=True)
    parser.add_argument('-c', '--columns', nargs='+', help='', required=True)
    args = parser.parse_args()

    # Check column names and types
    for column in args.columns:
        if column not in gaia_dr2_columns:
            print(f"Column {column} is not listed in Gaia DR2")
            exit(1)
        column_type = gaia_dr2_columns[column][1]
        if column_type not in gaia_pack_types:
            print(f"Type {column_type} of column {column} not supported")
            exit(1)
    binary_format = gaia_pack_format(args.columns)
    print(f"Format: {binary_format}")

    print(args.columns)
    gaia2db(args.path, args.output, args.columns)


if (__name__ == '__main__'):
    main()
