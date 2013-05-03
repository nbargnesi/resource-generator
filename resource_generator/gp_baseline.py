#!/usr/bin/env python3
# coding: utf-8
#
# gp_baseline.py
# inputs:
#   -o    old namespace/equivalence dictionary file (built with build_equivalence.py)
#   -n    the directory to store the equivalence data
#   -v    enables verbose mode

from common import download
from configparser import ConfigParser
from configuration import path_constants, gp_datasets #, gp_reference_info, gp_reference_history
import argparse
import errno
import os
import pdb
import pickle
import re
import sys
import tarfile
import parsers
import json

parser = argparse.ArgumentParser(description="Generate namespace and equivalence files for gene/protein datasets.")
parser.add_argument("-o", required=False, nargs=1, metavar="EQUIVALENCE FILE", help="The old namespace equivalence dictionary file.")
parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY", help="The directory to store the new namespace equivalence data.")
parser.add_argument("-v", required=False, action="store_true", help="This enables verbose program output.")
args = parser.parse_args()

if args.o is None:
    print("Generating gene/protein baseline.")
    old_equivalence = None
else:
    old_equivalence = args.o[0]

resource_dir = args.n[0]
if not os.path.exists(resource_dir):
    os.mkdir(resource_dir)

# change to resource directory
os.chdir(resource_dir)

# make dataset directory
if not os.path.exists(path_constants.dataset_dir):
    os.mkdir(path_constants.dataset_dir)

# create empty dictionary to hold all ns values and equivalence
gp_dict = {}

# parse reference dataset INFO (entrez gene)

#for path, url in gp_reference_info.file_to_url.items():
#    download(url, path)
#parser = gp_reference_info.parser_class(gp_reference_info.file_to_url)
#print("Running " + str(parser))

#gene_info_dict = parser.parse()
#with open('entrez_info.txt', 'w') as f:
#    for x in gene_info_dict:
#        json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

# parse reference dataset HISTORY (entrez gene)
#for path, url in gp_reference_history.file_to_url.items():
#    download(url, path)
#parser = gp_reference_history.parser_class(gp_reference_history.file_to_url)
#print("Running " + str(parser))

#gene_history_dict = parser.parse()
#with open('entrez_history.txt', 'w') as f:
#    for x in gene_history_dict:
#        json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

# parse dependent datasets
# print ("before datasets")
for d in gp_datasets:
    for path, url in d.file_to_url.items():
        download(url, path)
        parser = d.parser_class(d.file_to_url)
        print ("Running " + str(parser))
        with open(str(parser) +'.txt', 'w') as f:
            for x in parser.parse():
                json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

print("Completed gene protein resource generation.")
#print("Number of namespace entries: %d" %(len(gp_dict)))

#with open("equivalence.dict", "wb") as df:
#    pickle.dump(gp_dict, df)

with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
