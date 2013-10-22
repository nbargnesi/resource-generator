#!/usr/bin/env python3
# coding: utf-8

'''
 change_log.py

 Using a set of newly generated .belns and .beleq files, the
 change-log will determine which, if any, values have been lost
 between namespace versions. It will then parse additional data
 in an attempt to resolve those values to their new value or log
 them as being 'withdraw' completely. All of these values and
 their new mappings, as well as the values the could not be
 resolved, are the output of this module. This output is given
 in the form of a dictionary, which is meant to be consumed by
 an update script.

 inputs:
   -n    directory of the new namespace/equivalence files generated
         after running gp_baseline.py (required)
   -v    run the change-log in verbose mode (optional)

'''

import parsers
import urllib
import os
import write_log
import datetime
import pickle
import argparse
import time
from common import download
from changelog_config import changelog_data
from constants import RES_LOCATION, PARSER_TYPE

parser = argparse.ArgumentParser(description="""Generate namespace and
                               equivalence files for gene/protein datasets.""")
parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
                    help="""Directory to the newly generated .belns and .beleq files.""")
parser.add_argument("-v", action='store_true',
                    help="""Produce the change-log with extra output.""")
args = parser.parse_args()
resource_dir = args.n[0]
verbose = args.v

if verbose:
    print('\nProducing change-log in verbose mode.')

if not os.path.exists(resource_dir):
    os.mkdir(resource_dir)

# change to resource directory
os.chdir(resource_dir)

# BELNamespaceParser - parse() returns the specific url for each namespace
# currently published on resource.belframework.org
start_time = time.time()
parser = parsers.BELNamespaceParser()
print('\nRunning BELNamespace_Parser')
old_entrez = set()
old_hgnc = set()
old_mgi = set()
old_rgd = set()
old_sp_names = set()
old_sp_ids = set()
old_affy = set()
old_chebi_names = set()
old_chebi_ids = set()
old_gobp_ns_ids = set()
old_gobp_ns_names = set()
old_gocc_ns_ids = set()
old_gocc_ns_names = set()
old_mesh_bio = set()
old_mesh_cell = set()
old_mesh_disease = set()
old_schem_ns = set()
old_sdis_ns = set()
old_mesh_disease_anno = set()
old_mesh_cell_struct_anno = set()
old_mesh_anatomy_anno = set()
old_do_ns_names = set()
old_do_ns_ids = set()

old_chebi_eq_names = dict()
old_chebi_eq_ids = dict()
old_gobp_eq_ids = dict()
old_gobp_eq_names = dict()
old_gocc_eq_ids = dict()
old_gocc_eq_names = dict()
old_do_eq_names = dict()
old_do_eq_ids = dict()

# iterate over the urls to the .belns files, collecting the entries
# from the old data.
for url in parser.parse():
    debug = False
    namespaces = { 'entrez' : (False, old_entrez),
                   'hgnc' : (False, old_hgnc),
                   'mgi' : (False, old_mgi),
                   'rgd' : (False, old_rgd),
                   'swissprot-entry' : (False, old_sp_names),
                   'swissprot-accession' : (False, old_sp_ids),
                   'affy' : (False, old_affy),
                   'chebi-name' : (False, old_chebi_names),
                   'chebi-id' : (False, old_chebi_ids),
                   'go-biological-processes-acc' : (False, old_gobp_ns_ids),
                   'go-biological-processes-names' : (False, old_gobp_ns_names),
                   'go-cellular-component-terms' : (False, old_gocc_ns_names),
                   'go-cellular-component-acc' : (False, old_gocc_ns_ids),
                   'mesh-bio' : (False, old_mesh_bio),
                   'mesh-cell' : (False, old_mesh_cell),
                   'mesh-diseases' : (False, old_mesh_disease),
                   'selventa-legacy-chemical' : (False, old_schem_ns),
                   'selventa-legacy-diseases' : (False, old_sdis_ns),
                   'disease-ontology-names' : (False, old_do_ns_names),
                   'disease-ontology-ids' : (False, old_do_ns_ids)}

    open_url = urllib.request.urlopen(url)
    if '.belns' in open_url.url:
        for ns in namespaces:
            if ns in open_url.url:
                namespaces[ns] = (True, namespaces[ns][1])
    marker = False
    for u in open_url:
        if '[Values]' in str(u):
            marker = True
            continue
        if marker is False:
            continue
        # we are into namespace pairs with '|' delimiter
        t = u.decode('utf-8')
        tokenized = t.split('|')
        token = tokenized[0]
        # strip 'GO:' for compatibility with v1.0
        token = token.replace('GO:','')
        for k, v in namespaces.items():
            if v[0]:
                v[1].add(token)
