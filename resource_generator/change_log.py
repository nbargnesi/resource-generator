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
import parsed
import time
from changelog_config import changelog_data_opt
from constants import RES_LOCATION, PARSER_TYPE

# parse any files needed for change-log resolution
# for label, data_tuple in changelog_data_opt.items():
#     url = data_tuple[RES_LOCATION]
#     parser = data_tuple[PARSER_TYPE](url)
#     print('Running ' +str(parser))
#     for x in parser.parse():
#         parsed.build_data(x, str(parser))


# BELNamespaceParser - parse() returns the specific url for each namespace
# currently published on resource.belframework.org
start_time = time.time()
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
old_gobp_ns_ids = set()
old_gobp_ns_names = set()
old_gocc_ns_ids = set()
old_gocc_ns_names = set()

old_gobp_eq_ids = dict()
old_gobp_eq_names = dict()
old_gocc_eq_ids = dict()
old_gocc_eq_names = dict()

# iterate over the urls to the .belns files, collecting the entries
# from the old data.
for url in parser.parse():
    debug = False
    # if 'go-cellular-component-acc' in url:
    #     debug = True
    #     ipdb.set_trace()
    namespaces = { 'entrez' : (False, old_entrez),
                   'hgnc' : (False, old_hgnc),
                   'mgi' : (False, old_mgi),
                   'rgd' : (False, old_rgd),
                   'swissprot-entry' : (False, old_sp_names),
                   'swissprot-accession' : (False, old_sp_acc),
                   'affy' : (False, old_affy),
                   'chebi-name' : (False, old_chebi_names),
                   'chebi-id' : (False, old_chebi_ids),
                   'go-biological-processes-acc' : (False, old_gobp_ns_ids),
                   'go-biological-processes-names' : (False, old_gobp_ns_names),
                   'go-cellular-component-terms' : (False, old_gocc_ns_names),
                   'go-cellular-component-acc' : (False, old_gocc_ns_ids)}

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

# parse the .beleq files needed for resolving lost values
parser = parsers.BELEquivalenceParser()
print('Running BELEquivalence_Parser')
for url in parser.parse():

    equivalences = {
        'go-biological-processes-acc' : (False, old_gobp_eq_ids),
        'go-biological-processes-names' : (False, old_gobp_eq_names),
        'go-cellular-component-terms' : (False, old_gocc_eq_names),
        'go-cellular-component-acc' : (False, old_gocc_eq_ids)}

    open_url = urllib.request.urlopen(url)
    for eq in equivalences:
        if eq in open_url.url:
            equivalences[ns] = (True, equivalences[eq][1])
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
#        ipdb.set_trace()
        for k, v in equivalences.items():
            if v[0]:
                v[1][value] = uid
#                v[1].add(value, uid)

# reverse the dicts, the uuids will be the keys
#    ipdb.set_trace()
inv_gobp_ids = {v:k for k, v in old_gobp_eq_ids.items()}
inv_gobp_names = {v:k for k, v in old_gobp_eq_names.items()}
inv_gocc_ids = {v:k for k, v in old_gocc_eq_ids.items()}
inv_gocc_names = {v:k for k, v in old_gocc_eq_names.items()}

gobp_names_to_ids = {}
gocc_names_to_ids = {}
# any keys that match up, get the corresponding name/id
for uid in inv_gobp_ids:
    if uid in inv_gobp_names:
        name = inv_gobp_names.get(uid)
        id = inv_gobp_ids.get(uid)
        gobp_names_to_ids[name] = id
for uid in inv_gocc_ids:
    if uid in inv_gocc_names:
        name = inv_gocc_names.get(uid)
        id = inv_gocc_ids.get(uid)
        gocc_names_to_ids[name] = id

def name_to_id(name):
#    ipdb.set_trace()
    if name in gobp_names_to_ids:
#        ipdb.set_trace()
        return gobp_names_to_ids[name]
    elif name in gocc_names_to_ids:
#        ipdb.set_trace()
        return gocc_names_to_ids[name]
    else:
 #       print('gobp name |'+name+'| not in old data.')
        return None

