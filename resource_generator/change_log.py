#!/usr/bin/env python3
# coding: utf-8
#
# change_log.py

import parsers
import urllib
import os
import write_log
import datetime
import pickle
import ipdb
import time
import datasets
from configuration import hgnc_update_data, mgi_update_data, \
    rgd_update_data, gp_reference_history

# parse any files needed for change-log resolution
parser = parsers.SwissWithdrawnParser()
print('Running ' +str(parser))



# BELNamespaceParser - parse() returns the specific url for each namespace
# currently published on resource.belframework.org
parser = parsers.BELNamespaceParser()
print('Running BELNamespace_Parser')
old_entrez = set()
old_hgnc = set()
old_mgi = set()
old_rgd = set()
old_sp_names = set()
old_sp_acc = set()
old_affy = set()
old_chebi_names = set()
old_chebi_ids = set()
# iterate over the urls to the .belns files, collecting the entries
# from the old data.
for url in parser.parse():
    namespaces = { 'entrez' : (False, old_entrez),
                   'hgnc' : (False, old_hgnc),
                   'mgi' : (False, old_mgi),
                   'rgd' : (False, old_rgd),
                   'swissprot-entry' : (False, old_sp_names),
                   'swissprot-accession' : (False, old_sp_acc),
                   'affy' : (False, old_affy),
                   'chebi-name' : (False, old_chebi_names),
                   'chebi-id' : (False, old_chebi_ids) }

    open_url = urllib.request.urlopen(url)
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
        for k, v in namespaces.items():
            if v[0]:
                v[1].add(token)

print('===========================================')
print('len of old entrez is ' +str(len(old_entrez)))
print('len of old hgnc is ' +str(len(old_hgnc)))
print('len of old mgi is ' +str(len(old_mgi)))
print('len of old rgd is ' +str(len(old_rgd)))
print('len of old swissprot names is ' +str(len(old_sp_names)))
print('len of old swissprot accessions is ' +str(len(old_sp_acc)))
print('len of old affy is ' +str(len(old_affy)))
print('len of old chebi names is ' +str(len(old_chebi_names)))
print('len of old chebi ids is' +str(len(old_chebi_ids)))
print('===========================================')

new_entrez = set()
new_hgnc = set()
new_mgi = set()
new_rgd = set()
new_sp_names = set()
new_sp_acc = set()
new_affy = set()
new_chebi_names = set()
new_chebi_ids = set()
# gather the new data for comparison (locally stored for now)
indir = '/home/jhourani/openbel-contributions/resource_generator/touchdown'
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        if '.belns' in f:
            newf = open(os.path.join(root, f), 'r')
            if 'entrez' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_entrez.add(token)
            if 'hgnc' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_hgnc.add(token)
            if 'mgi' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_mgi.add(token)
            if 'rgd' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_rgd.add(token)
            if 'swiss-acc' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_sp_acc.add(token)
            if 'swiss-names' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_sp_names.add(token)
            if 'affy' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_affy.add(token)
            if 'chebi-names' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_chebi_names.add(token)
            if 'chebi-ids' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_chebi_ids.add(token)


print('len of new entrez is ' +str(len(new_entrez)))
print('len of new hgnc is ' +str(len(new_hgnc)))
print('len of new mgi is ' +str(len(new_mgi)))
print('len of new rgd is ' +str(len(new_rgd)))
print('len of new swiss names is ' +str(len(new_sp_names)))
print('len of new swiss acc is ' +str(len(new_sp_acc)))
print('len of new affy is ' +str(len(new_affy)))
print('len of new chebi names is ' +str(len(new_chebi_names)))
print('len of new chebi ids is ' +str(len(new_chebi_ids)))

# values in the old data that are not in the new (either withdrawn or replaced)
entrez_lost = [x for x in old_entrez if x not in new_entrez]
hgnc_lost = [x for x in old_hgnc if x not in new_hgnc]
mgi_lost = [x for x in old_mgi if x not in new_mgi]
rgd_lost = [x for x in old_rgd if x not in new_rgd]
sp_lost_names = [x for x in old_sp_names if x not in new_sp_names]
sp_lost_acc = [x for x in old_sp_acc if x not in new_sp_acc]
affy_lost = [x for x in old_affy if x not in new_affy]
chebi_lost_names = [x for x in old_chebi_names if x not in new_chebi_names]
chebi_lost_ids = [x for x in old_chebi_ids if x not in new_chebi_ids]

print('===========================================')
print('lost entrez values ' +str(len(entrez_lost)))
print('lost hgnc values ' +str(len(hgnc_lost)))
print('lost mgi values ' +str(len(mgi_lost)))
print('lost rgd values ' +str(len(rgd_lost)))
print('lost swissprot names ' +str(len(sp_lost_names)))
print('lost swissprot ids ' +str(len(sp_lost_acc)))
print('lost affy values ' +str(len(affy_lost)))
print('lost chebi names ' +str(len(chebi_lost_names)))
print('lost chebi ids ' +str(len(chebi_lost_ids)))
print('===========================================')

# values in the new data that are not in the old (either new or a replacement)
entrez_gained = [x for x in new_entrez if x not in old_entrez]
hgnc_gained = [x for x in new_hgnc if x not in old_hgnc]
mgi_gained = [x for x in new_mgi if x not in old_mgi]
rgd_gained = [x for x in new_rgd if x not in old_rgd]
sp_gained_names = [x for x in new_sp_names if x not in old_sp_names]
sp_gained_acc = [x for x in new_sp_acc if x not in old_sp_acc]
affy_gained = [x for x in new_affy if x not in old_affy]
chebi_gained_names = [x for x in new_chebi_names if x not in old_chebi_names]
chebi_gained_ids = [x for x in new_chebi_ids if x not in old_chebi_ids]