# parse the old .beleq files needed for resolving lost values
parser = parsers.BELEquivalenceParser()
print('Running BELEquivalence_Parser')
for url in parser.parse():

    equivalences = {
        'go-biological-processes-acc' : (False, old_gobp_eq_ids),
        'go-biological-processes-names' : (False, old_gobp_eq_names),
        'go-cellular-component-terms' : (False, old_gocc_eq_names),
        'go-cellular-component-acc' : (False, old_gocc_eq_ids),
        'chebi-names' : (False, old_chebi_eq_names),
        'chebi-ids' : (False, old_chebi_eq_ids),
        'disease-ontology-names' : (False, old_do_eq_names),
        'disease-ontology-ids' : (False, old_do_eq_ids)}

    open_url = urllib.request.urlopen(url)
    for eq in equivalences:
        if eq in open_url.url:
            equivalences[eq] = (True, equivalences[eq][1])
    marker = False
    for u in open_url:
        if '[Values]' in str(u):
            marker = True
            continue
        if marker is False:
            continue
        # we are into namespace pairs with '|' delimiter
        t = u.decode('utf-8')
        tokenized = t.split('|')
        value = tokenized[0]
        uid = tokenized[1]
        for k, v in equivalences.items():
            if v[0]:
                # strip 'GO:' for GO namespaces to match v1.0
                value = value.replace('GO:','')
                v[1][uid] = value

# parse the old .belanno files needed for resolving lost values
parser = parsers.BELAnnotationsParser()
print('Running ' +str(parser))
for url in parser.parse():

    annotations = { 'mesh-disease' : (False, old_mesh_disease_anno),
                    'mesh-cell-structure' : (False, old_mesh_cell_struct_anno),
                    'mesh-anatomy' : (False, old_mesh_anatomy_anno) }

    open_url = urllib.request.urlopen(url)
    for anno in annotations:
        if anno in open_url.url:
            annotations[anno] = (True, annotations[anno][1])
    marker = False
    for u in open_url:
        if '[Values]' in str(u):
            marker = True
            continue
        if marker is False:
            continue
        # we are into namespace pairs with '|' delimiter
        t = u.decode('utf-8')
        tokenized = t.split('|')
        token = tokenized[0]
        for k, v in annotations.items():
            if v[0]:
                v[1].add(token)

gobp_names_to_ids = {}
gocc_names_to_ids = {}
chebi_names_to_ids = {}
do_names_to_ids = {}

# create a lookup for old ids/names. This is used to resolve lost
# values between generations of the namespace.
for uid in old_gobp_eq_ids:
    if uid in old_gobp_eq_names:
        name = old_gobp_eq_names.get(uid)
        id = old_gobp_eq_ids.get(uid)
        gobp_names_to_ids[name] = id
for uid in old_gocc_eq_ids:
    if uid in old_gocc_eq_names:
        name = old_gocc_eq_names.get(uid)
        id = old_gocc_eq_ids.get(uid)
        gocc_names_to_ids[name] = id
for uid in old_chebi_eq_ids:
    if uid in old_chebi_eq_names:
        name = old_chebi_eq_names.get(uid)
        id = old_chebi_eq_ids.get(uid)
        chebi_names_to_ids[name] = id
for uid in old_do_eq_names:
    if uid in old_do_eq_ids:
        name = old_do_eq_names.get(uid)
        id = old_do_eq_ids.get(uid)
        do_names_to_ids[name] = id

def name_to_id(name):
    if name in gobp_names_to_ids:
        return gobp_names_to_ids[name]
    elif name in gocc_names_to_ids:
        return gocc_names_to_ids[name]
    elif name in chebi_names_to_ids:
        return chebi_names_to_ids[name]
    elif name in do_names_to_ids:
        return do_names_to_ids[name]
    else:
        return None

if verbose:
    print('===========================================')
    print('len of old EGID is ' +str(len(old_entrez)))
    print('len of old HGNC is ' +str(len(old_hgnc)))
    print('len of old MGI is ' +str(len(old_mgi)))
    print('len of old RGD is ' +str(len(old_rgd)))
    print('len of old SP is ' +str(len(old_sp_names)))
    print('len of old SPAC is ' +str(len(old_sp_ids)))
    print('len of old AFFX is ' +str(len(old_affy)))
    print('len of old CHEBI is ' +str(len(old_chebi_names)))
    print('len of old CHEBIID is ' +str(len(old_chebi_ids)))
    print('len of old GOBP is ' +str(len(old_gobp_ns_names)))
    print('len of old GOBPID is ' +str(len(old_gobp_ns_ids)))
    print('len of old GOCC is ' +str(len(old_gocc_ns_names)))
    print('len of old GOCCID is ' +str(len(old_gocc_ns_ids)))
    print('len of old MESHPP is ' +str(len(old_mesh_bio)))
    print('len of old MESHCL is ' +str(len(old_mesh_cell)))
    print('len of old MESHD is ' +str(len(old_mesh_disease)))
    print('len of old SCHEM is ' +str(len(old_schem_ns)))
    print('len of old SDIS is ' +str(len(old_sdis_ns)))
    #print('len of old mesh-cell-structure-annotations is ' +str(len(old_mesh_cell_struct_anno)))
    #print('len of old mesh-diseases-annotations is ' +str(len(old_mesh_disease_anno)))
    #print('len of old mesh-anatomy-annotations is ' +str(len(old_mesh_anatomy_anno)))
    print('len of old DO is ' +str(len(old_do_ns_names)))
    print('len of old DOID is ' +str(len(old_do_ns_ids)))
    print('===========================================')