print('===========================================')
print('len of old entrez is ' +str(len(old_entrez)))
print('len of old hgnc is ' +str(len(old_hgnc)))
print('len of old mgi is ' +str(len(old_mgi)))
print('len of old rgd is ' +str(len(old_rgd)))
print('len of old swissprot names is ' +str(len(old_sp_names)))
print('len of old swissprot accessions is ' +str(len(old_sp_acc)))
print('len of old affy is ' +str(len(old_affy)))
print('len of old chebi names is ' +str(len(old_chebi_names)))
print('len of old chebi ids is ' +str(len(old_chebi_ids)))
print('len of old gobp names is ' +str(len(old_gobp_ns_names)))
print('len of old gobp ids is ' +str(len(old_gobp_ns_ids)))
print('len of old gocc names is ' +str(len(old_gocc_ns_names)))
print('len of old gocc ids is ' +str(len(old_gocc_ns_ids)))
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
new_gobp_ns_ids = set()
new_gobp_ns_names = set()
new_gocc_ns_ids = set()
new_gocc_ns_names = set()

# gather the new data for comparison (locally stored for now)
indir = '/home/jhourani/openbel-contributions/resource_generator/lions'
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
            elif 'hgnc' in newf.name:
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
            elif 'mgi' in newf.name:
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
            elif 'rgd' in newf.name:
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
            elif 'swiss-acc' in newf.name:
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
            elif 'swiss-entry' in newf.name:
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
            elif 'affy' in newf.name:
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
            elif 'chebi-names' in newf.name:
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
            elif 'chebi-ids' in newf.name:
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
            elif 'go-biological-processes-acc' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_gobp_ns_ids.add(token)
            elif 'go-biological-processes-names' in newf.name:
                fp = open(newf.name, 'r')
                for line in fp:
                    # if '[Values]' in str(line):
                    #     marker = True
                    #     continue
                    # if marker is False:
                    #     continue
                    tokenized = str(line).split('|')
                    token = tokenized[0]
                    new_gobp_ns_names.add(token)



print('len of new entrez is ' +str(len(new_entrez)))
print('len of new hgnc is ' +str(len(new_hgnc)))
print('len of new mgi is ' +str(len(new_mgi)))
print('len of new rgd is ' +str(len(new_rgd)))
print('len of new swiss names is ' +str(len(new_sp_names)))
print('len of new swiss acc is ' +str(len(new_sp_acc)))
print('len of new affy is ' +str(len(new_affy)))
print('len of new chebi names is ' +str(len(new_chebi_names)))
print('len of new chebi ids is ' +str(len(new_chebi_ids)))
print('len of new gobp names is ' +str(len(new_gobp_ns_names)))
print('len of new gobp ids is ' +str(len(new_gobp_ns_ids)))
print('len of new gocc names is ' +str(len(new_gocc_ns_names)))
print('len of new gocc ids is ' +str(len(new_gocc_ns_ids)))

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
gobp_lost_ns_names = [x for x in old_gobp_ns_names if x not in new_gobp_ns_names]
gobp_lost_ns_ids = [x for x in old_gobp_ns_ids if x not in new_gobp_ns_ids]
gocc_lost_ns_names = [x for x in old_gocc_ns_names if x not in new_gocc_ns_names]
gocc_lost_ns_ids = [x for x in old_gocc_ns_ids if x not in new_gocc_ns_ids]

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
print('lost gobp names ' +str(len(gobp_lost_ns_names)))
print('lost gobp ids ' +str(len(gobp_lost_ns_ids)))
print('lost gocc names ' +str(len(gocc_lost_ns_names)))
print('lost gocc ids ' +str(len(gocc_lost_ns_ids)))

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
gobp_gained_ns_names = [x for x in new_gobp_ns_names if x not in old_gobp_ns_names]
gobp_gained_ns_ids = [x for x in new_gobp_ns_ids if x not in old_gobp_ns_ids]
gocc_gained_ns_names = [x for x in new_gocc_ns_names if x not in old_gocc_ns_names]
gocc_gained_ns_ids = [x for x in new_gocc_ns_ids if x not in old_gocc_ns_ids]

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
print('gained gobp names ' +str(len(gobp_gained_ns_names)))
print('gained gobp ids ' +str(len(gobp_gained_ns_ids)))
print('gained gocc names ' +str(len(gocc_gained_ns_names)))
print('gained gocc ids ' +str(len(gocc_gained_ns_ids)))
print('===========================================')

# with open('hgnc-new-values.txt', 'w') as fp:
#     for val in hgnc_gained:
#         fp.write(val +'\n')

# iterate lost values for each dataset, find out if they are withdrawn or
# replaced. If replaced, map oldname->newname. Otherwise map oldname->withdrawn.
change_log = {}
change_log['entrez'] = {}
change_log['hgnc'] = {}
change_log['mgi'] = {}
change_log['rgd'] = {}
change_log['swiss-names'] = {}
change_log['gobp-ids'] = {}
change_log['gobp-names'] = {}
change_log['gocc-ids'] = {}
change_log['gocc-names'] = {}

