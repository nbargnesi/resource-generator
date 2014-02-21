#!/usr/bin/env python3
# coding: utf-8

'''
 gp_baseline.py

 The entrance point to the program. gp_baseline calls out to
 namespace.py, equiv.py, and annotate.py to construct various
 .bel files.

 inputs:
   -b    resource-generator phase to begin at [1,2,3,4,5]
   -e    resource-generator phase to end at [1,2,3,4,5] (>= begin phase)
   -n	 the directory to store the new equivalence data
   -p    pickle file name suffix for parsed data
   -v	 enables verbose mode

 phases:
   1.    data download
   2.    data parser with pickler
   3.    namespace builder
   4.    annotation builder
   5.    equivalence builder

'''

from configuration import *
from configuration import baseline_data
import argparse
import os
import parsed
import pickle
import time
import shutil
import annotate
from common import download
from datasets import NamespaceDataSet
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
parser.add_argument("-p", "--parsed_pickle", type=str, default = 'parsed_data.pickle',
					help="pickle file name suffix for parsed data")
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
	if verbose:
		print('Created resource destination directory:', resource_dir)

# change to resource directory
os.chdir(resource_dir)
if verbose:
	print('Changing to directory:', resource_dir)

# make dataset directory
if not os.path.exists('datasets'):
	os.mkdir('datasets')
	if verbose:
		print('Created datasets directory')
# bring in some dependancies
dep_files = []
#dep_files.append('meshcs_to_gocc.csv')
dep_files.append('SDIS_to_DO.txt')
dep_files.append('SCHEM_to_CHEBIID.txt')
dep_files.append('named_complexes_to_GOCC.csv')
dep_files.append('selventa-protein-families.txt')

for df in dep_files:
	if not os.path.exists(src_dir+'/datasets/'+df):
		print('WARNING !!! Dependency file %s not found in %s/datasets/' % (df, src_dir))
	else:
		shutil.copy(src_dir+'/datasets/'+df, os.getcwd()+'/datasets')
		if verbose:
			print('Copying dependency file %s to %s/datasets/' % (df, os.getcwd()))

# make templates directory
if not os.path.exists('templates'):
	os.mkdir('templates')
	if verbose:
		print('Created templates directory')
for df in os.listdir(src_dir+'/templates'):
	shutil.copy(src_dir+'/templates/'+df, os.getcwd()+'/templates')
	if verbose:
		print('Copying template file %s to %s/templates/' % (df, os.getcwd()))

# make BEL file headers directory
#if not os.path.exists('headers'):
#	os.mkdir('headers')
#	if verbose:
#		print('Created BEL file header directory')

cwd = os.getcwd()

start_time = time.time()

if args.begin_phase <= 1:
	print('\n======= Phase I, downloading data =======')
	for name, url_tuple in baseline_data.items():
		if verbose:
			print('Downloading ' +str(name))
			sys.stdout.flush()
		path = os.path.join('datasets/', name)
	#	if url_tuple[RES_LOCATION].startswith('http') or \
	#			url_tuple[RES_LOCATION].startswith('ftp'):
		loc = url_tuple[RES_LOCATION]
		if any([loc.startswith(x) for x in ['file', 'ftp', 'http']]):
			download(url_tuple[RES_LOCATION], path)
			print(loc)
	print('Phase 1 ran in %.3f minutes' % ((time.time() - start_time) / 60))
	
	if args.end_phase == 1:
		print('\nTerminating process after phase 1 as specified by user.')
		print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
		sys.exit()
else:
	print('\nSkipping phase 1.')

sys.stdout.flush()