new_entrez = set()
new_hgnc = set()
new_mgi = set()
new_rgd = set()
new_sp_names = set()
new_sp_ids = set()
new_affy = set()
new_chebi_names = set()
new_chebi_ids = set()
new_gobp_ns_ids = set()
new_gobp_ns_names = set()
new_gocc_ns_ids = set()
new_gocc_ns_names = set()
new_mesh_bio = set()
new_mesh_cell = set()
new_mesh_disease = set()
new_schem_ns = set()
new_sdis_ns = set()
new_mesh_disease_anno = set()
new_mesh_cell_struct_anno = set()
new_mesh_anatomy_anno = set()
new_do_ns_names = set()
new_do_ns_ids = set()

# gather the new data for comparison (locally stored)
# should work with (or without) file headers
indir = os.getcwd()
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        if '.belns' in f:
            with open(os.path.join(root, f), 'r') as fp:
                values = set()
                for line in fp:
                    if len(str(line).split('|')) == 2 and line is not 'DelimiterString=|':
                        (value, encoding) = str(line).split('|')
                        values.add(value)
                    else:
                        continue 
                if 'entrez' in fp.name:
                    new_entrez = values
                elif 'hgnc' in fp.name:
                    new_hgnc = values
                elif 'mgi' in fp.name:
                    new_mgi = values
                elif 'rgd' in fp.name:
                    new_rgd = values
                elif 'swissprot-acc' in fp.name:
                    new_sp_ids = values
                elif 'swissprot-entry' in fp.name:
                    new_sp_names = values
                elif 'affy' in fp.name:
                    new_affy = values
                elif 'chebi-names' in fp.name:
                    new_chebi_names = values
                elif 'chebi-ids' in fp.name:
                    new_chebi_ids = values
                elif 'go-biological-processes-ids' in fp.name:
                    # note name mismatch for 1.0
                    new_gobp_ns_ids= values 
                elif 'go-biological-processes-names' in fp.name:
                    new_gobp_ns_names = values 
                elif 'go-cellular-component-ids' in fp.name:
                    # note name mismatch for 1.0
                    new_gocc_ns_ids = values 
                elif 'go-cellular-component-names' in fp.name:
                    # note name mismatch for 1.0
                    new_gocc_ns_names = values 
                elif 'mesh-bio' in fp.name:
                    new_mesh_bio= values 
                elif 'mesh-cell' in fp.name:
                    new_mesh_cell = values 
                elif 'mesh-disease' in fp.name:
                    new_mesh_disease = values
                elif 'selventa-legacy-chem' in fp.name:
                    new_schem_ns = values 
                elif 'selventa-legacy-disease' in fp.name:
                    new_sdis_ns = values 
                elif 'disease-ontology-names' in fp.name:
                    new_do_ns_names = values 
                elif 'disease-ontology-ids' in fp.name:
                    new_do_ns_ids = values 
        #elif '.belanno' in f:
            #with open(os.path.join(root, f), 'r') as fp:
                #if 'mesh-disease' in fp.name:
                    #for line in fp:
                        #tokenized = str(line).split('|')
                        #token = tokenized[0]
                        #new_mesh_disease_anno.add(token)
                #elif 'mesh-cell-structure' in fp.name:
                    #for line in fp:
                        #tokenized = str(line).split('|')
                        #token = tokenized[0]
                        #new_mesh_cell_struct_anno.add(token)
                #elif 'mesh-anatomy' in fp.name:
                    #for line in fp:
                        #tokenized = str(line).split('|')
                        #token = tokenized[0]
                        #new_mesh_anatomy_anno.add(token)


