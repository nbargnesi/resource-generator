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
import uuid
import pdb
from collections import defaultdict
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

# build equivalencies, starting with Entrez. Assign UUID to each unique gene.
entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}

hgnc_list = []
mgi_list = []
rgd_list = []

hgnc_map = {}
rgd_map = {}
mgi_map = {}

mgi_known_list = []
rgd_known_list = []

def to_entrez(gene_id):
    converted_id = entrez_eq_dict.get(gene_id)
    return converted_id

# gene_id = 'AKT1' data_type = 'hgnc'
def equiv(gene_id, data_type):
    if data_type is 'entrez':
        entrez_eq[gene_id] = uuid.uuid4()
    if data_type is 'hgnc':
        new_id = to_entrez('HGNC:'+gene_id)
        if new_id is None:
            # keep track of which hgnc genes need new uuids (dont map to entrez)
            #hgnc_count = hgnc_count + 1
            hgnc_list.append(gene_id)
            # generate new uuid
            hgnc_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            hgnc_eq[gene_id] = entrez_eq.get(new_id)
    if data_type is 'mgi':
        new_id = to_entrez('MGI:'+gene_id)
        if new_id is None:
            # keep track of which genes need new uuids (dont map to entrez)
            mgi_list.append(gene_id)
            # generate new uuid
            mgi_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            mgi_eq[gene_id] = entrez_eq.get(new_id)
    if data_type is 'rgd':
        new_id = to_entrez('RGD:'+gene_id)
        if new_id is None:
            # keep track of which genes need new uuids (dont map to entrez)
            rgd_list.append(gene_id)
            # generate new uuid
            rgd_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            rgd_eq[gene_id] = entrez_eq.get(new_id)

sp_eq = {}
sp_list = []
target_pool = ['HGNC', 'MGI', 'RGD']
def build_sp_eq(row):

    # dbrefs is a dict, i.e { reference_type : id_of_that_gene}
    dbrefs = row.get('dbReference')
    gene_ids = []
    alt_ids = []

#    if row.get('name') == 'IL7_RAT':
#        print('DBREFS for ' +row.get('name')+ ' ' +str(dbrefs))
    for k, v in dbrefs.items():
        if k == 'GeneId':
            gene_ids.extend(v)
        if k in target_pool:
            # could be MGI or RGD or HGNC ids
            alt_ids.extend(v)
    # new ID if more than 1 entrez reference
    if len(gene_ids) == 1:
        sp_eq[row.get('name')] = entrez_eq.get(gene_ids[0])
    elif len(gene_ids) == 0:
        # are there hgnc, mgi or rgd refs?
        if len(alt_ids) == 0:
            sp_eq[row.get('name')] = uuid.uuid4()
            sp_list.append(row.get('name'))
        elif len(alt_ids) == 1:
            a_id = alt_ids[0]
            if 'HGNC' in a_id:
                hgnc_key = hgnc_map.get(a_id)
                sp_eq[row.get('name')] = hgnc_eq.get(hgnc_key)
            elif 'MGI' in a_id:
                mgi_key = mgi_map.get(a_id)
                sp_eq[row.get('name')] = mgi_eq.get(mgi_key)
            else:
                rgd_key = rgd_map.get(a_id)
                sp_eq[row.get('name')] = rgd_eq.get(rgd_key)
        # more than one alt_id then generate a new uuid
        else:
            sp_eq[row.get('name')] = uuid.uuid4()
    # more than one Entrez id than generate a new uuid
    else:
        sp_eq[row.get('name')] = uuid.uuid4()


# Everything between the #'s should be refactored into a separate module
###############################################################################

entrez_ns_dict = {}
hgnc_ns_dict = {}
mgi_ns_dict = {}
rgd_ns_dict = {}
sp_ns_dict = {}
sp_acc_ns_dict = {}
affy_ns_dict = {}

