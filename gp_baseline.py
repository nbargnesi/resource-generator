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
import argparse
import os
import parsed
import pickle
import time
import shutil
import equiv
from common import download
from datasets import NamespaceDataSet, DataSet
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
# using os.getcwd() for value of [cwd]
# - if gp_baseline is not launched from its source directory, the import fails
os.chdir(src_dir)
# assure full path is saved
src_dir = os.getcwd()

os.chdir(cwd)

parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-v", "--verbose", required=False, action="store_true",
                    help="enable verbose program output")
parser.add_argument(
    "-n",
    required=True,
    nargs=1,
    metavar="DIRECTORY",
    help="directory to store the new namespace equivalence data")
parser.add_argument(
    "-b",
    "--begin_phase",
    type=int,
    choices=[
        1,
        2,
        3,
        4,
        5],
    default=1,
    help="resource-generator phase to begin at")
parser.add_argument(
    "-e",
    "--end_phase",
    type=int,
    choices=[
        1,
        2,
        3,
        4,
        5],
    default=5,
    help="resource-generator phase to end at")
parser.add_argument(
    "-p",
    "--parsed_pickle",
    type=str,
    default='parsed_data.pickle',
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
dep_files.append('selventa-legacy-diseases.txt')
dep_files.append('selventa-legacy-chemical-names.txt')
dep_files.append('selventa-protein-families.txt')
dep_files.append('selventa-named-complexes.txt')

if args.begin_phase <= 1:
    for df in dep_files:
        if not os.path.exists(src_dir + '/datasets/' + df):
            print(
                'WARNING !!! Dependency file %s not found in %s/datasets/' %
                (df, src_dir))
        else:
            shutil.copy(src_dir + '/datasets/' + df, os.getcwd() + '/datasets')
            if verbose:
                print(
                    'Copying dependency file %s to %s/datasets/' %
                    (df, os.getcwd()))

# make templates directory
if not os.path.exists('templates'):
    os.mkdir('templates')
    if verbose:
        print('Created templates directory')
for df in os.listdir(src_dir + '/templates'):
    shutil.copy(src_dir + '/templates/' + df, os.getcwd() + '/templates')
    if verbose:
        print('Copying template file %s to %s/templates/' % (df, os.getcwd()))

cwd = os.getcwd()

start_time = time.time()

if args.begin_phase <= 1:
    print('\n======= Phase I, downloading data =======')
    for name, url_tuple in baseline_data.items():
        if verbose:
            print('Downloading ' + str(name))
            sys.stdout.flush()
        path = os.path.join('datasets/', name)
        # if url_tuple[RES_LOCATION].startswith('http') or \
        # url_tuple[RES_LOCATION].startswith('ftp'):
        loc = url_tuple[RES_LOCATION]
        if any([loc.startswith(x) for x in ['file', 'ftp', 'http']]):
            download(url_tuple[RES_LOCATION], path)
            print(loc)
    print('Phase 1 ran in %.3f minutes' % ((time.time() - start_time) / 60))

    if args.end_phase == 1:
        print('\nTerminating process after phase 1 as specified by user.')
        print(
            'Total runtime: %.3f minutes' %
            ((time.time() - start_time) / 60))
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
    # object_dict is dictionary with keys = prefix + '_data' and value = data object
    # use object_dict to access data objects by name
    object_dict = {}
    for root, dirs, filenames in os.walk(working_dir):
        for fn in filenames:
            if fn in baseline_data:
                try:
                    data_tuple = baseline_data.get(fn)
                    data_object = data_tuple[2]
                    parser = data_tuple[PARSER_TYPE]('datasets/' + fn)
                    if verbose:
                        parser.is_verbose()
                        print(
                            'Running {0} on file {1}'.format(
                                str(parser), fn))
                except:
                    print(
                        'WARNING - skipping {0}; file not properly configured'.format(fn))
                    continue
                for x in parser.parse():
                    parsed.build_data(x, str(parser), data_object)
                # if data_tuple[2] is a list of objects, handle list
                if isinstance(data_object, list):
                    for o in data_object:
                        o.source_file = fn
                        with open(str(o) + '.' + args.parsed_pickle, 'wb') as f:
                            pickle.dump(o, f, pickle.HIGHEST_PROTOCOL)
                        object_dict[str(o) + '_data'] = o
                    continue
                # if data_tuple[2] is a single object
                elif isinstance(data_object, DataSet):
                    data_object.source_file = fn
                    with open(str(data_object) + '.' + args.parsed_pickle, 'wb') as f:
                        pickle.dump(data_object, f, pickle.HIGHEST_PROTOCOL)
                    object_dict[str(data_object) + '_data'] = data_object

    print('Phase II ran in %.3f minutes' %
          ((time.time() - interval_time) / 60))

    if args.end_phase == 2:
        print('\nTerminating process after phase 2 as specified by user.')
        print(
            'Total runtime: %.3f minutes' %
            ((time.time() - start_time) / 60))
        sys.exit()
else:
    print('\nSkipping phase 2.')

sys.stdout.flush()

# if beginning after parsing phase (phase 2), load pickled objects and
# store in object_dict
if args.begin_phase >= 3:
    object_dict = {}
    for file_name in os.listdir("."):
        if file_name.endswith("parsed_data.pickle"):
            with open(file_name, 'rb') as f:
                d = pickle.load(f)
                file_name = file_name.replace(
                    ".parsed_data.pickle", "") + '_data'
            if isinstance(d, DataSet):
                object_dict[file_name] = d
                if verbose:
                    print('Loading {0} from pickle file'.format(str(d)))

if args.begin_phase <= 3:
    print('\n======= Phase III, building namespaces =======')
    interval_time = time.time()

    for dataset in object_dict.values():
        if not isinstance(dataset, NamespaceDataSet):
            continue
        if 'ns' not in dataset.scheme_type:
            continue  # skip annotation 'anno' data sets
        if verbose:
            print('Generating namespace file for ' + str(dataset))
        try:
            dataset.write_ns_values(cwd)
        except:
            print("Unexpected error:", sys.exc_info()[1])

    print('Phase III ran in %.3f minutes' %
          ((time.time() - interval_time) / 60))

    if args.end_phase == 3:
        print('\nTerminating process after phase 3 as specified by user.')
        print(
            'Total runtime: %.3f minutes' %
            ((time.time() - start_time) / 60))
        sys.exit()
else:
    print('\nSkipping phase 3.')

sys.stdout.flush()

if args.begin_phase <= 4:
    print('\n======= Phase IV, building annotations =======')
    interval_time = time.time()

    # NOTE - Phase Iv not implemented!

    print('Phase IV ran in %.3f minutes' %
          ((time.time() - interval_time) / 60))

    if args.end_phase == 4:
        print('\nTerminating process after phase 4 as specified by user.')
        print(
            'Total runtime: %.3f minutes' %
            ((time.time() - start_time) / 60))
        sys.exit()
else:
    print('\nSkipping phase 4.')

sys.stdout.flush()

print('\n======= Phase V, building equivalences =======')
# Any datasets producing a .beleq file should be added to equiv_data
interval_time = time.time()

if args.begin_phase > 2:
    # need to reload some data into parsed objects since they are needed by eqiv:
    #  - meshd 			...needs... do
    parsed.do_data = object_dict.get('do_data')
    #  - affy           ...needs... g2
    parsed.gene2acc_data = object_dict.get('gene2acc_data')

# equiv_root_data should include string names for each namespacedataset
# used as a 'root' for equivalence
equiv_root_data = [
    'egid_data',
    'hgnc_data',
    'mgi_data',
    'rgd_data',
    'gobp_data',
    'chebi_data',
    'gocc_data',
    'do_data',
    'meshc_data']
for data_name in equiv_root_data:
    data = object_dict.get(data_name)
    if data:
        if verbose:
            print('Generating equivalence file for ' + str(data))
        equiv.equiv(data, verbose)
# now make equivalences for namespace datasets that are not root
for data_name, data in object_dict.items():
    # skip equiv root datasets handled above
    if data_name in equiv_root_data:
        continue
    elif isinstance(data, NamespaceDataSet) and 'ns' in data.scheme_type:
        if verbose:
            print('Generating equivalence file for ' + str(data))
        equiv.equiv(data, verbose)

print('Phase V ran in %.3f minutes' % ((time.time() - interval_time) / 60))

print('\n======= Phase VI, finished! =======')
print('Total runtime: %.3f minutes' % ((time.time() - start_time) / 60))