if verbose:
    print('len of new entrez is ' +str(len(new_entrez)))
    print('len of new hgnc is ' +str(len(new_hgnc)))
    print('len of new mgi is ' +str(len(new_mgi)))
    print('len of new rgd is ' +str(len(new_rgd)))
    print('len of new swissprot names is ' +str(len(new_sp_names)))
    print('len of new swissprot ids is ' +str(len(new_sp_ids)))
    print('len of new affy is ' +str(len(new_affy)))
    print('len of new chebi names is ' +str(len(new_chebi_names)))
    print('len of new chebi ids is ' +str(len(new_chebi_ids)))
    print('len of new gobp names is ' +str(len(new_gobp_ns_names)))
    print('len of new gobp ids is ' +str(len(new_gobp_ns_ids)))
    print('len of new gocc names is ' +str(len(new_gocc_ns_names)))
    print('len of new gocc ids is ' +str(len(new_gocc_ns_ids)))
    print('len of new mesh-bio is ' +str(len(new_mesh_bio)))
    print('len of new mesh-cell is ' +str(len(new_mesh_cell)))
    print('len of new mesh-diseases is ' +str(len(new_mesh_disease)))
    print('len of new selventa-legacy-chemicals is ' +str(len(new_schem_ns)))
    print('len of new selventa-legacy-diseases is ' +str(len(new_sdis_ns)))
    print('len of new mesh-diseases-anno is ' +str(len(new_mesh_disease_anno)))
    print('len of new mesh-cell is ' +str(len(new_mesh_cell_struct_anno)))
    print('len of new mesh-anatomy is ' +str(len(new_mesh_anatomy_anno)))
    print('len of new diseases-ontology-names is ' +str(len(new_do_ns_names)))
    print('len of new diseases-ontology-ids is ' +str(len(new_do_ns_ids)))

# values in the old data that are not in the new (either withdrawn or replaced)
entrez_lost = old_entrez.difference(new_entrez)
hgnc_lost = old_hgnc.difference(new_hgnc)
mgi_lost = old_mgi.difference(new_mgi)
rgd_lost = old_rgd.difference(new_rgd)
sp_lost_names = old_sp_names.difference(new_sp_names)
sp_lost_ids = old_sp_ids.difference(new_sp_ids)
affy_lost = old_affy.difference(new_affy)
chebi_lost_names = old_chebi_names.difference(new_chebi_names)
chebi_lost_ids = old_chebi_ids.difference(new_chebi_ids)
gobp_lost_ns_names = old_gobp_ns_names.difference(new_gobp_ns_names)
gocc_lost_ns_names = old_gocc_ns_names.difference(new_gocc_ns_names)
gobp_lost_ns_ids = old_gobp_ns_ids.difference(new_gobp_ns_ids)
gocc_lost_ns_ids = old_gocc_ns_ids.difference(new_gocc_ns_ids)
mesh_bio_lost = old_mesh_bio.difference(new_mesh_bio)
mesh_cell_lost = old_mesh_cell.difference(new_mesh_cell)
mesh_disease_lost = old_mesh_disease.difference(new_mesh_disease)
#mesh_disease_anno_lost = [x for x in old_mesh_disease_anno if x not in new_mesh_disease_anno]
#mesh_cell_struct_anno_lost = [x for x in old_mesh_cell_struct_anno if x not in new_mesh_cell_struct_anno]
#mesh_anatomy_anno_lost = [x for x in old_mesh_anatomy_anno if x not in new_mesh_anatomy_anno]
schem_lost = old_schem_ns.difference(new_schem_ns)
sdis_lost = old_sdis_ns.difference(new_sdis_ns)
do_lost_names = old_do_ns_names.difference(new_do_ns_names)
do_lost_ids = old_do_ns_ids.difference(new_do_ns_ids)

if verbose:
    print('===========================================')
    print('lost entrez values ' +str(len(entrez_lost)))
    print('lost hgnc values ' +str(len(hgnc_lost)))
    print('lost mgi values ' +str(len(mgi_lost)))
    print('lost rgd values ' +str(len(rgd_lost)))
    print('lost swissprot names ' +str(len(sp_lost_names)))
    print('lost swissprot ids ' +str(len(sp_lost_ids)))
    print('lost affy values ' +str(len(affy_lost)))
    print('lost chebi names ' +str(len(chebi_lost_names)))
    print('lost chebi ids ' +str(len(chebi_lost_ids)))
    print('lost gobp names ' +str(len(gobp_lost_ns_names)))
    print('lost gobp ids ' +str(len(gobp_lost_ns_ids)))
    print('lost gocc names ' +str(len(gocc_lost_ns_names)))
    print('lost gocc ids ' +str(len(gocc_lost_ns_ids)))
    print('lost mesh-bio ' +str(len(mesh_bio_lost)))
    print('lost mesh-cell ' +str(len(mesh_cell_lost)))
    print('lost mesh-diseases ' +str(len(mesh_disease_lost)))
    #print('lost mesh-diseases-anno ' +str(len(mesh_disease_anno_lost)))
    #print('lost mesh-cell-anno ' +str(len(mesh_cell_struct_anno_lost)))
    #print('lost mesh-anatomy-anno ' +str(len(mesh_anatomy_anno_lost)))
    print('lost selventa-legacy-chemicals ' +str(len(schem_lost)))
    print('lost selventa-legacy-diseases ' +str(len(sdis_lost)))
    print('lost diseases-ontology-names ' +str(len(do_lost_names)))
    print('lost diseases-ontology-ids ' +str(len(do_lost_ids)))

