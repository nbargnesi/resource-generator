#!/usr/bin/env python3
# coding: utf-8

'''
 gp_baseline.py

 The entrance point to the program. gp_baseline calls out to
 namespace.py, equiv.py, and annotate.py to construct various
 .bel files.

 inputs:
   -b    resource-generator phase to begin at
   -e    resource-generator phase to end at
   -n	 the directory to store the new equivalence data
   -v	 enables verbose mode

'''

from configuration import baseline_data
import argparse
import os
import namespaces
import parsed
import time
#import equiv
import shutil
import annotate
from common import download
from constants import PARSER_TYPE, RES_LOCATION

# collect paths needed for proper resource file location
import sys
# script source path
if sys.argv[0].find('/') < 0:
	src_dir = '.'
else:
	src_dir = sys.argv[0][:sys.argv[0].rfind('/')]
# script execution path
cwd = os.getcwd()
# allow for successful import of equiv module
# - equiv.py attempts to load data from [cwd]/datasets/meshcs_to_gocc.csv
#	using os.getcwd() for value of [cwd]
# - if gp_baseline is not launched from its source directory, the import fails
os.chdir(src_dir)
# assure full path is saved
src_dir = os.getcwd()
#print('* src_dir =', src_dir)
import equiv
os.chdir(cwd)

parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-v", "--verbose", required=False, action="store_true",
					help="enable verbose program output")
parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
parser.add_argument("-b", "--begin_phase", type=int, choices=[1, 2, 3, 4, 5], default = 1,
					help="resource-generator phase to begin at")
parser.add_argument("-e", "--end_phase", type=int, choices=[1, 2, 3, 4, 5], default = 5,
					help="resource-generator phase to end at")
args = parser.parse_args()

verbose = args.verbose
if verbose:
	print('\nRunning gp_baseline in verbose mode.\n')
	
if args.begin_phase > args.end_phase:
	args.end_phase = args.begin_phase
	print('Reseting end phase to match begin phase: %d.' % (args.end_phase))

resource_dir = args.n[0]
if not os.path.exists(resource_dir):
	os.mkdir(resource_dir)

# change to resource directory
os.chdir(resource_dir)

# make dataset directory
if not os.path.exists('datasets'):
	os.mkdir('datasets')

# bring in some dependancies
dep_files = []
dep_files.append('meshcs_to_gocc.csv')
dep_files.append('SDIS_to_DO.txt')
dep_files.append('SCHEM_to_CHEBIID.txt')
dep_files.append('named_complexes_to_GOCC.csv')
dep_files.append('test')
for df in dep_files:
	if not os.path.exists(src_dir+'/datasets/'+df):
		print('WARNING !!! Dependency file %s not found in %s/datasets/' % (df, src_dir))
	else:
		shutil.copy(src_dir+'/datasets/'+df, os.getcwd()+'/datasets')
		if verbose:
			print('Copying dependency file %s to %s/datasets/' % (df, os.getcwd()))

#shutil.copy(src_dir+'/datasets/meshcs_to_gocc.csv', os.getcwd()+'/datasets')
#shutil.copy(src_dir+'/datasets/SDIS_to_DO.txt', os.getcwd()+'/datasets')
#shutil.copy(src_dir+'/datasets/SCHEM_to_CHEBIID.txt', os.getcwd()+'/datasets')
#shutil.copy(src_dir+'/datasets/named_complexes_to_GOCC.csv', os.getcwd()+'/datasets')

start_time = time.time()

if args.begin_phase <= 1:
	print('\n======= Phase I, downloading data =======')
	for name, url_tuple in baseline_data.items():
		if verbose:
			print('Downloading ' +str(name))
		path = os.path.join('datasets/', name)
		if url_tuple[RES_LOCATION].startswith('http') or \
				url_tuple[RES_LOCATION].startswith('ftp'):
			download(url_tuple[RES_LOCATION], path)
	print('Phase 1 ran in %.3f minutes' % ((time.time() - start_time) / 60))
else:
	print('\nSkipping phase 1.')

#sys.exit()

print('\n======= Phase II, parsing data =======')
# For now, download and store the data in the parsed.py module. This module
# could be replaced or re-implemented using something like DBM to help with
# memory usage.
interval_time = time.time()
working_dir = os.getcwd()
for root, dirs, filenames in os.walk(working_dir):
	for f in filenames:
		if f in baseline_data:
			data_tuple = baseline_data.get(f)
			parser = data_tuple[PARSER_TYPE]('datasets/'+f)
			if verbose:
				parser.is_verbose()
				print('Running ' +str(parser))
			for x in parser.parse():
				parsed.build_data(x, str(parser))
print('Phase II ran in %.3f minutes' % ((time.time() - interval_time) / 60))

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
nch = parsed.load_data('nch')
ctg = parsed.load_data('ctg')
gobp = parsed.load_data('gobp')
gocc = parsed.load_data('gocc')
# pub_eq = parsed.load_data('pubchem_equiv')
# pub_ns = parsed.load_data('pubchem_namespace')
mesh = parsed.load_data('mesh')
do = parsed.load_data('do')

# does NOT include pubchem currently
ns_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, mesh, schem, do, sdis, nch]
for d in ns_data:
	if verbose:
		print('Generating namespace file for ' +str(d))
	namespaces.make_namespace(d, verbose)
print('Phase III ran in %.3f minutes' % ((time.time() - interval_time) / 60))

print('\n======= Phase IV, building annotations =======')
# There are 3 .belanno files to generate from the MeSH dataset.
interval_time = time.time()
annotate.make_annotations(mesh)
print('Phase IV ran in %.3f minutes' % ((time.time() - interval_time) / 60))

print('\n======= Phase V, building equivalences =======')
# Any datasets producing a .beleq file should be added to equiv_data
interval_time = time.time()
equiv_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, do, mesh, sdis_to_do,
              schem_to_chebi, nch]
for d in equiv_data:
	if verbose:
		print('Generating equivalence file for ' +str(d))
	equiv.equiv(d, verbose)
print('Phase V ran in %.3f minutes' % ((time.time() - interval_time) / 60))

print('\n======= Phase VI, finished! =======')
print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
