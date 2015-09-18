# Project Overview
Python modules to generate BEL resource documents.

See [wiki](https://github.com/OpenBEL/resource-generator/wiki/Adding-new-Namespace-datasets) for information about dataset objects and how to add new datasets.

## Resource Generator

To run:
'./gp_baseline.py -n [dir]'
'[dir]' is the working directory to which data will be downloaded and new files generated.

 [gp_baseline.py](https://github.com/OpenBEL/resource-generator/blob/master/gp_baseline.py) runs in several phases:
 1. data download
 2. data parse (and save as pickled objects)
 3. build .belns (namespace) files
 4. -removed-
 5. build .beleq (equivalence) files
  
 The pipeline can be started and stopped at any phase using the '-b' and '-e' options. This enables re-rerunning the pipeline on stored data downloads and pickled data objects.

1. **[gp_baseline.py](https://github.com/OpenBEL/resource-generator/blob/master/gp_baseline.py)** - acts as the driver for the resource-generator.
2. **[configuration.py](https://github.com/OpenBEL/resource-generator/blob/master/configuration.py)** - Configures the datasets to be included in the resource-generation pipeline, including initialization of the [dataset](https://github.com/OpenBEL/resource-generator/blob/master/datasets.py) objects, specification of a download url, and association with a [parser](https://github.com/OpenBEL/resource-generator/blob/master/parsers.py)
3. **[parsers.py](https://github.com/OpenBEL/resource-generator/blob/master/parsers.py)** - contains parsers for each dataset. 
4. **[parsed.py](https://github.com/OpenBEL/resource-generator/blob/master/parsed.py)** - acts as a storage module. Takes the data handed to it by
   the parser and stores it in a DataObject. Currently all of the data being
   used in this module is being kept in memory. See bug tracker about a
   possible solution to this memory constraint.
5. **[datasets.py](https://github.com/OpenBEL/resource-generator/blob/master/datasets.py)** - each DataObject class  
is defined in this module. See [wiki](https://github.com/OpenBEL/resource-generator/wiki/Dataset-Objects) for     information about DataObject classes, methods, and attributes.
6. **[equiv.py](https://github.com/OpenBEL/resource-generator/blob/master/equiv.py)** - this module will take a DataObject as
   a parameter, and use that object's defined functions to generate the new
   .beleq files.
7.  **[common.py](https://github.com/OpenBEL/resource-generator/blob/master/common.py)** - defines some common functions used throughout the program,
   namely a download() function and a function that will open and read a
   `gzipped` file.
8. **[constants.py](https://github.com/OpenBEL/resource-generator/blob/master/constants.py)** - any constants used throughout the program are defined
   in this module.
9. **[rdf.py](https://github.com/OpenBEL/resource-generator/blob/master/rdf.py)** - loads each pickled dataset object generated by Phase II of gp_baseline and generates triples for each namespace 'concept', including id, preferred label, synonyms, concept type, and equivalences.

## Change-Log

1. **[change_log.py](https://github.com/OpenBEL/resource-generator/blob/master/change_log.py)** - a separate module from gp_baseline. This module will
   download pickled data objects generated by [gp_baseline.py](https://github.com/OpenBEL/resource-generator/blob/master/gp_baseline.py). change_log.py
   outputs a json dictionary mapping old terms to either their replacement
   terms or the string `withdrawn`. This dictionary can be consumed by an update
   script to resolve lost terms in older versioned BEL documents.

## Dependencies

1. To run these Python scripts, the following software must be installed:
  * [Python 3.x](http://www.python.org/getit/) - modules are written in Python 3.2.3
  * [lxml](http://lxml.de/) - used to parse various XML documents.
  * [rdflib](https://github.com/RDFLib) - used by rdf.py
