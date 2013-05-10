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

gene_info_dict = parser.parse()
with open('entrez_info.txt', 'w') as f:
    for x in gene_info_dict:
        if x.get("Synonyms") is not None:
            if 'E_synonyms' in gp_dict:
                gp_dict["E_synonyms"].append(x.get("Synonyms"))
            else:
                gp_dict['E_synonyms'] = [x.get('Synonyms')]
        if x.get("Other_designations") is not None:
            if 'E_other_designations' in gp_dict:
                gp_dict["E_other_designations"].append(x.get("Other_designations"))
            else:
                gp_dict['E_other_designations'] = [x.get('Other_designations')]
        if x.get("Full_name_from_nomenclature_authority") is not None:
            if 'E_full_name_from_nomenclature_authority' in gp_dict:
                gp_dict["E_full_name_from_nomenclature_authority"].append(x.get("Full_name_from_nomenclature_authority"))
            else:
                gp_dict['E_full_name_from_nomenclature_authority'] = [x.get('Full_name_from_nomenclature_authority')]
        if x.get("GeneID") is not None:
            if 'GendeID' in gp_dict:
                gp_dict["E_gene_id"].append(x.get("GeneID"))
            else:
                gp_dict['GeneID'] = [x.get('GeneID')]
        json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

# parse reference dataset HISTORY (entrez gene)
for path, url in gp_reference_history.file_to_url.items():
    download(url, path)
parser = gp_reference_history.parser_class(gp_reference_history.file_to_url)
print("Running " + str(parser))

gene_history_dict = parser.parse()
with open('entrez_history.txt', 'w') as f:
    #print ('-------DEBUG-----' + str(type(gene_history_dict)))
    for x in gene_history_dict:
    #    print ('-------DEBUG-----' + str(type(x)))
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
                if str(parser) == "HGNC_Parser":
                    if x.get("Synonyms") is not None:
                        if 'H_synonyms' in gp_dict:
                            gp_dict["H_synonyms"].append(x.get('Synonyms'))
                        else:
                            gp_dict["H_synonyms"] = [x.get('Synonyms')]
                    if x.get("Approved Symbol") is not None:
                        if 'H_approved_symbol' in gp_dict:
                            gp_dict["H_approved_symbol"].append(x.get("Approved Symbol"))
                        else:
                            gp_dict['H_approved_symbol'] = [x.get("Approved Symbol")]
                    if x.get("Previous Names") is not None:
                        if 'H_previous_names' in gp_dict:
                            gp_dict["H_previous_names"].append(x.get("Previous Names"))
                        else:
                            gp_dict['H_previous_names'] = [x.get("Previous Names")]
                    if x.get("Previous Symbols") is not None:
                        if 'H_previous_symbols' in gp_dict:
                            gp_dict["H_previous_symbols"].append(x.get("Previous Symbols"))
                        else:
                            gp_dict['H_previous_symbols'] = [x.get("Previous Symbols")]
                    if x.get("Name Synonyms") is not None:
                        if 'H_name_synonyms' in gp_dict:
                            gp_dict["H_name_synonyms"].append(x.get("Name Synonyms"))
                        else:
                            gp_dict['H_name_synonyms'] = [x.get("Name Synonyms")]
                if str(parser) == "MGI_Parser":
                    if x.get("Marker Synonyms (pipe-separated)") is not None:
                        if 'M_synonyms' in gp_dict:
                            gp_dict["M_synonyms"].append(x.get("Marker Synonyms (pipe-separated)"))
                        else:
                            gp_dict['M_synonyms'] = [x.get('Marker Synonyms (pipe-separated)')]
                    if x.get("Marker Symbol") is not None:
                        if 'M_marker_symbol' in gp_dict:
                            gp_dict["M_marker_symbol"].append(x.get("Marker Symbol"))
                        else:
                            gp_dict['M_marker_symbol'] = [x.get('Marker Symbol')]
                if str(parser) == 'SwissProt_Parser':
                    if x.get('name') is not None:
                        if 's_name' in gp_dict:
                            gp_dict['s_name'].append(x.get('name'))
                        else:
                            gp_dict['s_name'] = [x.get('name')]
                    if x.get('recommendedFullName') is not None:
                        if 's_recommendedFullName' in gp_dict:
                            gp_dict['s_recommendedFullName'].append(x.get('recommendedFullName'))
                        else:
                            gp_dict['s_recommendedFullName'] = [x.get('recommendedFullName')]
                    if x.get('recommendedShortName') is not None:
                        if 's_recommendedShortName' in gp_dict:
                            gp_dict['s_recommendedShortName'].append(x.get('recommendedShortName'))
                        else:
                            gp_dict['s_recommendedShortName'] = [x.get('recommendedShortname')]
                    if x.get('alternativeFullNames') is not None:
                        if 's_alternativeFullNames' in gp_dict:
                            gp_dict['s_alternativeFullNames'].append(x.get('alternativeFullNames'))
                        else:
                            gp_dict['s_alternativeFullNames'] = [x.get('alternativeFullNames')]
                    if x.get('alternativeShortNames') is not None:
                        if 's_alternativeShortNames' in gp_dict:
                            gp_dict['s_alternativeShortNames'].append(x.get('alternativeShortNames'))
                        else:
                            gp_dict['s_alternativeFullNames'] = [x.get('alternativeFullNames')]
                json.dump(x, f, sort_keys=True, indent=4, separators=(',', ':'))

print("Completed gene protein resource generation.")

with open('equiv.txt', 'w') as fp:
    json.dump(gp_dict, fp, sort_keys=True, indent=4, separators=(',', ':'))
        
#print("Number of namespace entries: %d" %(len(gp_dict)))

with open("equivalence.dict", "wb") as df:
    pickle.dump(gp_dict, df)

with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
