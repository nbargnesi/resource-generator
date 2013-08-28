# Project Overview
Python modules to generate BEL resource documents.

## Resource Generation

1. **[gp_baseline.py](https://github.com/OpenBEL/resource-generator/blob/master/gp_baseline.py)** - acts as the driver for the resource-generator.
   This module uses [configuration.py](https://github.com/jhourani/openbel-contributions/blob/master/configuration.py) to determine which parsers to run
   over which datasets. After parsing and stroring the data in a usable
   form, gp_baseline calls out to namespaces.py, annotate.py, and equiv.py
   to generate the new .belns, .belanno, and .beleq files.
2. **[configuration.py](https://github.com/OpenBEL/resource-generator/blob/master/configuration.py)** - matches each dataset to the proper parser. This
   module can be used to customize which parsers to run. To run/not run a
   particular parser, simply uncomment/comment it.
3. **[parsers.py](https://github.com/OpenBEL/resource-generator/blob/master/parsers.py)** - contains parsers for each dataset, and in some cases
   mutiple parsers over the same data. This is mainly due to the fact that
   in some cases *withdrawn* or *deprecated* terms are not included during
   resource generation, but are needed for resolving lost terms in the
   change log. Also included are parsers for the not-yet fully implemented
   PubChem names and IDs namespace.
4. **[parsed.py](https://github.com/OpenBEL/resource-generator/blob/master/parsed.py)** - acts as a storage module. Takes the data handed to it by
   the parser and stores it in a DataObject. Currently all of the data being
   used in this module is being kept in memory. See bug tracker about a
   possible solution to this memory constraint.
5. **[datasets.py](https://github.com/OpenBEL/resource-generator/blob/master/datasets.py)** - each DataObject that holds a particular dataset is
   defined in this module. These objects act as an interface to the underlying
   dictionaries, and do various manipulations over the data to assist in
   generating the BEL resource files.
6. **[namespaces.py](https://github.com/OpenBEL/resource-generator/blob/master/namespaces.py)** - uses the parser instance itself to determine which
   namespace to generate. Properly encodes each term, and writes out each
   .belns file.
7. **[annotate.py](https://github.com/OpenBEL/resource-generator/blob/master/annotate.py)** - simple module that uses the MeSH data set to generate
   .belanno files.
8. **[equiv.py](https://github.com/OpenBEL/resource-generator/blob/master/equiv.py)** - the main function in this module will take a DataObject as
   a parameter, and use that object's defined functions to generate the new
   .beleq files.
8.  **[common.py](https://github.com/OpenBEL/resource-generator/blob/master/common.py)** - defines some common functions used throughout the program,
   namely a download() function and a function that will open and read a
   `gzipped` file.
9. **[constants.py](https://github.com/OpenBEL/resource-generator/blob/master/constants.py)** - any constants used throughout the program are defined
   in this module.

## Change-Log

1. **[change_log.py](https://github.com/OpenBEL/resource-generator/blob/master/change_log.py)** - a separate module from gp_baseline. This module will
   download and parse the old .belns, .belanno, and .beleq files and compare
   those results with the newly generated files that will be locally stored
   from [gp_baseline.py](https://github.com/jhourani/openbel-contributions/blob/master/gp_baseline.py). Currently, change_log.py must be run
   with the flag `-n <res_files>`. `res_files` being the directory in which the
   newly generated resource files are located. The result of running change_log.py
   will be a dictionary mapping all the old terms to either their replacement
   terms or the string `withdrawn`. This dictionary can be consumed by an update
   script to resolve lost terms in older versioned BEL documents.
2. **[changelog_config.py](https://github.com/OpenBEL/resource-generator/blob/master/changelog_config.py)** - the configuration file for change_log.py. Much like
   configuration.py, this module maps which parsers will be needed, and the
   corresponding datasets for those parsers.
3. **[write_log.py](https://github.com/OpenBEL/resource-generator/blob/master/write_log.py)** - the only task for this module is to write the change-log
   data out to a file using a `json` format.

## Dependencies

1. To run these Python scripts, the following software must be installed:
  * [Python 3.x](http://www.python.org/getit/) - modules are written in Python 3.2.3
  * [lxml](http://lxml.de/) - used to parse various XML documents.