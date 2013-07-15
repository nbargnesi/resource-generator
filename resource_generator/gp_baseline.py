#!/usr/bin/env python3
# coding: utf-8
#
# gp_baseline.py
# inputs:
#   -o    old namespace/equivalence dictionary file
#         (built with build_equivalence.py)
#   -n    the directory to store the equivalence data
#   -v    enables verbose mode

from common import download
from configuration import path_constants, gp_datasets, gp_reference_info, \
     gp_reference_history
import argparse
import os
import pdb
import pickle
import tarfile
import json
import pdb
import namespaces
import equiv
import write
import time

# start program timer
start_time = time.time()
parser = argparse.ArgumentParser(description="""Generate namespace and
                               equivalence files for gene/protein datasets.""")
parser.add_argument("-o", required=False, nargs=1, metavar="EQUIVALENCE FILE",
                    help="The old namespace equivalence dictionary file.")
parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
                    help="""The directory to store the new namespace
                            equivalence data.""")
parser.add_argument("-v", required=False, action="store_true",
                    help="This enables verbose program output.")
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

# parse reference dataset INFO (entrez gene)
for path, url in gp_reference_info.file_to_url.items():
    download(url, path)

parser = gp_reference_info.parser_class(gp_reference_info.file_to_url)
print("Running " + str(parser))

entrez_info_dict = parser.parse()
with open('entrez_info.txt', 'wb') as f:
    for x in entrez_info_dict:
        namespaces.make_namespace(x, parser)
        # generate a new UUID for all entrez (only first time though!)
        equiv.equiv(x.get('GeneID'), 'entrez')
        equiv.make_eq_dict(x.get('GeneID'),
                           x.get('Symbol_from_nomenclature_authority'),
                           x.get('tax_id'))
        pickle.dump(x, f)

# parse reference dataset HISTORY (entrez gene)
for path, url in gp_reference_history.file_to_url.items():
    download(url, path)

parser = gp_reference_history.parser_class(gp_reference_history.file_to_url)
print("Running " + str(parser))

gene_history_dict = parser.parse()
with open('entrez_history.txt', 'w') as f:
    for x in gene_history_dict:
        json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

# parse dependent datasets
for d in gp_datasets:
    p_time = time.time()
    for path, url in d.file_to_url.items():
        download(url, path)
        parser = d.parser_class(d.file_to_url)
        print('Running ' +str(parser))
        #pool = ['RGD_Parser', 'MGI_Parser', 'SwissProt_Parser', 'HGNC_Parser']
        #if str(parser) in pool:
        #    break
        for x in parser.parse():
            if str(parser) == 'Gene2Acc_Parser':
                # to be used in affy probe set equivalencing
                equiv.build_refseq(x)
            if str(parser) == 'SwissProt_Parser':
                # this method contains a boolean value to ensure it is only
                # called once (the first iteration).
                equiv.build_equivs()
                namespaces.make_namespace(x, parser)
            else:
                # put together the namespace file for each dataset
                namespaces.make_namespace(x, parser)
        print(str(parser) +' ran in ' +str(((time.time() - p_time) / 60)) \
                  +' minutes')

equiv.finish()
print('Completed gene protein resource generation.')
print('Writing namespaces to file ...')
write.write_out()
write.changes()

# print runtime of the program
print('Total runtime is ' +str(((time.time() - start_time) / 60)) +' minutes')
with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
