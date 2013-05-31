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
from configparser import ConfigParser
from configuration import path_constants, gp_datasets, gp_reference_info, \
     gp_reference_history
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
from equivalence_dictionaries import EGID_to_HGNC, EGID_to_MGI, EGID_to_SP, \
     EGID_eq

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

# Everything between the #'s should be refactored into a separate module
###############################################################################

entrez_ns_dict = {}
hgnc_ns_dict = {}
mgi_ns_dict = {}
rgd_ns_dict = {}
sp_ns_dict = {}
sp_acc_ns_dict = {}

# miscRNA should not be used here, as it will be handled in a special case.
# For completion sake it is included.
entrez_encoding = {"protein-coding" : "GRP", "miscRNA" : "GR", "ncRNA" : "GR",
                   "snoRNA" : "GR", "snRNA" : "GR", "tRNA" : "GR",
                   "scRNA" : "GR", "other" : "G", "pseudo" : "GR",
                   "unknown" : "G", "rRNA" : "GR"}

hgnc_encoding = {"gene with protein product" : "GRP", "RNA, cluster" : "GR",
                 "RNA, long non-coding" : "GR", "RNA, micro" : "GRM",
                 "RNA, ribosomal" : "GR", "RNA, small cytoplasmic" : "GR",
                 "RNA, small misc" : "GR", "RNA, small nuclear" : "GR",
                 "RNA, small nucleolar" : "GR", "RNA, transfer" : "GR",
                 "phenotype only" : "G", "RNA, pseudogene" : "GR",
                 "T cell receptor pseudogene" : "GR",
                 "immunoglobulin pseudogene" : "GR", "pseudogene" : "GR",
                 "T cell receptor gene" : "GRP",
                 "complex locus constituent" : "GRP",
                 "endogenous retrovirus" : "G", "fragile site" : "G",
                 "immunoglobulin gene" : "G", "protocadherin" : "G",
                 "readthrough" : "GR", "region" : "G",
                 "transposable element" : "G", "unknown" : "GRP",
                 "virus integration site" : "G", "RNA, micro" : "GRM",
                 "RNA, misc" : "GR", "RNA, Y" : "GR", "RNA, vault" : "GR",
                 }

mgi_encoding = {"gene" : "G", "protein coding gene" : "GRP",
                "non-coding RNA gene" : "GR", "rRNA gene" : "GR",
                "tRNA gene" : "GR", "snRNA gene" : "GR", "snoRNA gene" : "GR",
                "miRNA gene" : "GRM", "scRNA gene" : "GR",
                "lincRNA gene" : "GR", "RNase P RNA gene" : "GR",
                "RNase MRP RNA gene" : "GR", "telomerase RNA gene" : "GR",
                "unclassified non-coding RNA gene" : "GR",
                "heritable phenotypic marker" : "G", "gene segment" : "G",
                "unclassified gene" : "GR", "other feature types" : "G",
                "pseudogene" : "GR", "QTL" : "G", "transgene" : "G",
                "complex/cluster/region" : None, "cytogenetic marker" : None,
                "BAC/YAC end" : None, "other genome feature" : "G",
                "pseudogenic region" : "GR", "polymorphic pseudogene" : "GRP",
                "pseudogenic gene segment" : "GR", "SRP RNA gene" : "GR"}

rgd_encoding = {"gene" : "G", "miscrna" : "GR", "predicted-high" : "GRP",
                "predicted-low" : "GRP", "predicted-moderate" : "GRP",
                "protein-coding" : "GRP", "pseudo" : "GR", "snrna" : "GR",
                "trna" : "GR", "rrna" : "GR"}

def make_namespace(row, parser):

    # build the namespace values (to be refactored later)

    if str(parser) == 'EntrezGeneInfo_Parser':
        gene_id = x.get('GeneID')
        gene_type = x.get('type_of_gene')
        if gene_type == 'miscRNA':
            desc = x.get('description')
            if 'microRNA' in desc:
                entrez_ns_dict[gene_id] = 'GRM'
            else:
                entrez_ns_dict[gene_id] = 'GR'
        else:
            entrez_ns_dict[gene_id] = entrez_encoding[gene_type]

    if str(parser) == 'HGNC_Parser':
        gene_id = row.get('Approved Symbol')
        locus_type = row.get('Locus Type')
        # withdrawn genes not included in this namespace
        if locus_type is not 'withdrawn' and 'withdrawn' not in gene_id:
            hgnc_ns_dict[gene_id] = hgnc_encoding[locus_type]

    if str(parser) == 'MGI_Parser':
        feature_type = row.get('Feature Type')
        symbol = row.get('Marker Symbol')
        flag = row.get('Marker Type')
        if flag == 'Gene' or flag == 'Pseudogene':
            mgi_ns_dict[symbol] = mgi_encoding[feature_type]

    # withdrawn genes are NOT included in this namespace
    if str(parser) == 'RGD_Parser':
        g_type = row.get('GENE_TYPE')
        name = row.get('NAME')
        symbol = row.get('SYMBOL')
        if g_type == 'miscrna' and 'microRNA' in name:
            rgd_ns_dict[symbol] = 'GRM'
        elif g_type == 'miscrna' and 'microRNA' not in name:
            rgd_ns_dict[symbol] = 'GR'
        else:
            if g_type is not '':
                rgd_ns_dict[symbol] = rgd_encoding[g_type]

    if str(parser) == 'SwissProt_Parser':
        sp_ns_dict[row.get('name')] = 'GRP'
        accessions = row.get('accessions')
        for acc in accessions:
            sp_acc_ns_dict[acc] = 'GRM'

