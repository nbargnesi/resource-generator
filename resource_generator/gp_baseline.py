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
from configuration import path_constants, gp_datasets, gp_reference_info, gp_reference_history
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
from equivalence_dictionaries import EGID_to_HGNC, EGID_to_MGI, EGID_to_SP, EGID_eq

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

for path, url in gp_reference_info.file_to_url.items():
    download(url, path)
parser = gp_reference_info.parser_class(gp_reference_info.file_to_url)
print("Running " + str(parser))

#####   Temporary Block   #####
equiv_dict = {}
entrez_dict = {}
#hgnc_dict = {}
#mgi_dict = {}
#sp_dict = {}

#Build equivalence dictionary. This maps Entrez id# to its HGNC, MGD, and SP types OR NONE if there is none.
for k in EGID_eq.keys():
    equiv_dict[k] = {
        "hgnc_eq" : 'NONE' if (k not in EGID_to_HGNC) else EGID_to_HGNC.get(k), 
        "mgi_eq" :  'NONE' if (k not in EGID_to_MGI) else EGID_to_MGI.get(k),
        "sp_eq" :   'NONE' if (k not in EGID_to_SP) else EGID_to_SP.get(k) }


gene_info_dict = parser.parse()
with open('entrez_info.txt', 'w') as f:
    for x in gene_info_dict:
        entrez_dict[x.get('GeneID')] = {
                'Full_name_from_nomenclature_authority' : x.get('Full_name_from_nomenclature_authority'),
                'Other_designations' : x.get('Other_designations').split('|'),
                'Synonyms' : x.get('Synonyms').split('|') }
        json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

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
# print ("before datasets")
for d in gp_datasets:
    for path, url in d.file_to_url.items():
        download(url, path)
        parser = d.parser_class(d.file_to_url)
        print ("Running " + str(parser))
        with open(str(parser) +'.txt', 'w') as f:
            for x in parser.parse():
                hgnc_dict = {}
                mgi_dict = {}
                sp_dict = {}

                # build a dict for the hgnc dataset, where the keys will be the 'Approved Symbol'
                if (str(parser)) == 'HGNC_Parser':
                    # print ('Synomyms: ' +str(x.get('Synonyms')))

                    test = x.get('Previous Names')
                    if test is not None:
                        new = test.split('", ')
                        for n in new:
                            #print('before split: ' +n)
                            #print('type is: ' +str(type(n)))
                            t = n.split(', \"')
                            #print('after split: ' +n)
                            test = t

                    hgnc_dict[x.get('Approved Symbol')] = {
                        'Previous Names' : new,
                        'Previous Symbols' : x.get('Previous Symbols'),
                        'Name Synonyms' : x.get('Name Synonyms'),
                        'Synonyms' : x.get('Synonyms') }

                # Build a dict for the mgi dataset, where the keys will be the 'Marker Symbol'
                if (str(parser)) == 'MGI_Parser':
                    mgi_dict[x.get('Marker Symbol')] = {
                        'Marker Synonyms' : x.get('Marker Synonyms') }

                # build a dict for the swissprot data set, where the keys will be the 'name'
                if (str(parser)) == 'SwissProt_Parser':
                    sp_dict[x.get('name')] = {
                        'recommendedFullName' : x.get('recommendedFullName'),
                        'recommendedShortName' : x.get('recommendedShortName'),
                        'alternativeFullNames' : x.get('alternativeFullNames'),
                        'althernativeShortNames' : x.get('alternativeShortNames') }

                json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

print('Completed gene protein resource generation.')
print('Gathering data for merging ... ')