for label, data_tuple in changelog_data_opt.items():
    url = data_tuple[RES_LOCATION]
    parser = data_tuple[PARSER_TYPE](url)

    if str(parser) == 'EntrezGeneHistory_Parser':
        print('Gathering Entrez update info...')
        for row in parser.parse():
            discontinued_id  = row.get('Discontinued_GeneID')
            gid = row.get('GeneID')
            replacement_id = gid if gid != '-' else 'withdrawn'
            log = change_log.get('entrez')
            log[discontinued_id] = replacement_id

    elif str(parser) == 'HGNC_Parser':
        print('Gathering HGNC update info...')
        for row in parser.parse():
            val = row.get('Approved Symbol')
            if '~withdrawn' in val:
                new_name = row.get('Approved Name')
                # no replacement
                if 'entry withdrawn' in new_name:
                    old_val = val.split('~')[0]
                    log = change_log.get('hgnc')
                    log[old_val] = 'withdrawn'
                # has a replacement
                if 'symbol withdrawn' in new_name:
                    old_val = val.split('~')[0]
                    new_val = new_name.split('see ')[1]
                    log = change_log.get('hgnc')
                    log[old_val] = new_val

    elif str(parser) == 'MGI_Parser':
        print('Gathering MGI update info...')
        for row in parser.parse():
            old_val = row.get('Marker Symbol')
            name = row.get('Marker Name')
            if '=' in name:
                log = change_log.get('mgi')
                log[old_val] = name.split('= ')[1]
            if 'withdrawn ' in name:
                log = change_log.get('mgi')
                log[old_val] = 'withdrawn'

    elif str(parser) == 'RGD_Parser':
        # rgd changes (still dont know if withdrawn or replaced!!)
        print('Gathering RGD update info...')
        for row in parser.parse():
            new_val = row.get('SYMBOL')
            lost_vals = row.get('OLD_SYMBOL').split(';')
            for symbol in lost_vals:
                log = change_log.get('rgd')
                log[symbol] = new_val

    elif str(parser) == 'SwissWithdrawn_Parser':
        # swissprot name changes
        print('Gathering SwissProt update info...')
        cache_hits = 0
        cache_misses = 0
        files = set()
        for f in os.listdir('lions/cache/'):
            if os.path.isfile('lions/cache/'+f):
                files.add(f)
        for name in sp_lost_names:
            cached = False
            from_cache = False
            url = 'http://www.uniprot.org/uniprot/?query=mnemonic%3a'+name+ \
                '+active%3ayes&format=tab&columns=entry%20name'
            hashed_url = str(hash(url))
            ################### For Testing Only - use cache ##################
            if hashed_url in files:
                cached = True
                cache_hits += 1
                with open('lions/cache/'+hashed_url, 'rb') as fp:
                    content = pickle.load(fp)
            else:
                cache_misses += 1
                content = urllib.request.urlopen(url)

            # get the contents returned from the HTTPResponse object
            if cached:
