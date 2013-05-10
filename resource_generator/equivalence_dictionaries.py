#!/usr/bin/env python3.3
from collections import defaultdict
import urllib.request
import csv
import operator
import sys
import gzip
from string import Template
csv.field_size_limit(262144)


def get_data(url):
    REQ = urllib.request.urlopen(url)
    file_name = url.split('/')[-1]
    with open(file_name,'b+w') as f:
        f.write(REQ.read())
    return file_name

EGID_url = 'http://resource.belframework.org/belframework/1.0/equivalence/entrez-gene-ids-hmr.beleq'
SP_url = 'http://resource.belframework.org/belframework/1.0/equivalence/swissprot-entry-names.beleq'
HGNC_url = 'http://resource.belframework.org/belframework/1.0/equivalence/hgnc-approved-symbols.beleq'
MGI_url = 'http://resource.belframework.org/belframework/1.0/equivalence/mgi-approved-symbols.beleq'

# open and save SP beleq document


# parse beleq document and make dictionary of UUIDs
EGID_eq = {}
with open(get_data(EGID_url),'r') as eq:
    reader = csv.reader(eq, delimiter='|')
    for row in reader:
    # need to find row after [Values]
        if len(row) == 2:
            if len(row[1]) > 10:
                EGID_eq[row[0]] = row[1]

EGID_to_HGNC = {}
EGID_to_MGI = {}
EGID_to_SP = {}

# parse beleq document and make dictionary of UUIDs
HGNC_eq = {}
with open(get_data(HGNC_url),'r') as eq:
    reader = csv.reader(eq, delimiter='|')
    for row in reader:
    # need to find row after [Values]
        if len(row) == 2:
            if len(row[1]) > 10:
                HGNC_eq[row[1]] = row[0]

# parse beleq document and make dictionary of UUIDs
MGI_eq = {}
with open(get_data(MGI_url),'r') as eq:
    reader = csv.reader(eq, delimiter='|')
    for row in reader:
    # need to find row after [Values]
        if len(row) == 2:
            if len(row[1]) > 10:
                MGI_eq[row[1]] = row[0]

# parse beleq document and make dictionary of UUIDs
SP_eq = {}
with open(get_data(SP_url),'r') as eq:
    reader = csv.reader(eq, delimiter='|')
    for row in reader:
    # need to find row after [Values]
        if len(row) == 2:
            if len(row[1]) > 10:
                SP_eq[row[1]] = row[0]

for k,v in EGID_eq.items():
    if v in HGNC_eq:
        EGID_to_HGNC[k] = HGNC_eq[v]
    else:
        EGID_to_HGNC[k] = "NONE"
    #nv =  EGID_to_HGNC[k]
    #print(k + ' => ' + nv)

for k,v in EGID_eq.items():
    if v in MGI_eq:
        EGID_to_MGI[k] = MGI_eq[v]
    else:
        EGID_to_MGI[k] = "NONE"

for k,v in EGID_eq.items():
    if v in SP_eq:
        EGID_to_SP[k] = SP_eq[v]
    else:
        EGID_to_SP[k] = "NONE"