# values in the new .belns files that are not in the old (may be either new or a replacement)
entrez_gained = new_entrez.difference(old_entrez)
hgnc_gained = new_hgnc.difference(old_hgnc)
mgi_gained = new_mgi.difference(old_mgi)
rgd_gained = new_rgd.difference(old_rgd)
sp_gained_names = new_sp_names.difference(old_sp_names)
sp_gained_ids = new_sp_ids.difference(old_sp_ids)
affy_gained = new_affy.difference(old_affy)
chebi_gained_names = new_chebi_names.difference(old_chebi_names)
chebi_gained_ids = new_chebi_ids.difference(old_chebi_ids)
gobp_gained_ns_names = new_gobp_ns_names.difference(old_gobp_ns_names)
gobp_gained_ns_ids = new_gobp_ns_ids.difference(old_gobp_ns_ids)
gocc_gained_ns_names = new_gocc_ns_names.difference(old_gocc_ns_names)
gocc_gained_ns_ids = new_gocc_ns_ids.difference(old_gocc_ns_ids)
mesh_gained_bio = new_mesh_bio.difference(old_mesh_bio)
mesh_gained_cell = new_mesh_cell.difference(old_mesh_cell)
mesh_gained_disease = new_mesh_disease.difference(old_mesh_disease)
#mesh_disease_anno_gained = [x for x in new_mesh_disease_anno if x not in old_mesh_disease_anno]
#mesh_cell_struct_anno_gained = [x for x in new_mesh_cell_struct_anno if x not in old_mesh_cell_struct_anno]
#mesh_anatomy_anno_gained = [x for x in new_mesh_anatomy_anno if x not in old_mesh_anatomy_anno]
schem_gained_ns_names = new_schem_ns.difference(old_schem_ns)
sdis_gained_ns_names = new_sdis_ns.difference(old_sdis_ns)
do_gained_ns_names = new_do_ns_names.difference(old_do_ns_names)
do_gained_ns_ids = new_do_ns_ids.difference(old_do_ns_ids)

if verbose:
    print('===========================================')
    print('gained entrez values ' +str(len(entrez_gained)))
    print('gained hgnc values ' +str(len(hgnc_gained)))
    print('gained mgi values ' +str(len(mgi_gained)))
    print('gained rgd values ' +str(len(rgd_gained)))
    print('gained swissprot names ' +str(len(sp_gained_names)))
    print('gained swissprot ids ' +str(len(sp_gained_ids)))
    print('gained affy values ' +str(len(affy_gained)))
    print('gained chebi names ' +str(len(chebi_gained_names)))
    print('gained chebi ids ' +str(len(chebi_gained_ids)))
    print('gained gobp names ' +str(len(gobp_gained_ns_names)))
    print('gained gobp ids ' +str(len(gobp_gained_ns_ids)))
    print('gained gocc names ' +str(len(gocc_gained_ns_names)))
    print('gained gocc ids ' +str(len(gocc_gained_ns_ids)))
    print('gained mesh_bio ' +str(len(mesh_gained_bio)))
    print('gained mesh_cell ' +str(len(mesh_gained_cell)))
    print('gained mesh_disease ' +str(len(mesh_gained_disease)))
    #print('gained mesh-disease-anno ' +str(len(mesh_disease_anno_gained)))
    #print('gained mesh-cell-anno ' +str(len(mesh_cell_struct_anno_gained)))
    #print('gained mesh-anatomy-anno ' +str(len(mesh_anatomy_anno_gained)))
    print('gained selventa-legacy-chemicals ' +str(len(schem_gained_ns_names)))
    print('gained selventa-legacy-diseases ' +str(len(sdis_gained_ns_names)))
    print('gained diseases-ontology-names ' +str(len(do_gained_ns_names)))
    print('gained diseases-ontology-ids ' +str(len(do_gained_ns_ids)))
    print('===========================================')

