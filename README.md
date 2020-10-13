# Mini Gaia DB

Gaia DR2 csv to binary converter.

## Introduction

[Gaia DR2](https://www.cosmos.esa.int/web/gaia/data-release-2) is the second data release of the [Gaia mission](https://www.cosmos.esa.int/web/gaia/) by the [European Space Agency](https://www.esa.int/) (ESA). Gaia is an astrometric mission whose goal is to create a 3D map with the position and characteristics of more than one billion stars of our galaxy, the Milky Way.

Gaia DR2 official release contains ~1.8 billion stars (1.8 x 10^9). The official repository has 61,235 compressed text files which use 500 GB. Its format is CSV (comma separated values). Mini Gaia allows to extract some of the columns from these files and to store them in binary format for fast access:

```
$ minigaia_convert -c source_id ra dec -o gdr2.db -p /tmp/gaiadr2/
```

## Requirements

The official Gaia DR2 files are required. Mini Gaia has a tool to help download them.

### Gaia DR2 download tool

To download Gaia DR2 CSV (compressed) files, run the ``minigaia_download`` command:

```
$ minigaia_download -p /tmp/gaiadr2/
```

**Warning**: This task takes many hours to complete and requires ~500 GB of free disk storage.

## Gaia DR2 data model

Gaia DR2 [data model](https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html) defines 94 columns. Each of these columns has one of these types:

> Boolean, Byte, Double, Float, Integer, Long, String and Short. 

Mini Gaia converts them to binary format. Check the data model page or ``minigaia.dr2.columns`` to select the columns to be converted.

**Note:** The string type is not storage-efficient due to the use of fixed-length strings, which use 256 bytes.

## Installing

To download Mini Gaia, use git:

```
$ git clone https://github.com/vrruiz/minigaia.git
```

To install it on the system:

```
$ cd minigaia.git
$ python3 setup.py install
```

The ``minigaia_download`` and  ``minigaia_convert`` commands will be installed along the module ``minigaia`` and the class ``minigaia.db.MiniGaiaDB``.

## Database generation

To generate a database, use the ``minigaia_convert`` command.

```
$ minigaia_convert -p <path to database> -o <output file> -c <column list>
```

It supports three arguments:

-  ``--path | -p`` to specify the path to Gaia DR2 CSV files.

- ``--output | -o`` to specify the database file name to create.

- ``--columns | -c`` to specify the column names to extract, separated by commas.

This example extracts Source ID, Right Ascension, Declination and G Magnitude.

```
$ minigaia_convert -p /tmp/gaiadr2/ -o gdr2.db -c source_id ra dec phot_g_mean_mag
```

## Reading the database using Python

``minigaia.db`` provides an easy-to-use Python class to read the generated databases, ``MiniGaiaDB``.

```python
#!/usr/bin/env python3
import argparse
from minigaia.db import MiniGaiaDB

# Read arguments
parser = argparse.ArgumentParser(description='Reads Mini Gaia DR2 database.')
parser.add_argument('-db', '--database', help='Mini Gaia file path', required=True)
args = parser.parse_args()

# Open database
gaia = MiniGaiaDB(args.database)

# Display database headers
print(gaia.headers())

# Display first 10 stars
i = 0
for star in gaia:
    print(star['source_id'], star['ra'], star['dec'], star['phot_g_mean_mag'])
    i += 1
    if i > 10:
        break
```

See more in the ``examples`` directory.

## Mini Gaia database format

The Mini Gaia binary database format is very simple and can be read easily with most programming languages. The database has two sections: the header and the records. Although the conversion tool and the provided reader class uses Python's [struct.pack](https://docs.python.org/3/library/struct.html) module to store the data, it can be replicated in other languages.

### Header section

The Mini Gaia header section contains information about the database version and the stored column descriptions. The header section is divided in three headers of 256 bytes. Each header begins with a byte (the length of the string) and then the string itself. The unused bytes are filled with zeros. This string format is called _Pascal strings_.

The three headers are:

- **Version**. Currently, the value is ``Mini Gaia DB 1.0``.

- **Column formats**. An string containing the types of each column. The type is coded in a character. Currently, these formats are supported:

| Format | Type | Bytes |
| --------- | ---- | ----- |
| i | Integer | 4 |
| l | Integer long | 4 |
| f | Float | 4 | 
| d | Double | 8 |
| 255p | String | 256 |

This format is based on Python's [struct](https://docs.python.org/3/library/struct.html) module. Python makes very easy to read them.

- **Column names**. The third header is a Pascal string containing the names of the database columns, separated by a space. Note: Due to the Pascal string being limited to 255 characters, there is a limitation in the number of columns that the database can store. This limit can be easily overcome if needed, though_.

The number and sort of field format and names must match.

### Record section

The size of the database record can be calculated from the  format header. It is the sum of the bytes used by each column type. For example, a simple database containing ``source_id``, ``ra`` and ``dec`` have types long, double and double. Record size is 4 + 8 + 8 = 18.

The provided ``MiniGaiaDB`` class is able to read the headers of a generated database and to parse it correctly, without the need to do any calculation.

## Authors

- **Víctor R. Ruiz** [<rvr@infoastro.com>](mailto:rvr@infoastro.com)

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.