###############################################################################

entrez_dict = {}
gene_info_dict = parser.parse()
with open('entrez_info.txt', 'w') as f:
    for x in gene_info_dict:
        make_namespace(x, parser)
        entrez_dict[x.get('GeneID')] = {
                'Full_name_from_nomenclature_authority' :
                    x.get('Full_name_from_nomenclature_authority'),
                'Other_designations' : x.get('Other_designations').split('|'),
                'Synonyms' : x.get('Synonyms').split('|') }
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
    for path, url in d.file_to_url.items():
        download(url, path)
        parser = d.parser_class(d.file_to_url)
        print ("Running " + str(parser))
        with open(str(parser) +'.txt', 'w') as f:
            for x in parser.parse():
                hgnc_dict = {}
                mgi_dict = {}
                sp_dict = {}

                # build a dict for the HGNC dataset, where the keys will be the
                # 'Approved Symbol'
                if (str(parser)) == 'HGNC_Parser':
                    #print('within HGNC..' +str(x))
                    test = x.get('Previous Names')
                    if test is not None:
                        new = test.split('", ')
                        for n in new:
                            t = n.split(', \"')
                            test = t

                    hgnc_dict[x.get('Approved Symbol')] = {
                        'Previous Names' : new,
                        'Previous Symbols' : x.get('Previous Symbols'),
                        'Name Synonyms' : x.get('Name Synonyms'),
                        'Synonyms' : x.get('Synonyms') }

                # build a dict for the MGI dataset, where the keys will be the
                # 'Marker Symbol'
                if (str(parser)) == 'MGI_Parser':
                    mgi_dict[x.get('Marker Symbol')] = {
                        'Marker Synonyms' : x.get('Marker Synonyms') }

                # build a dict for the SwissProt data set, where the keys will
                # be the 'name'
                if (str(parser)) == 'SwissProt_Parser':
                    sp_dict[x.get('name')] = {
                        'recommendedFullName' : x.get('recommendedFullName'),
                        'recommendedShortName' : x.get('recommendedShortName'),
                        'alternativeFullNames' : x.get('alternativeFullNames'),
                        'althernativeShortNames' :
                            x.get('alternativeShortNames') }

                # put together the namespace file for each dataset
                make_namespace(x, parser)

                # dump each dataset to a pickle file
                pickle.dump(x, f)

# build equivalencies, starting with Entrez. Assign UUID to each unique gene.
entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}

entrez = pickle.load('EntrezGeneInfo_Parser')
hgnc = pickle.load('HGNC_Parser')
mgi = pickle.load('MGI_Parser')
rgd = pickle.load('RGD_Parser')
sp = pickle.load('SwissProt_Parser')

# entrez is the root, so just generate a UUID for each entry.
for k, v in entrez:
    entrez_symbol = k.get('GeneID')
    # this symbol could be HGNC, MGI, or RGD. Will need to check tax_id.
    varity_symbol = k.get('Symbol_from_nomenclature_authority')
    entrez_eq[symbol] = uuid.uuid4()

# use symbol (AKT1), and tax_id column to decide which species it is
for k, v in hgnc:
    symbol = k

# write out the namespace files (maybe in another module also?)
print('Writing namespaces to file ...')

with open('entrez-namespace.belns', 'w') as fp:
    for key in sorted(entrez_ns_dict):
        fp.write('{0}|{1}\n'.format(key, entrez_ns_dict[key]))

with open('hgnc-namespace.belns', 'w') as fp:
    for key in sorted(hgnc_ns_dict):
        fp.write('{0}|{1}\n'.format(key, hgnc_ns_dict[key]))

with open('mgi-namespace.belns', 'w') as fp:
    for key in sorted(mgi_ns_dict):
        fp.write('{0}|{1}\n'.format(key, mgi_ns_dict[key]))

with open('rgd-namespace.belns', 'w') as fp:
    for key in sorted(rgd_ns_dict):
        fp.write('{0}|{1}\n'.format(key, rgd_ns_dict[key]))

with open('swissprot-namespace.belns', 'w') as fp:
    for key in sorted(sp_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_ns_dict[key]))

with open('swissprot-accessions-namespace.belns', 'w') as fp:
    for key in sorted(sp_acc_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_acc_ns_dict[key]))

print('Completed gene protein resource generation.')

with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
