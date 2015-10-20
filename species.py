#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import pickle

'''
Load specified pickled data object (produced by gp_baseline) and
Get all non-obsolete terms for the specified tax_id.

    -n directory where the pickle files are
    -d data set prefix (e.g., 'egid')
    -t tax id; default = '9606' (human)
'''

parser = argparse.ArgumentParser(description="""Get species info from data object.""")

parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
                    help="directory where data is stored")
parser.add_argument("-d", required=True, type=str,
                    help="dataset name")
parser.add_argument(
    "-t",
    default='9606',
    choices=[
        '9606',
        '10090',
        '10116'],
    help="species by taxid")
args = parser.parse_args()

dataset = args.d
tax_id = args.t

if os.path.exists(args.n[0]):
    os.chdir(args.n[0])
else:
    print('data directory {0} not found!'.format(args.n[0]))

if not os.path.exists(dataset + '.parsed_data.pickle'):
    print(
        'WARNING !!! Required pickled data file %s not found.' %
        (dataset + '.parsed_data.pickle'))
else:
    with open(dataset + '.parsed_data.pickle', 'rb') as f:
        data = pickle.load(f)

for term_id in data.get_values():
    if data.get_species(term_id) == tax_id:
        print(term_id)
