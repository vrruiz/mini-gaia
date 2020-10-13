#!/usr/bin/env python3
#
# minigaia.db - Víctor R. Ruiz <rvr@infoastro.com>
# Reads a Mini Gaia DR2 binary format database file
#
import os

from struct import unpack, calcsize

VERSION_STRING = 'Mini Gaia DB 1.0'


class MiniGaiaDB():
    """ Reads Mini Gaia DR2 database file """

    def __init__(self, file_name):
        """ Reads Mini Gaia DR2 database file """

        # Variable definitions
        self._file_name = file_name  # File name
        self._headers = {}           # Headers
        self._columns = []           # List of column names
        self._record_size = 0        # Record size, calculated using format
        self._record_number = 0      # Number of records
        self._records_start = 0      # File position for record start
        self._records_end = 0        # End of file position

        # Open file
        self._db_file = open(file_name, 'rb')
        # Read headers
        self._headers['version'] = unpack('256p', self._db_file.read(256))[0].decode('ascii')
        self._headers['format'] = unpack('256p', self._db_file.read(256))[0].decode('ascii')
        self._headers['columns'] = unpack('256p', self._db_file.read(256))[0].decode('ascii')
        self._columns = self._headers['columns'].split(' ')
        # Check header sanity
        if (self._headers['version'] != VERSION_STRING):
            raise "Expected version. Incorrect file? {file_name}"
        if (len(self._columns) != len(self._headers['format'])):
            raise "Number of columns differs from format fields."
        # Calculate record size
        self._record_size = calcsize(self._headers['format'])
        if (self._record_size < 1):
            raise "Record size equals zero. Incorrect database format? {file_name}"
        # Calculate number of records
        self._records_start = self._db_file.tell()
        self._db_file.seek(0, os.SEEK_END)
        self._records_end = self._db_file.tell()
        self._record_number = (self._records_end - self._records_start) / self._record_size

    def headers(self):
        """ Return database headers """
        return self._headers

    def version(self):
        """ Return database version """
        return self._headers['version']

    def format(self):
        """ Return database format """
        return self._headers['format']

    def columns(self):
        """ Return database columns """
        return self._headers['columns']

    def record_size(self):
        """ Return record size """
        return self._record_size

    def record_number(self):
        """ Return record number """
        return self._record_number

    def __iter__(self):
        """ Iterate """
        self.n = 0
        # Go to first record
        self._db_file.seek(self._records_start)
        return self

    def __next__(self):
        """ Next item """
        record = self._db_file.read(self._record_size)
        if record:
            # Decode record
            values = unpack(self._headers['format'], record)
            row = dict(zip(self._columns, values))
            return row
        else:
            raise StopIteration