# miscRNA should not be used here, as it will be handled in a special case.
# For completion sake it is included.
entrez_encoding = {"protein-coding" : "GRP", "miscRNA" : "GR", "ncRNA" : "GR",
                   "snoRNA" : "GR", "snRNA" : "GR", "tRNA" : "GR",
                   "scRNA" : "GR", "other" : "G", "pseudo" : "GR",
                   "unknown" : "GRP", "rRNA" : "GR"}

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
                 "immunoglobulin gene" : "GRP", "protocadherin" : "GRP",
                 "readthrough" : "GR", "region" : "G",
                 "transposable element" : "G", "unknown" : "GRP",
                 "virus integration site" : "G", "RNA, micro" : "GRM",
                 "RNA, misc" : "GR", "RNA, Y" : "GR", "RNA, vault" : "GR",
                 }

mgi_encoding = {"gene" : "GRP", "protein coding gene" : "GRP",
                "non-coding RNA gene" : "GR", "rRNA gene" : "GR",
                "tRNA gene" : "GR", "snRNA gene" : "GR", "snoRNA gene" : "GR",
                "miRNA gene" : "GRM", "scRNA gene" : "GR",
                "lincRNA gene" : "GR", "RNase P RNA gene" : "GR",
                "RNase MRP RNA gene" : "GR", "telomerase RNA gene" : "GR",
                "unclassified non-coding RNA gene" : "GR",
                "heritable phenotypic marker" : "G", "gene segment" : "G",
                "unclassified gene" : "GRP", "other feature types" : "G",
                "pseudogene" : "GR", "transgene" : "G",
                "other genome feature" : "G", "pseudogenic region" : "GR",
                "polymorphic pseudogene" : "GRP",
                "pseudogenic gene segment" : "GR", "SRP RNA gene" : "GR"}