for k in filter(lambda x: x is not None, entrez_dict.keys()):
    # append new values to the dict returned by entrez(k) and replace with new dict
    #print("Length of entrez keys: %d" %(len(entrez_dict)))
    #print ("K is : " +str(k))

    if k is not None and k is not 'NONE':

        var = equiv_dict.get(k)
        if (var is not None):
            hgnc_name = var.get('hgnc_eq')
            mgi_name = var.get('mgi_eq')
            sp_name = var.get('sp_eq')
            # print ('SP name: ' +sp_name)
            new_dict = entrez_dict.get(k)

            # could be 'NONE' if there is no equivalent from Entrez to that particular dataset
            if hgnc_name is not 'NONE' and hgnc_name is not None :
                new_dict['HGNC_approved_symbol'] = hgnc_name
                # print ('Synomyms: ' +str(var.get('Synonyms')))
                # some records may be None, if they are skip over them.
                var = hgnc_dict.get(hgnc_name)
                if (var is not None):
                    new_dict['HGNC_previous_names'] = var.get('Previous Names')
                    new_dict['HGNC_previous_symbols'] = var.get('Previous Symbols')
                    new_dict['HGNC_name_synonyms'] = var.get('Name Synonyms')
                    new_dict['HGNC_synonyms'] = var.get('Synonyms')
    
            if mgi_name is not 'NONE' and mgi_name is not None:
                new_dict['MGI_marker_symbol'] = mgi_name

                var = mgi_dict.get(mgi_name)
                if (var is not None):
                    new_dict['MGI_marker_synonyms'] = var.get('Marker Synonyms')
            
            if sp_name is not 'NONE' and sp_name is not None:
                new_dict['SP_name'] = sp_name
                
                var = sp_dict.get(sp_name)
                if (var is not None):
                    new_dict['SP_recommendedFullName'] = var.get('recommendedFullName')
                    new_dict['SP_recommendedShortName'] = var.get('recommendedShortName')
                    new_dict['SP_alternativeFullNames'] = var.get('alternativeFullNames')
                    new_dict['SP_alternativeShortNames'] = var.get('alternativeShortNames')

            entrez_dict[k] = new_dict

print ('Merging the datasets ... ')
some_dict = {}
for k in filter(lambda x: x is not None, entrez_dict.keys()):
    
    index = entrez_dict.get(k)
    if (index is not None):
        # name synonyms
        name_syn = []
        # synonyms
        syns = [] 
        # describing symbol (NONE by default, possibly replaced by new value)
        symbol = 'NONE'

        if ('HGNC_approved_symbol' in index.keys()):
            s = index.get('HGNC_approved_symbol') 
            symbol = s if (s is not None) else 'None'
        if ('MGI_marker_symbol' in index.keys()):
            s = index.get('MGI_marker_symbol')
            symbol = s if (s is not None) else 'None'

        if ('Other_designations' in index.keys()):
            n = index.get('Other_designations')
            if n is not None:
                name_syn.extend(n)
        if ('HGNC_previous_names' in index.keys()):
            n = index.get('HGNC_previous_names')
            if n is not None:
                #if k == 100009613:
                 #   print('Here is previous nameooooooooo: ' +str(n))
                name_syn.extend(n)
        if ('HGNC_name_synonyms' in index.keys()):
            n = index.get('HGNC_name_synonyms')
            if n is not None:
                #n = n.split(',')
                name_syn.append(n)
        if ('SP_recommendedFullName' in index.keys()):
            n = index.get('SP_recommendedFullName')
            if n is not None:
                name_syn.append(n)
        if ('SP_alternativeFullNames' in index.keys()):
            n = index.get('SP_alternativeFullNames')
            if n is not None:
                name_syn.extend(n)

        if ('SP_recommendedShortName' in index.keys()):
            s = index.get('SP_recommendedShortName')
            if s is not None:
                syns.append(s)
        if ('SP_alternativeShortNames' in index.keys()):
            s = index.get('SP_alternativeShortNames') 
            if s is not None:
                syns.extend(s)
        if ('Synonyms' in index.keys()):
            s = index.get('Synonyms')
            if s is not None:
                #print ("here is s: ----------------" +str(s))
                syns.extend(s)
        if ('HGNC_synonyms' in index.keys()):
            s = index.get('HGNC_synonyms')
            if s is not None:
                #print ("here is HGNC_synonyms: ----------------  " +str(s))
                syns.append(s)
        if ('HGNC_previous_symbols' in index.keys()):
            s = index.get('HGNC_previous_symbols')
            if s is not None:
                #print ("here is HGNC_previous_symbols: ----------------  " +str(s))
                syns.append(s)
        if ('MGI_marker_synonyms' in index.keys()):
            s = index.get('MGI_marker_synonyms')
            if s is not None:
                #print ("here is MGI_marker_synonyms: ----------------" +str(s))
                syns.append(s)

        some_dict[k] = {
            'SwissProtName' : index.get('SP_name'),
            'Name' : index.get('Full_name_from_nomenclature_authority'),
            'Symbol' : symbol,
            'Name Synonyms' : name_syn,
            'Synonyms' : syns }

        # print ("Successfull Iteration.")
                                          
with open('new.txt', 'w') as fp:
    json.dump(some_dict, fp, sort_keys=True, indent=4, separators=(',', ':'))

#print("Number of namespace entries: %d" %(len(gp_dict)))

with open("equivalence.dict", "wb") as df:
    pickle.dump(gp_dict, df)

with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
