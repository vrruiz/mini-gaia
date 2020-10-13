#!/usr/bin/env python3
#
# metadata.py - Víctor R. Ruiz <rvr@infoastro.com>
# Displays database metadata
#
import argparse

from minigaia.db import MiniGaiaDB

# Read arguments
parser = argparse.ArgumentParser(description='Reads Mini Gaia DR2 database.')
parser.add_argument('-db', '--database', help='Mini Gaia file path', required=True)
args = parser.parse_args()

# Open database
gaia = MiniGaiaDB(args.database)

# Display metadata
print(f"Version: {gaia.version()}")
print(f"Columns: {gaia.columns()}")
print(f"Records: {gaia.record_number()}")