print('===========================================')
print('gained entrez values ' +str(len(entrez_gained)))
print('gained hgnc values ' +str(len(hgnc_gained)))
print('gained mgi values ' +str(len(mgi_gained)))
print('gained rgd values ' +str(len(rgd_gained)))
print('gained swissprot names ' +str(len(sp_gained_names)))
print('gained swissprot ids ' +str(len(sp_gained_acc)))
print('gained affy values ' +str(len(affy_gained)))
print('gained chebi names ' +str(len(chebi_gained_names)))
print('gained chebi ids ' +str(len(chebi_gained_ids)))
print('===========================================')

# with open('hgnc-new-values.txt', 'w') as fp:
#     for val in hgnc_gained:
#         fp.write(val +'\n')

# iterate lost values for each dataset, find out if they are withdrawn or
# replaced. If replaced, map oldname->newname. Otherwise map oldname->withdrawn.
change_log = {}

# entrez changes
parser = parsers.EntrezGeneHistoryParser(gp_reference_history.file_to_url)
print('Gathering Entrez update info...')
for row in parser.parse():
    discontinued_id  = row.get('Discontinued_GeneID')
    gid = row.get('GeneID')
    replacement_id = gid if gid != '-' else 'withdrawn'
    change_log[discontinued_id] = replacement_id

# hgnc changes
parser = parsers.HGNCParser(hgnc_update_data.file_to_url)
print('Gathering HGNC update info...')
for row in parser.parse():
    val = row.get('Approved Symbol')
    if '~withdrawn' in val:
        new_name = row.get('Approved Name')
        # no replacement
        if 'entry withdrawn' in new_name:
            old_val = val.split('~')[0]
            change_log[old_val] = 'withdrawn'
        # has a replacement
        if 'symbol withdrawn' in new_name:
            old_val = val.split('~')[0]
            new_val = new_name.split('see ')[1]
            change_log[old_val] = new_val

# mgi changes
parser = parsers.MGIParser(mgi_update_data.file_to_url)
print('Gathering MGI update info...')
for row in parser.parse():
    old_val = row.get('Marker Symbol')
    name = row.get('Marker Name')
    if '=' in name:
        change_log[old_val] = name.split('= ')[1]
    if 'withdrawn ' in name:
        change_log[old_val] = 'withdrawn'

# rgd changes (still dont know if withdrawn or replaced!!)
parser = parsers.RGDParser(rgd_update_data.file_to_url)
print('Gathering RGD update info...')
for row in parser.parse():
    new_val = row.get('SYMBOL')
    lost_vals = row.get('OLD_SYMBOL').split(';')
    for symbol in lost_vals:
        change_log[symbol] = new_val

# swissprot changes
print('Gathering SwissProt update info...')
start_time = time.time()
cache_hits = 0
cache_misses = 0
#os.mkdir('cache/')
for name in sp_lost_names:
    cached = False
    url = 'http://www.uniprot.org/uniprot/?query=mnemonic%3a'+name+ \
        '+active%3ayes&format=tab&columns=entry%20name'
    hashed_url = hash(url)
    ###################### For Testing Only - use cache ########################
    files = set()
    for f in os.listdir('cache/'):
        if os.path.isfile('cache/' +f):
            files.add(f)
    if hashed_url in files:
        cached = True
        cache_hits += 1
        content = pickle.load('cache/' +hashed_url)
    else:
        cache_misses += 1
        content = urllib.request.urlopen(url)

    # get the contents returned from the HTTPResponse object
    content_list = [x.decode().strip() for x in content.readlines()]
    if not cached:
        with open('cache/'+str(hashed_url), 'wb') as fp:
            pickle.dump(content_list, fp)
    ############################################################################

    # no replacement
    if len(content_list) is 0:
        change_log[name] = 'withdrawn'
    # get the new name
    else:
        new_name = content_list[1]
        change_log[name] = new_name

for acc in sp_lost_acc:
    
end_time = time.time()
print('total runtime is '+str(((end_time - start_time) / 60)) +' minutes.')

# verification and error checking
e_unknowns = [x for x in entrez_lost if x not in change_log]
hgnc_unknowns = [x for x in hgnc_lost if x not in change_log]
mgi_unknowns = [x for x in mgi_lost if x not in change_log]
rgd_unknowns = [x for x in rgd_lost if x not in change_log]
sp_unknown_names = [x for x in sp_lost_names if x not in change_log]
sp_unknown_acc = [x for x in sp_lost_acc if x not in change_log]
chebi_unknown_names = [x for x in chebi_lost_names if x not in change_log]
chebi_unknown_ids = [x for x in chebi_lost_ids if x not in change_log]

print('entrez unknowns: ' +str(len(e_unknowns)))
print('hgnc unknowns: ' +str(len(hgnc_unknowns)))
print('mgi unknowns: ' +str(len(mgi_unknowns)))
print('rgd unknowns: ' +str(len(rgd_unknowns)))
print('swissprot unknown names: ' +str(len(sp_unknown_names)))
print('swissprot unknown acc: ' +str(len(sp_unknown_acc)))
print('chebi unknown names: ' +str(len(chebi_unknown_names)))
print('chebi unknown ids: ' +str(len(chebi_unknown_ids)))

print('Cache checks: ' +str(cache_hits))
print('Cache misses: ' +str(cache_misses))
# add the date
today = str(datetime.date.today())
change_log['date'] = today
write_log.write(change_log)
