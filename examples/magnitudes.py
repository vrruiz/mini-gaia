#!/usr/bin/env python3
#
# magnitudes.py - Víctor R. Ruiz <rvr@infoastro.com>
# Calculates the magnitude distribution of a Mini Gaia DR2 database
#
import argparse
import math

from minigaia.db import MiniGaiaDB

# Read arguments
parser = argparse.ArgumentParser(description='Reads Mini Gaia DR2 database.')
parser.add_argument('-db', '--database', help='Mini Gaia file path', required=True)
args = parser.parse_args()

# Open database
gaia = MiniGaiaDB(args.database)

# Calculate magnitude distribution
total = 0
magnitudes = [0 for i in range(28)]
for star in gaia:
    (d, mag) = math.modf(star['phot_g_mean_mag'])
    mag = int(mag)
    magnitudes[mag] += 1
    total += 1

# Display magnitude distribution
for i, n in enumerate(magnitudes):
    percentage = n / total * 100
    print(f"Mag {i}: {n} ({percentage}%)")