if args.begin_phase <= 2:
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
				if len(data_tuple) >= 3:
					data_object = data_tuple[2]			
				for x in parser.parse():
					parsed.build_data(x, str(parser), data_object)
	# pickle parsed data
	# - just do it.... pickle each dataset by name :-(
	with open('ei.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('entrez_info'), f, pickle.HIGHEST_PROTOCOL)
	with open('eh.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('entrez_history'), f, pickle.HIGHEST_PROTOCOL)
	with open('hg.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('hgnc'), f, pickle.HIGHEST_PROTOCOL)
	with open('mg.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('mgi'), f, pickle.HIGHEST_PROTOCOL)
	with open('rg.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('rgd'), f, pickle.HIGHEST_PROTOCOL)
	with open('sp.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('swiss'), f, pickle.HIGHEST_PROTOCOL)
	with open('af.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('affy'), f, pickle.HIGHEST_PROTOCOL)
	with open('g2.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('gene2acc'), f, pickle.HIGHEST_PROTOCOL)
	with open('chebi.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('chebi'), f, pickle.HIGHEST_PROTOCOL)
	with open('schem.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('schem'), f, pickle.HIGHEST_PROTOCOL)
	with open('schem_to_chebi.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('schem_to_chebi'), f, pickle.HIGHEST_PROTOCOL)
	with open('sdis.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('sdis'), f, pickle.HIGHEST_PROTOCOL)
	with open('sdis_to_do.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('sdis_to_do'), f, pickle.HIGHEST_PROTOCOL)
	with open('nch.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('nch'), f, pickle.HIGHEST_PROTOCOL)
	with open('ctg.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('ctg'), f, pickle.HIGHEST_PROTOCOL)
	with open('gobp.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('gobp'), f, pickle.HIGHEST_PROTOCOL)
	with open('gocc.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('gocc'), f, pickle.HIGHEST_PROTOCOL)
	# with open('pub_eq.'+args.parsed_pickle, 'wb') as f:
	#	pickle.dump(parsed.load_data('pubchem_equiv'), f, pickle.HIGHEST_PROTOCOL)
	# with open('pub_ns.'+args.parsed_pickle, 'wb') as f:
	#	pickle.dump( parsed.load_data('pubchem_namespace'), f, pickle.HIGHEST_PROTOCOL)
	with open('meshcl.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('meshcl'), f, pickle.HIGHEST_PROTOCOL)
	with open('meshd.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('meshd'), f, pickle.HIGHEST_PROTOCOL)
	with open('meshpp.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('meshpp'), f, pickle.HIGHEST_PROTOCOL)
	with open('do.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('do'), f, pickle.HIGHEST_PROTOCOL)
	with open('sfam.'+args.parsed_pickle, 'wb') as f:
		pickle.dump(parsed.load_data('sfam'), f, pickle.HIGHEST_PROTOCOL)
	
	print('Phase II ran in %.3f minutes' % ((time.time() - interval_time) / 60))
	
	if args.end_phase == 2:
		print('\nTerminating process after phase 2 as specified by user.')
		print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
		sys.exit()
else:
	print('\nSkipping phase 2.')

sys.stdout.flush()

if args.begin_phase <= 3:
	print('\n======= Phase III, building namespaces =======')
	interval_time = time.time()
	
	# load parsed data to build namespaces
	
	#   check if this is the starting point and pickled data needs to be loaded
	#   or if data exists in memory already
	if args.begin_phase == 3:
		# starting at this phase, so need pickled data files for:
		# [ei, hg, mg, rg, sp, af, chebi, schem, sdis, gobp, gocc, mesh, do, nch]
		# NOTE - these are the data files that generate namespaces
		if not os.path.exists('ei.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('ei.'+args.parsed_pickle))
			ei = None
		else:
			with open('ei.'+args.parsed_pickle, 'rb') as f:
				ei = pickle.load(f)
		if not os.path.exists('hg.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('hg.'+args.parsed_pickle))
			hg = None
		else:
			with open('hg.'+args.parsed_pickle, 'rb') as f:
				hg = pickle.load(f)
		if not os.path.exists('mg.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('mg.'+args.parsed_pickle))
			mg = None
		else:
			with open('mg.'+args.parsed_pickle, 'rb') as f:
				mg = pickle.load(f)
		if not os.path.exists('rg.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('rg.'+args.parsed_pickle))
			rg = None
		else:
			with open('rg.'+args.parsed_pickle, 'rb') as f:
				rg = pickle.load(f)
		if not os.path.exists('sp.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('sp.'+args.parsed_pickle))
			sp = None
		else:
			with open('sp.'+args.parsed_pickle, 'rb') as f:
				sp = pickle.load(f)
		if not os.path.exists('af.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('af.'+args.parsed_pickle))
			af = None
		else:
			with open('af.'+args.parsed_pickle, 'rb') as f:
				af = pickle.load(f)
		if not os.path.exists('chebi.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('chebi.'+args.parsed_pickle))
			chebi = None
		else:
			with open('chebi.'+args.parsed_pickle, 'rb') as f:
				chebi = pickle.load(f)
		if not os.path.exists('schem.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('schem.'+args.parsed_pickle))
			schem = None
		else:
			with open('schem.'+args.parsed_pickle, 'rb') as f:
				schem = pickle.load(f)
		if not os.path.exists('sdis.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('sdis.'+args.parsed_pickle))
			sdis = None
		else:
			with open('sdis.'+args.parsed_pickle, 'rb') as f:
				sdis = pickle.load(f)
		if not os.path.exists('gobp.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('gobp.'+args.parsed_pickle))
			gobp = None
		else:
			with open('gobp.'+args.parsed_pickle, 'rb') as f:
				gobp = pickle.load(f)
		if not os.path.exists('gocc.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('gocc.'+args.parsed_pickle))
			gocc = None
		else:
			with open('gocc.'+args.parsed_pickle, 'rb') as f:
				gocc = pickle.load(f)
		if not os.path.exists('meshcl.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshcl.'+args.parsed_pickle))
			meshcl = None
		else:
			with open('meshcl.'+args.parsed_pickle, 'rb') as f:
				meshcl = pickle.load(f)
		if not os.path.exists('meshd.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshd.'+args.parsed_pickle))
			meshd = None
		else:
			with open('meshd.'+args.parsed_pickle, 'rb') as f:
				meshd = pickle.load(f)
		if not os.path.exists('meshpp.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshpp.'+args.parsed_pickle))
			meshbp = None
		else:
			with open('meshpp.'+args.parsed_pickle, 'rb') as f:
				meshpp = pickle.load(f)
		if not os.path.exists('do.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('do.'+args.parsed_pickle))
			do = None
		else:
			with open('do.'+args.parsed_pickle, 'rb') as f:
				do = pickle.load(f)
		if not os.path.exists('nch.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('nch.'+args.parsed_pickle))
			nch = None
		else:
			with open('nch.'+args.parsed_pickle, 'rb') as f:
				nch = pickle.load(f)
		if not os.path.exists('sfam.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('sfam.'+args.parsed_pickle))
			sfam = None
		else:
			with open('sfam.'+args.parsed_pickle, 'rb') as f:
				sfam = pickle.load(f)
	else:
		# data already in memory	
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
		meshcl = parsed.load_data('meshcl')
		meshd = parsed.load_data('meshd')
		meshpp = parsed.load_data('meshpp')
		do = parsed.load_data('do')
		sfam = parsed.load_data('sfam')
	#for key in parsed.__dict__.keys():
		#if isinstance(key, NamespaceDataSet):
		#print(key)
	ns_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, meshcl, meshpp, meshd, schem, do, sdis, nch, sfam]
	for dataset in ns_data:
		if verbose:
			print('Generating namespace file for ' +str(dataset))
		try:
			dataset.write_ns_values(cwd)
		except:
			print("Unexpected error:", sys.exc_info()[1])
			
	print('Phase III ran in %.3f minutes' % ((time.time() - interval_time) / 60))
	
	if args.end_phase == 3:
		print('\nTerminating process after phase 3 as specified by user.')
		print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
		sys.exit()
else:
	print('\nSkipping phase 3.')

sys.stdout.flush()

if args.begin_phase <= 4:
	print('\n======= Phase IV, building annotations =======')
	# There are 3 .belanno files to generate from the MeSH dataset.
	interval_time = time.time()
	
	#   check if this is the starting point and pickled data needs to be loaded
	#   or if data exists in memory already -> mesh loaded in phase 3
	if args.begin_phase == 4:
		if not os.path.exists('meshd.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshd.'+args.parsed_pickle))
			meshd = None
		else:
			with open('meshd.'+args.parsed_pickle, 'rb') as f:
				meshd = pickle.load(f)
				print('loaded meshd dataset!')	
		if not os.path.exists('meshcl.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshcl.'+args.parsed_pickle))
			meshcl = None
		else:
			with open('meshcl.'+args.parsed_pickle, 'rb') as f:
				meshcl = pickle.load(f)
		if not os.path.exists('meshpp.'+args.parsed_pickle):
			print('WARNING !!! Required pickled data file %s not found.' % ('meshpp.'+args.parsed_pickle))
			meshpp = None
		else:
			with open('meshpp.'+args.parsed_pickle, 'rb') as f:
				meshpp = pickle.load(f)
	
	# NOTE - Phase Iv not implemented!
	#if mesh:
	#	annotate.make_annotations(mesh)
	
	print('Phase IV ran in %.3f minutes' % ((time.time() - interval_time) / 60))
	
	if args.end_phase == 4:
		print('\nTerminating process after phase 4 as specified by user.')
		print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
		sys.exit()
else:
	print('\nSkipping phase 4.')

sys.stdout.flush()

print('\n======= Phase V, building equivalences =======')
# Any datasets producing a .beleq file should be added to equiv_data
interval_time = time.time()

#   check if this is the starting point and pickled data needs to be loaded
#   or if data exists in memory already
#   - check for phase start >= 4 since phase 4 only loads selected data

if args.begin_phase >= 3:
	# Always need these in phase 5 since they were not used in previous phases:
	# [sdis_to_do, schem_to_chebi, ctg, g2]
	if not os.path.exists('schem_to_chebi.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('schem_to_chebi.'+args.parsed_pickle))
		schem_to_chebi = None
	else:
		with open('schem_to_chebi.'+args.parsed_pickle, 'rb') as f:
			schem_to_chebi = pickle.load(f)
	if not os.path.exists('sdis_to_do.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('sdis_to_do.'+args.parsed_pickle))
		sdis_to_do = None
	else:
		with open('sdis_to_do.'+args.parsed_pickle, 'rb') as f:
			sdis_to_do = pickle.load(f)
	if not os.path.exists('ctg.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('ctg.'+args.parsed_pickle))
		ctg = None
	else:
		with open('ctg.'+args.parsed_pickle, 'rb') as f:
			ctg = pickle.load(f)
	if not os.path.exists('g2.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('g2.'+args.parsed_pickle))
		g2 = None
	else:
		with open('g2.'+args.parsed_pickle, 'rb') as f:
			g2 = pickle.load(f)

if args.begin_phase >= 4:
	# started with phase 4 r 5, so still need pickled data files for:
	# [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, do, nch, schem, sdis]
	if not os.path.exists('ei.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('ei.'+args.parsed_pickle))
		ei = None
	else:
		with open('ei.'+args.parsed_pickle, 'rb') as f:
			ei = pickle.load(f)
	if not os.path.exists('hg.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('hg.'+args.parsed_pickle))
		hg = None
	else:
		with open('hg.'+args.parsed_pickle, 'rb') as f:
			hg = pickle.load(f)
	if not os.path.exists('mg.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('mg.'+args.parsed_pickle))
		mg = None
	else:
		with open('mg.'+args.parsed_pickle, 'rb') as f:
			mg = pickle.load(f)
	if not os.path.exists('rg.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('rg.'+args.parsed_pickle))
		rg = None
	else:
		with open('rg.'+args.parsed_pickle, 'rb') as f:
			rg = pickle.load(f)
	if not os.path.exists('sp.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('sp.'+args.parsed_pickle))
		sp = None
	else:
		with open('sp.'+args.parsed_pickle, 'rb') as f:
			sp = pickle.load(f)
	if not os.path.exists('af.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('af.'+args.parsed_pickle))
		af = None
	else:
		with open('af.'+args.parsed_pickle, 'rb') as f:
			af = pickle.load(f)
	if not os.path.exists('chebi.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('chebi.'+args.parsed_pickle))
		chebi = None
	else:
		with open('chebi.'+args.parsed_pickle, 'rb') as f:
			chebi = pickle.load(f)
	if not os.path.exists('nch.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('nch.'+args.parsed_pickle))
		nch = None
	else:
		with open('nch.'+args.parsed_pickle, 'rb') as f:
			nch = pickle.load(f)
	if not os.path.exists('gobp.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('gobp.'+args.parsed_pickle))
		gobp = None
	else:
		with open('gobp.'+args.parsed_pickle, 'rb') as f:
			gobp = pickle.load(f)
	if not os.path.exists('gocc.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('gocc.'+args.parsed_pickle))
		gocc = None
	else:
		with open('gocc.'+args.parsed_pickle, 'rb') as f:
			gocc = pickle.load(f)
	if not os.path.exists('do.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('do.'+args.parsed_pickle))
		do = None
	else:
		with open('do.'+args.parsed_pickle, 'rb') as f:
			do = pickle.load(f)
	if not os.path.exists('schem.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('schem.'+args.parsed_pickle))
		schem = None
	else:
		with open('schem.'+args.parsed_pickle, 'rb') as f:
			schem = pickle.load(f)
	if not os.path.exists('sdis.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('sdis.'+args.parsed_pickle))
		sdis = None
	else:
		with open('sdis.'+args.parsed_pickle, 'rb') as f:
			sdis = pickle.load(f)
	
	#if not os.path.exists('eh.'+args.parsed_pickle):
	#	print('WARNING !!! Required pickled data file %s not found.' % ('eh.'+args.parsed_pickle))
	#	eh = None
	#else:
	#	with open('eh.'+args.parsed_pickle, 'rb') as f:
	#		eh = pickle.load(f)
	#if not os.path.exists('pub_eq.'+args.parsed_pickle):
	#	print('WARNING !!! Required pickled data file %s not found.' % ('pub_eq.'+args.parsed_pickle))
	#	pub_eq = None
	#else:
	#	with open('pub_eq.'+args.parsed_pickle, 'rb') as f:
	#		pub_eq = pickle.load(f)
	#if not os.path.exists('pub_ns.'+args.parsed_pickle):
	#	print('WARNING !!! Required pickled data file %s not found.' % ('pub_ns.'+args.parsed_pickle))
	#	pub_ns = None
	#else:
	#	with open('pub_ns.'+args.parsed_pickle, 'rb') as f:
	#		pub_ns = pickle.load(f)

if args.begin_phase == 5:
	# Already loaded: [ei, hg, mg, rg, sp, af, chebi, schem, sdis, gobp, gocc, do, nch, 
	#                  sdis_to_do, schem_to_chebi, ctg]
	# still need data files for: [mesh]
	if not os.path.exists('meshd.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('meshd.'+args.parsed_pickle))
		meshd = None
	else:
		with open('meshd.'+args.parsed_pickle, 'rb') as f:
			meshd = pickle.load(f)
	if not os.path.exists('meshcl.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('meshcl.'+args.parsed_pickle))
		meshcl = None
	else:
		with open('meshcl.'+args.parsed_pickle, 'rb') as f:
			meshcl = pickle.load(f)
	if not os.path.exists('meshpp.'+args.parsed_pickle):
		print('WARNING !!! Required pickled data file %s not found.' % ('meshpp.'+args.parsed_pickle))
		meshpp = None
	else:
		with open('meshpp.'+args.parsed_pickle, 'rb') as f:
			meshpp = pickle.load(f)

if args.begin_phase > 2:
	# need to reload some data into parsed objects since they are needed by eqiv:
	#  - sdis_to_do     ...needs... sdis
	#  - schem_to_chebi ...needs... schem
	#  - nch            ...needs... ctg
	parsed.sdis_data = sdis
	parsed.sdis_to_do_data = sdis_to_do
	parsed.schem_data = schem
	parsed.schem_to_chebi_data = schem_to_chebi
	parsed.ctg_data = ctg
	#  - swiss          ...needs... hgnc, mgi, rgd
	parsed.hgnc_data = hg
	parsed.mgi_data = mg
	parsed.rgd_data = rg
	#  - mesh           ...needs... do
	parsed.do_data = do
	#  - affy           ...needs... g2
	parsed.gene2acc_data = g2

equiv_data = [ei, hg, mg, rg, sp, af, chebi, gobp, gocc, do, meshd, meshcl, meshpp, sdis,
               schem, nch]
for d in equiv_data:
	if d:
		if verbose:
			print('Generating equivalence file for ' +str(d))
		equiv.equiv(d, verbose)

print('Phase V ran in %.3f minutes' % ((time.time() - interval_time) / 60))

print('\n======= Phase VI, finished! =======')
print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))