#                ipdb.set_trace()
                content_list = content
            else:
                content_list = [x.decode().strip() for x in content.readlines()]
                with open('lions/cache/'+hashed_url, 'wb') as fp:
                    pickle.dump(content_list, fp)
            ####################################################################

            # no replacement
            if len(content_list) is 0:
                log = change_log.get('swiss-names')
                log[name] = 'withdrawn'
            # get the new name
            else:
                new_name = content_list[1]
                log = change_log.get('swiss-names')
                log[name] = new_name
        # swissprot accession names
        accessions = []
        for row in parser.parse():
            accessions.append(row.get('accession'))
        # values removed since the last namespace, but NOT found in the
        # list provided by swiss prot
        unresolved_from_old = [x for x in sp_lost_acc if x not in accessions]
        # values swiss prot has listed as withdrawn, but they have NOT been
        # withdrawn in our new namespace
        unresolved_from_new = [x for x in accessions if x not in sp_lost_acc]
        unresolved = unresolved_from_old + unresolved_from_new

    elif str(parser) == 'GOBP_Parser':
        # GOBP name and id changes
        print('Gathering GOBP update info...')
        # treat every id as obsolete
        for lost_id in gobp_lost_ns_ids:
            log = change_log.get('gobp-ids')
            log[lost_id] = 'withdrawn'

        non_obsolete_terms = {}
        obsolete_terms = set()
        # this parser only returns the obsolete terms
        for row in parser.obsolete_parse():
            termname = row.get('termname')
            termid = row.get('termid')
            obsolete_terms.add(termid)

        # this parser only returns the NON-obsolete terms
        for row in parser.parse():
            termname = row.get('termname')
            termid = row.get('termid')
            non_obsolete_terms[termid] = termname

        # try to resolve the name
        for lost_name in gobp_lost_ns_names:
            lost_id = name_to_id(lost_name)
            if lost_id in obsolete_terms:
                log = change_log.get('gobp-names')
                log[lost_name] = 'withdrawn'
            else:
                new_name = non_obsolete_terms.get(lost_id)
                log = change_log.get('gobp-names')
                log[lost_name] = new_name

    elif str(parser) == 'GOCC_Parser':
        # GOBP name and id changes
        print('Gathering GOCC update info...')
        # treat every id as obsolete
        for lost_id in gocc_lost_ns_ids:
            log = change_log.get('gocc-ids')
            log[lost_id] = 'withdrawn'

        non_obsolete_terms = {}
        obsolete_terms = set()
        # this parser only returns the obsolete terms
        for row in parser.obsolete_parse():
            termname = row.get('termname')
            termid = row.get('termid')
            obsolete_terms.add(termid)

        # this parser only returns the NON-obsolete terms and
        # and maps them to the corresponding term-name
        for row in parser.parse():
            termname = row.get('termname')
            termid = row.get('termid')
            non_obsolete_terms[termid] = termname

        for lost_name in gocc_lost_ns_names:
            lost_id = name_to_id(lost_name)
            if lost_id in obsolete_terms:
                log = change_log.get('gocc-names')
                log[lost_name] = 'withdrawn'
            else:
                new_name = non_obsolete_terms.get(lost_id)
                log = change_log.get('gocc-names')
                log[lost_name] = new_name

end_time = time.time()

# verification and error checking
dataset = change_log.get('entrez')
e_unresolved = [x for x in entrez_lost if x not in dataset]
#ipdb.set_trace()
dataset = change_log.get('hgnc')
hgnc_unresolved = [x for x in hgnc_lost if x not in dataset]

dataset = change_log.get('mgi')
mgi_unresolved = [x for x in mgi_lost if x not in dataset]

dataset = change_log.get('rgd')
rgd_unresolved = [x for x in rgd_lost if x not in dataset]

dataset = change_log.get('swiss-names')
sp_unresolved_names = [x for x in sp_lost_names if x not in dataset]

sp_unresolved_ids = unresolved

#chebi_unresolved_names = [x for x in chebi_lost_names if x not in change_log]
#chebi_unresolved_ids = [x for x in chebi_lost_ids if x not in change_log]

dataset = change_log.get('gobp-ids')
gobp_unresolved_ids = [x for x in gobp_lost_ns_ids if x not in dataset]

dataset = change_log.get('gobp-names')
gobp_unresolved_names = [x for x in gobp_lost_ns_names if x not in dataset]


dataset = change_log.get('gocc-ids')
gocc_unresolved_ids = [x for x in gocc_lost_ns_ids if x not in dataset]

dataset = change_log.get('gocc-names')
gocc_unresolved_names = [x for x in gocc_lost_ns_names if x not in dataset]

print('===========================================')
print('entrez unresolved: ' +str(len(e_unresolved)))
print('hgnc unresolved: ' +str(len(hgnc_unresolved)))
print('mgi unresolved: ' +str(len(mgi_unresolved)))
print('rgd unresolved: ' +str(len(rgd_unresolved)))
print('swissprot unresolved names: ' +str(len(sp_unresolved_names)))
print('swissprot unresolved ids: ' +str(len(sp_unresolved_ids)))
#print('chebi unresolved names: ' +str(len(chebi_unresolved_names)))
#print('chebi unresolved ids: ' +str(len(chebi_unresolved_ids)))
print('gobp unresolved names: ' +str(len(gobp_unresolved_names)))
print('gobp unresolved ids: ' +str(len(gobp_unresolved_ids)))
print('gocc unresolved names: ' +str(len(gocc_unresolved_names)))
print('gocc unresolved ids: ' +str(len(gocc_unresolved_ids)))
print('Cache checks: ' +str(cache_hits))
print('Cache misses: ' +str(cache_misses))
# add the date
today = str(datetime.date.today())
change_log['date'] = today
write_log.write(change_log)
print('total runtime is '+str(((end_time - start_time) / 60)) +' minutes.')