# iterate lost values for each dataset, find out if they are withdrawn or
# replaced. If replaced, map oldname->newname. Otherwise map oldname->withdrawn.
change_log = {}
change_log['EGID'] = {}
change_log['HGNC'] = {}
change_log['MGI'] = {}
change_log['RGD'] = {}
change_log['SP'] = {}
change_log['SPAC'] = {}
change_log['GOBPID'] = {}
change_log['GOBP'] = {}
change_log['GOCCID'] = {}
change_log['GOCC'] = {}
change_log['CHEBI'] = {}
change_log['CHEBIID'] = {}
change_log['MESHPP'] = {}
change_log['MESHCL'] = {}
change_log['MESHD'] = {}
change_log['SCHEM'] = {}
change_log['SDIS'] = {}
change_log['DO'] = {}
change_log['DOID'] = {}
# download the data needed for resolving lost values
print('\nDownloading data needed for resolving changed/lost terms...')
for name, data_tuple in changelog_data.items():
    if verbose:
        print('Downloading ' +str(data_tuple[RES_LOCATION]))
    path = os.path.join('datasets/', name)
    if 'ftp' in data_tuple[RES_LOCATION] or 'http' in data_tuple[RES_LOCATION]:
        download(data_tuple[RES_LOCATION], path)

print('Resolving changed/lost terms...')
sp_accession_ids = []
for label, data_tuple in changelog_data.items():
    url = label
    parser = data_tuple[PARSER_TYPE]('datasets/'+url)

    if str(parser) == 'EntrezGeneHistory_Parser':
        log = change_log.get('EGID')
        if verbose:
            print('\nGathering Entrez update info...')
        for row in parser.parse():
            discontinued_id  = row.get('Discontinued_GeneID')
            gid = row.get('GeneID')
            replacement_id = gid if gid != '-' else 'withdrawn'
            if discontinued_id in entrez_lost:
                log[discontinued_id] = replacement_id
        unresolved = entrez_lost.difference(log)
        for value in unresolved:
            log[value] = 'unresolved'
    elif str(parser) == 'HGNC_Parser':
        if verbose:
            print('Gathering HGNC update info...')
        for row in parser.parse():
            symbol = row.get('Approved Symbol')
            ps = row.get('Previous Symbols')
            log = change_log.get('HGNC')
            previous_symbols = set(ps.split(', '))
            match = previous_symbols.intersection(hgnc_lost)
            for m in match:
                log[m] = symbol 
            if '~withdrawn' in symbol:
                old_symbol = symbol.split('~')[0]
                approved_name = row.get('Approved Name')
                if old_symbol in hgnc_lost:
                    # no replacement
                    if 'entry withdrawn' in approved_name:
                        log[old_symbol] = 'withdrawn'
                    # has a replacement
                    if 'symbol withdrawn' in approved_name:
                        new_symbol = approved_name.split('see ')[1]
                        log[old_symbol] = new_symbol
        unresolved = hgnc_lost.difference(log)
        for value in unresolved:
            log[value] = 'unresolved'

    elif str(parser) == 'MGI_Parser':
        if verbose:
            print('Gathering MGI update info...')
        for row in parser.parse():
            mgi_accession = row.get('MGI Accession ID')
            log = change_log.get('MGI')
            if mgi_accession == 'NULL':
                old_symbol = row.get('Marker Symbol')
                name = row.get('Marker Name')
                if old_symbol in mgi_lost:
                    if '=' in name:
                        log[old_symbol] = name.split('= ')[1]
                    elif 'withdrawn' in name:
                        log[old_symbol] = 'withdrawn'
        unresolved = mgi_lost.difference(log)
        for value in unresolved:
            log[value] = 'unresolved'

    elif str(parser) == 'RGD_Parser':
        # two possible cases - 
        # (1) ID retired/obsoleted (symbol is withdrawn or replaces)
        # (2) ID retained, symbol replaced
        if verbose:
            print('Gathering RGD update info...')
        for row in parser.parse():
            new_symbol = row.get('SYMBOL')
            old_symbols = set(row.get('OLD_SYMBOL').split(';'))
            log = change_log.get('RGD')
            # find lost rgd values matching old symbols
            match = rgd_lost.intersection(old_symbols)
            for m in match:
                log[m] = new_symbol

    elif str(parser) == 'RGD_Obsolete_Parser':
        # RGD file tracking retired/withdrawn RGD IDs
        if verbose:
            print('Gathering RGD obsolete ID info...')
        log = change_log.get('RGD')
        for row in parser.parse():
            old_symbol = row.get('OLD_GENE_SYMBOL')
            status = row.get('OLD_GENE_STATUS')
            new_symbol = row.get('NEW_GENE_SYMBOL')
            new_symbol_status = row.get('NEW_GENE_STATUS')
            if old_symbol in rgd_lost:
                if status == 'WITHDRAWN':
                    log[old_symbol] = 'withdrawn'
                if status == 'RETIRED' and new_symbol_status == 'ACTIVE':
                    log[old_symbol] = new_symbol  
        # TODO combine RGD parsers; should be OK as is if run in order
        unresolved = rgd_lost.difference(log)
        for value in unresolved:
            log[value] = 'unresolved' 
    elif str(parser) == 'SwissWithdrawn_Parser':
        # swissprot name changes
        if verbose:
            print('Gathering SwissProt update info...')
        cache_hits = 0
        cache_misses = 0
        files = set()
        log = change_log.get('SP')
        if not os.path.exists('cache/'):
            os.mkdir('cache/')
        for f in os.listdir('cache/'):
            if os.path.isfile('cache/'+f):
                files.add(f)
        for name in sp_lost_names:
            cached = False
            from_cache = False
            url = 'http://www.uniprot.org/uniprot/?query=mnemonic%3a'+name+ \
                '+active%3ayes&format=tab&columns=entry%20name'
            hashed_url = str(hash(url))
            ################# Use cache to limit http requests #################
            if hashed_url in files:
                cached = True
                cache_hits += 1
                with open('cache/'+hashed_url, 'rb') as fp:
                    content = pickle.load(fp)
            else:
                cache_misses += 1
                content = urllib.request.urlopen(url)

            # get the contents returned from the HTTPResponse object
            if cached:
                content_list = content
            else:
                content_list = [x.decode().strip() for x in content.readlines()]
                with open('cache/'+hashed_url, 'wb') as fp:
                    pickle.dump(content_list, fp)
            ####################################################################

            # no replacement
            if len(content_list) is 0:
                log[name] = 'withdrawn'
            # get the new name
            else:
                new_name = content_list[1]
                log[name] = new_name
        # swissprot accession numbers (ids)
        # list of deleted ids provided as file - 'delac_sp.txt' 
        log = change_log.get('SPAC')
        for row in parser.parse():
            withdrawn_id = row.get('accession')
            if withdrawn_id in sp_lost_ids:
                log[withdrawn_id] = 'withdrawn'
        unresolved = sp_lost_ids.difference(log)
        for value in unresolved:
            log[value] = 'unresolved'
        if verbose:
            print('Cache checks: ' +str(cache_hits))
            print('Cache misses: ' +str(cache_misses))

    elif str(parser) == 'GOBP_Parser':
        # GOBP name and id changes
        if verbose:
            print('Gathering GOBP update info...')

        # get obsolete term ids, includng altids
        obsolete_ids = set()
        for row in parser.obsolete_parse():
            termname = row.get('termname')
            termid = row.get('termid')
            altids = row.get('altids')
            obsolete_ids.update(altids)
            obsolete_ids.add(termid)

        # if id is obsolete, log as 'withdrawn'
        for lost_id in gobp_lost_ns_ids:
            log = change_log.get('GOBPID')
            if lost_id in obsolete_ids:
                log[lost_id] = 'withdrawn'
            else:
                log[lost_id] = 'unresolved'

        # make dictionary of ids, altids to names for non-obsolete terms
        non_obsolete_ids = {}
        for row in parser.parse():
            termname = row.get('termname')
            termid = row.get('termid')
            altids = row.get('altids')
            for altid in altids:
                non_obsolete_ids[altid] = termname
            non_obsolete_ids[termid] = termname

        # try to resolve the name
        for lost_name in gobp_lost_ns_names:
            log = change_log.get('GOBP')
            lost_id = name_to_id(lost_name)
            if lost_id in obsolete_ids:
                log[lost_name] = 'withdrawn'
            else:
                new_name = non_obsolete_ids.get(lost_id)
                if new_name is not None:
                    log[lost_name] = new_name
                else:
                    log[lost_name] = 'unresolved'

    elif str(parser) == 'GOCC_Parser':
        # GOCC name and id changes
        if verbose:
            print('Gathering GOCC update info...')

        non_obsolete_ids = {}
        obsolete_ids = set()
        # this parser only returns the obsolete terms
        for row in parser.obsolete_parse():
            termname = row.get('termname')
            termid = row.get('termid')
            altids = row.get('altids')
            obsolete_ids.add(termid)
            obsolete_ids.update(altids)

        #if id is obsolete, log as 'withdrawn'
        for lost_id in gocc_lost_ns_ids:
            log = change_log.get('GOCCID')
            if lost_id in obsolete_ids:
                log[lost_id] = 'withdrawn'
            else:
                log[lost_id] = 'unresolved'
        # this parser returns the NON-obsolete terms and
        # and maps them to the corresponding term-name
        for row in parser.parse():
            termname = row.get('termname')
            termid = row.get('termid')
            altids = row.get('altids')
            for altid in altids:
                non_obsolete_ids[altid] = termname
            non_obsolete_ids[termid] = termname

        for lost_name in gocc_lost_ns_names:
            lost_id = name_to_id(lost_name)
            new_name = non_obsolete_ids.get(lost_id)
            log = change_log.get('GOCC')
            if lost_id in obsolete_ids:
                log[lost_name] = 'withdrawn'
            elif lost_id in non_obsolete_ids:                
                log[lost_name] = new_name
            else:
                log[lost_name] = 'unresolved'

    elif str(parser) == 'CHEBI_Parser':
        if verbose:
            print('Gathering CHEBI update info...')
        # withdrawn ids not included in chebi.owl file; flag all as 'unresolved'
        log = change_log.get('CHEBIID')
        for value in chebi_lost_ids:
            log[value] = 'unresolved'
        # some names can be resolved by using the ID
        chebi_new_ids_to_names = {}
        for row in parser.parse():
            new_id = row.get('primary_id')
            new_name = row.get('name')
            alt_ids = row.get('alt_ids')
            chebi_new_ids_to_names[new_id] = new_name
            for id in alt_ids:
                chebi_new_ids_to_names[id] = new_name

        log = change_log.get('CHEBI')
        # get the corresponding ID for each name
        for name in chebi_lost_names:
            lost_id = name_to_id(name)
            # if in the new namespace, use the current name as replacement
            if lost_id in new_chebi_ids:
                new_name = chebi_new_ids_to_names[lost_id]
                log[name] = new_name
            else:
                log[name] = 'unresolved'

    elif str(parser) == 'MESHChanges_Parser':
        if verbose:
            print('Gathering MESH update info...')
        old_to_new = {}
        for row in parser.parse():
            mh_old = row.get('mh_old')
            mh_new = row.get('mh_new')
            old_to_new[mh_old] = mh_new
        bio_log = change_log.get('MESHPP')
        cell_log = change_log.get('MESHCL')
        diseases_log = change_log.get('MESHD')
        # try to resolve the lost values by using a mapping of old->new data
        for val in mesh_bio_lost:
            if val in old_to_new:
                bio_log[val] = old_to_new[val]
        for val in mesh_cell_lost:
            if val in old_to_new:
                cell_log[val] = old_to_new[val]
        for val in mesh_disease_lost:
            if val in old_to_new:
                diseases_log[val] = old_to_new[val]
        mesh_bio_unresolved = list(mesh_bio_lost.difference(bio_log))
        for value in mesh_bio_unresolved:
            bio_log[value] = 'unresolved'
        mesh_cell_unresolved = list(mesh_cell_lost.difference(cell_log))
        for value in mesh_cell_unresolved:
            cell_log[value] = 'unresolved'
        mesh_disease_unresolved = list(mesh_disease_lost.difference(diseases_log))
        for value in mesh_disease_unresolved:
            diseases_log[value] = 'unresolved'

    elif str(parser) == 'DODeprecated_Parser':
        if verbose:
            print('Gathering disease-ontology update info...')
        new_do_ids_to_names = {}
        dep_names = []

        for row in parser.parse():
            name = row.get('name')
            id = row.get('id')
            dep = row.get('deprecated')
            if dep:
                dep_names.append(name)
            else:
                new_do_ids_to_names[id] = name

        for do_lost_name in do_lost_names:
            log = change_log.get('DO')
            # could be withdrawn
            if do_lost_name in dep_names:
                log[do_lost_name] = 'withdrawn'
            # if not withdrawn, get the new name using the id
            else:
                do_id = name_to_id(do_lost_name)
                new_name = new_do_ids_to_names[do_id]
                log[do_lost_name] = new_name
        
        unresolved = do_lost_names.difference(log)
        for value in unresolved:
            log[value] = 'unresolved'

# report numbers of lost values that are resolved/replaced, withdrawn, and unresolved
# known reasons for failure to resolve terms -
#    GO BP - term moved to different domain (e.g., from Biological Process to Molecular Function)
for keyword in sorted(change_log.keys()):
    withdrawn = 0
    unresolved = 0
    replaced = 0
    lost_value_dict = change_log.get(keyword)
    lost_values = len(lost_value_dict)
    for v in lost_value_dict.values():
        if v == 'withdrawn':
            withdrawn += 1 
        elif v == 'unresolved':
            unresolved += 1
        else:
            replaced +=1
    if verbose:
        print('{0}\t{1} lost values, {2} replaced, {3} withdrawn, {4} unresolved'.format(keyword, lost_values, replaced, withdrawn, unresolved))

# add the date
today = str(datetime.date.today())
change_log['date'] = today
write_log.write(change_log)
 
end_time = time.time()
print('\nTotal runtime is '+str(((end_time - start_time) / 60)) +' minutes.')