rgd_encoding = {"gene" : "GRP", "miscrna" : "GR", "predicted-high" : "GRP",
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
        hgnc_map[row.get('HGNC ID')] = row.get('Approved Symbol')
        #pdb.set_trace()

    if str(parser) == 'MGI_Parser':
        feature_type = row.get('Feature Type')
        symbol = row.get('Marker Symbol')
        flag = row.get('Marker Type')
        if flag == 'Gene' or flag == 'Pseudogene':
            mgi_ns_dict[symbol] = mgi_encoding[feature_type]
        mgi_map[row.get('MGI Accession ID')] = row.get('Marker Symbol')

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
        if '2904' in row.get('GENE_RGD_ID'):
            print('rgd_map maps ' +row.get('GENE_RGD_ID')+ ' --> ' +row.get('SYMBOL'))
        rgd_map[row.get('GENE_RGD_ID')] = row.get('SYMBOL')
        #rgd_map[row.get('SYMBOL')] = row.get('GENE_RGD_ID')

    if str(parser) == 'SwissProt_Parser':
        sp_ns_dict[row.get('name')] = 'GRP'
        accessions = row.get('accessions')
        build_sp_eq(row)
        for acc in accessions:
            sp_acc_ns_dict[acc] = 'GRP'

    if str(parser) == 'Affy_Parser':
        probe_set_id = x.get('Probe Set ID')
        if probe_set_id not in affy_ns_dict:
            affy_ns_dict[probe_set_id] = 'R'

entrez_eq_dict = {}
def make_eq_dict(entrez_id, symbol, tax_id):
    if tax_id == '9606':
        entrez_eq_dict['HGNC:'+symbol] = entrez_id
    if tax_id == '10116':
        entrez_eq_dict['RGD:'+symbol] = entrez_id
    if tax_id == '10090':
        entrez_eq_dict['MGI:'+symbol] = entrez_id

entrez_dict = {}
entrez_info_dict = parser.parse()
with open('entrez_info.txt', 'wb') as f:
    for x in entrez_info_dict:
        make_namespace(x, parser)
        equiv(x.get('GeneID'), 'entrez')
        entrez_dict[x.get('GeneID')] = {
                'Full_name_from_nomenclature_authority' :
                    x.get('Full_name_from_nomenclature_authority'),
                'Other_designations' : x.get('Other_designations').split('|'),
                'Synonyms' : x.get('Synonyms').split('|') }
        make_eq_dict(x.get('GeneID'),
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
    for path, url in d.file_to_url.items():
        download(url, path)
        parser = d.parser_class(d.file_to_url)
        print ("Running " + str(parser))
        spaces = ['HGNC_Parser', 'MGI_Parser', 'RGD_Parser', 'SwissProt_Parser']
        if str(parser) not in spaces:
            break
        for x in parser.parse():
            # put together the namespace file for each dataset
            make_namespace(x, parser)

print('Writing namespaces to file ...')

with open('entrez-namespace.belns', 'w') as fp:
    for key in sorted(entrez_ns_dict):
        #equiv(key, 'entrez')
        fp.write('{0}|{1}\n'.format(key, entrez_ns_dict[key]))

with open('hgnc-namespace.belns', 'w') as fp:
    for key in sorted(hgnc_ns_dict):
        equiv(key, 'hgnc')
        fp.write('{0}|{1}\n'.format(key, hgnc_ns_dict[key]))

with open('mgi-namespace.belns', 'w') as fp:
    for key in sorted(mgi_ns_dict):
        equiv(key, 'mgi')
        fp.write('{0}|{1}\n'.format(key, mgi_ns_dict[key]))

with open('rgd-namespace.belns', 'w') as fp:
    for key in sorted(rgd_ns_dict):
        equiv(key, 'rgd')
        fp.write('{0}|{1}\n'.format(key, rgd_ns_dict[key]))

with open('swissprot-namespace.belns', 'w') as fp:
    for key in sorted(sp_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_ns_dict[key]))

with open('swissprot-accessions-namespace.belns', 'w') as fp:
    for key in sorted(sp_acc_ns_dict):
        fp.write('{0}|{1}\n'.format(key, sp_acc_ns_dict[key]))

with open('affy-namespace.belns', 'w') as fp:
    for key in sorted(affy_ns_dict):
        fp.write('{0}|{1}\n'.format(key, affy_ns_dict[key]))

print('Writing uuids ... ')

with open('entrez-uuids.txt', 'w') as fp:
    for key in sorted(entrez_eq):
        fp.write('{0}|{1}\n'.format(key, entrez_eq[key]))

with open('hgnc-uuids.txt', 'w') as fp:
    for key in sorted(hgnc_eq):
        fp.write('{0}|{1}\n'.format(key, hgnc_eq[key]))

with open('rgd-uuids.txt', 'w') as fp:
    for key in sorted(rgd_eq):
        fp.write('{0}|{1}\n'.format(key, rgd_eq[key]))

with open('mgi-uuids.txt', 'w') as fp:
    for key in sorted(mgi_eq):
        fp.write('{0}|{1}\n'.format(key, mgi_eq[key]))

with open('sp-uuids.txt', 'w') as fp:
    for key in sorted(sp_eq):
        fp.write('{0}|{1}\n'.format(key, sp_eq[key]))

with open('new-hgnc.txt', 'w') as fp:
    for val in hgnc_list:
        fp.write(val +'\n')

with open('new-mgi.txt', 'w') as fp:
    for val in mgi_list:
        fp.write(val +'\n')

with open('new-rgd.txt', 'w') as fp:
    for val in rgd_list:
        fp.write(val +'\n')

with open('new-sp.txt', 'w') as fp:
    for val in sp_list:
        fp.write(val +'\n')

print('Completed gene protein resource generation.')
print('Number of new HGNC uuids: ' +str(len(hgnc_list)))
print('Number of new MGI uuids: ' +str(len(mgi_list)))
print('Number of new RGD uuids: ' +str(len(rgd_list)))
print('Number of new SP uuids: ' +str(len(sp_list)))

with tarfile.open("datasets.tar", "w") as datasets:
    for fname in os.listdir(path_constants.dataset_dir):
        datasets.add(fname)
