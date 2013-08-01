#!/usr/bin/env python3
# coding: utf-8
#
# gp_baseline.py
# inputs:
#   -o    old namespace/equivalence dictionary file
#         (built with build_equivalence.py)
#   -n    the directory to store the equivalence data
#   -v    enables verbose mode


from configuration import baseline_data_opt
import argparse
import os
import namespaces
import parsed
import time
import equiv
import pickle
from constants import RES_LOCATION, PARSER_TYPE

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
    old_equivalence = None
else:
    old_equivalence = args.o[0]

resource_dir = args.n[0]
if not os.path.exists(resource_dir):
    os.mkdir(resource_dir)

# change to resource directory
os.chdir(resource_dir)

# make dataset directory
if not os.path.exists('datasets'):
    os.mkdir('datasets')

# test_pool = ['HGNC_Parser', 'MGI_Parser', 'RGD_Parser',
#                  'SwissProt_Parser', 'Affy_Parser', 'Gene2Acc_Parser',
#                  'PUBCHEM_Parser']
#too_much = ['PUBCHEM_Parser']
start_time = time.time()
print('\n======= Phase One, downloading data =======')

# parse dependent datasets, build namespaces & data for equivalencing
for label, data_tuple in baseline_data_opt.items():
    url = data_tuple[RES_LOCATION]
    parser = data_tuple[PARSER_TYPE](url)
    print('Running ' +str(parser))
    for x in parser.parse():
        parsed.build_data(x, str(parser))

print('Phase 1 ran in ' +str(((time.time() - start_time) / 60)) +' minutes')
interval_time = time.time()
print('\n======= Phase Two, building namespaces =======')
# load parsed data to build namespaces
ei = parsed.load_data('entrez_info')
eh = parsed.load_data('entrez_history')
hg = parsed.load_data('hgnc')
mg = parsed.load_data('mgi')
rg = parsed.load_data('rgd')
sp = parsed.load_data('swiss')
af = parsed.load_data('affy')
g2 = parsed.load_data('gene2acc')
chebi = parsed.load_data('chebi')
pub_eq = parsed.load_data('puchem_equiv')
pub_ns = parsed.load_data('pubchem_ns')

obj_list = [ei, eh, hg, mg, rg, sp, af, g2, chebi, pub_eq, pub_ns]
for obj in obj_list:
    with open(str(obj), 'wb') as fp:
        pickle.dump(obj, fp)

data = [ei, hg, mg, rg, sp, af, chebi, pub_ns]

for d in data:
    print('.', end='')
    namespaces.make_namespace(d)

print('Phase 2 ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')
interval_time = time.time()
print('\n======= Phase Three, building equivalencies =======')

# build some references to be used during equivalencing
equiv_data = [ei, hg, mg, rg, sp, af, chebi, pub_eq]
for d in equiv_data:
    equiv.equiv(d)

print('Phase 3 ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')
print('\n======= Phase Four, finished! =======')
print('Total runtime: ' +str(((time.time() - start_time) / 60)) +' minutes')
