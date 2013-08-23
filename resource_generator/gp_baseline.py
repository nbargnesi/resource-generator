#!/usr/bin/env python3
# coding: utf-8
#
# gp_baseline.py
# inputs:
#   -o    old namespace/equivalence dictionary file
#         (built with build_equivalence.py)
#   -n    the directory to store the equivalence data
#   -v    enables verbose mode


from configuration import baseline_data
import argparse
import os
import namespaces
import parsed
import time
import equiv
import pickle
import ipdb
import annotate
from common import download
from constants import PARSER_TYPE, RES_LOCATION

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

start_time = time.time()
print('\n======= Phase I, downloading data =======')
# for name, url_tuple in baseline_data.items():
#     print('Downloading ' +str(name))
#     path = os.path.join('datasets/', name)
#     if url_tuple[RES_LOCATION].startswith('http') or \
#             url_tuple[RES_LOCATION].startswith('ftp'):
#         download(url_tuple[RES_LOCATION], path)
print('Phase 1 ran in ' +str(((time.time() - start_time) / 60)) +' minutes')

print('\n======= Phase II, parsing data =======')
interval_time = time.time()
working_dir = os.getcwd()
for root, dirs, filenames in os.walk(working_dir):
    for f in filenames:
        if f in baseline_data:
            data_tuple = baseline_data.get(f)
            parser = data_tuple[PARSER_TYPE]('datasets/'+f)
            print('Running ' +str(parser))
            for x in parser.parse():
                parsed.build_data(x, str(parser))
print('Phase II ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')

print('\n======= Phase III, building namespaces =======')
interval_time = time.time()
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
schem = parsed.load_data('schem')
schem_to_chebi = parsed.load_data('schem_to_chebi')
sdis = parsed.load_data('sdis')
sdis_to_do = parsed.load_data('sdis_to_do')
gobp = parsed.load_data('gobp')
gocc = parsed.load_data('gocc')
# pub_eq = parsed.load_data('pubchem_equiv')
# pub_ns = parsed.load_data('pubchem_namespace')
mesh = parsed.load_data('mesh')
do = parsed.load_data('do')

####### This is a cache used in testing - not currently in use. #########

# does not include pubchem currently
# obj_list = [ei, eh, hg, mg, rg, sp, af, g2, chebi, schem, schem_to_chebi,
#             gobp, gocc, mesh]
# for obj in obj_list:
#     with open(str(obj), 'wb') as fp:
#         pickle.dump(obj, fp)

# files = [f for f in os.listdir('.') if os.path.isfile(f)]
# for f in files:
#     if f == 'entrez_info':
#         ei = pickle.load('entrez_info')
#     if f == 'entrez_history':
#         eh = pickle.load('entrez_history')
#     if f == 'hgnc':
#         hg = pickle.load('hgnc')
#     if f == 'mgi':
#         mg = pickle.load('mgi')
#     if f == 'rgd':
#         rg = pickle.load('rgd')
#     if f == 'swiss':
#         sp = pickle.load('swiss')
#     if f == 'affy':
#         af = pickle.load('affy')
#     if f == 'gene2acc':
#         g2 = pickle.load('gene2acc')
#     if f == 'chebi':
#         chebi = pickle.load('chebi')

#pub_eq = pickle.load('puchem_equiv')
#pub_ns = pickle.load('pubchem_ns')
#########################################################################

# does not include pubchem currently
ns_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, mesh, schem, do, sdis]
for d in ns_data:
    print('Generating namespace file for ' +str(d))
    namespaces.make_namespace(d)
print('Phase III ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')

print('\n======= Phase IV, building annotations =======')
interval_time = time.time()
annotate.make_annotations(mesh)
print('Phase IV ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')

# build some references to be used during equivalencing
print('\n======= Phase V, building equivalences =======')
interval_time = time.time()
equiv_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, do, mesh, sdis_to_do,
              schem_to_chebi]
for d in equiv_data:
    print('Generating equivalence file for ' +str(d))
    equiv.equiv(d)
print('Phase V ran in ' +str(((time.time() - interval_time) / 60)) +' minutes')

print('\n======= Phase VI, finished! =======')
print('Total runtime: ' +str(((time.time() - start_time) / 60)) +' minutes')
