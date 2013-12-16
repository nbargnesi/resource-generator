#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import parsed
import pickle
import time
import shutil
import annotate
from common import download
from constants import PARSER_TYPE, RES_LOCATION
import datasets
import rdflib


parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
parser.add_argument("-d", required=True, type=str, 
					help="dataset name")
parser.add_argument("-o", default='symbols', choices=['symbols', 'names', 'data','rdf'], help="output")
args = parser.parse_args()

dataset = args.d

if os.path.exists(args.n[0]):
    os.chdir(args.n[0])
else:
    print('data directory {0} not found!'.format(args.n[0]))
#dataset = 'mg'
if not os.path.exists(dataset+'.parsed_data.pickle'):
    print('WARNING !!! Required pickled data file %s not found.' % (dataset+'.parsed_data.pickle'))
else:
    with open(dataset+'.parsed_data.pickle', 'rb') as f:
        data = pickle.load(f)

from pprint import pprint
if args.o == 'symbols':
	pprint(data.get_synonym_symbols())
if args.o == 'names':
	pprint(data.get_synonym_names())
if args.o == 'data':
    pprint(data.get_dictionary())
if args.o == 'rdf':
	print(data.get_rdf().serialize(format='turtle'))
