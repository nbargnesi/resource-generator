#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(description='check resource-generator output files')
parser.add_argument('-p',required=False, help='path for .belns and .beleq file directory')
args = parser.parse_args()
path = args.p

namespaces = ['selventa-legacy-chemical-names', 
		'selventa-legacy-diseases',
		'disease-ontology-ids',
		'disease-ontology-names',
		'mesh-biological-processes',
		'mesh-diseases', 
		'mesh-cellular-locations',
		'go-cellular-component-names',
		'go-cellular-component-ids',
		'go-biological-processes-names', 
		'go-biological-processes-ids', 
		'chebi-ids',
		'chebi-names',
		'affy-probeset-ids',
		'swissprot-accession-numbers',
		'swissprot-entry-names',
		'rgd-approved-symbols',
		'mgi-approved-symbols',
		'hgnc-approved-symbols',
		'entrez-gene-ids']

gp_root = 'entrez-gene-ids'
disease_root = 'disease-ontology-ids'
chemical_root = 'chebi-names'
bp_root = 'go-biological-processes-names'
cc_root = 'go-cellular-component-names'

gp_namespaces = ['affy-probeset-ids',
		'swissprot-accession-numbers',
		'swissprot-entry-names',
		'rgd-approved-symbols',
		'mgi-approved-symbols',
		'hgnc-approved-symbols']

disease_namespaces = ['mesh-diseases', 
		'selventa-legacy-diseases']

chemical_namespaces = ['selventa-legacy-chemical-names', 'chebi-ids']


bp_namespaces = ['mesh-biological-processes', 'go-biological-processes-ids']

cc_namespaces = ['mesh-cellular-locations',
		'go-cellular-component-ids']

def test_namespace_values(ns):
    """Outputsand compares number of values in .belns and .beleq files;
    number and identity of values is expected to match."""
    ns_vals = []
    eq_vals = []
    ns_name = n + '.belns'
    eq_name = n + '.beleq'
    try:
        with open(ns_name, 'r') as f:
            for line in iter(f):
                (value, encoding) = line.split('|')
                ns_vals.append(value)
    except IOError:
        print('{0}.belns does not appear to exist'.format(ns))
    
    try:
        with open(eq_name, 'r') as eq:
            for line in iter(eq):
                (value, uid) = line.split('|')
                eq_vals.append(value)

    except IOError:
        print('{0}.beleq does not appear to exist.'.format(ns))
    
    if len(eq_vals) > 0 and len(ns_vals) >0:

        if len(eq_vals) != len(ns_vals):
            print(ns + ' .beleq and .belns value number mismatch!')
            check =  False
            extra_vals = set(ns_vals).symmetric_difference(set(eq_vals))
  
            if len(extra_vals) > 0:
                check = False
        else:
            check = True
    else:
        check = False
    length = len(ns_vals)
    return length, check

def compare_namespace_equivalences(ns1, ns2):
    """compares uuids"""
    eq_name1 = ns1 + '.beleq'
    eq_name2 = ns2 + '.beleq'
    ns1_uids = []
    ns2_uids = set()
    ns1_length = 0
    try:
        with open(eq_name1, 'r') as eq1:
            for line in iter(eq1):
                (value, uid) = line.split('|')
                ns1_uids.append(uid)
    except IOError:
        print('{0}.beleq does not appear to exist.'.format(ns1))
        
    ns1_length = len(ns1_uids)
    try:
        with open(eq_name2, 'r') as eq2:
            for line in iter(eq2):
                (value, uid) = line.split('|')
                ns2_uids.add(uid)
    except IOError:
        print('{0}.beleq does not appear to exist.'.format(ns2))

    matches = 0
    for uid in ns1_uids:
        if uid in ns2_uids:
            matches += 1
    return matches, ns1_length

def test_namespace_equivalences(ns):
    """checks number of uuids vs number of values"""
    eq_name = ns + '.beleq'
    ns_uids = []
    try:
        with open(eq_name, 'r') as eq:
            for line in iter(eq):
                (value, uid) = line.split('|')
                ns_uids.append(uid)
    except IOError:
        print('{0}.beleq does not appear to exist.'.format(ns))

    ns_length = len(ns_uids)
    ns_unique = len(set(ns_uids))
    return ns_length, ns_unique

def get_no_match(ns1, ns2):
    """ Returns dict of ns1 values and uuids for those values 
    NOT equivalenced to ns2. """
    eq_name1 = ns1 + '.beleq'
    eq_name2 = ns2 + '.beleq'
    no_match = {}
    ns2_uids = set()
    with open(eq_name2, 'r') as eq2:
        for line in iter(eq2):
            (value, uid) = line.split('|')
            ns2_uids.add(uid)
    with open(eq_name1, 'r') as eq1:
        for line in iter(eq1):
            (value, uid) = line.split('|')
            if uid not in ns2_uids:
                no_match[value] = uid
    return no_match    

# checking namespaces and equivalence files
# check that values in ns and eq files match
for n in namespaces:
    test_namespace_values(n)

# report unique uuids vs unique values for each ns
for n in namespaces:
    (ns_length, ns_unique) = test_namespace_equivalences(n)
    print('{1} uuids for {0} values in {2}.beleq'.format(ns_length, ns_unique, n))

# report number of equivalenced values for gene and protein namespaces to root (entrez Gene)
for n in gp_namespaces:
    (matches, ns1_length) = compare_namespace_equivalences(n, gp_root)
    print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, n, gp_root))

# report number of equivalenced values for SwissProt accessions to names
# ~1200 secondary accessions are mapped to multiple entry names
(matches, ns1_length) = compare_namespace_equivalences('swissprot-accession-numbers', 'swissprot-entry-names')
print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, 'swissprot-accession-numbers', 'swissprot-entry-names'))

for n in disease_namespaces:
    (matches, ns1_length) = compare_namespace_equivalences(n, disease_root)
    print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, n, disease_root))

for n in chemical_namespaces:
    (matches, ns1_length) = compare_namespace_equivalences(n, chemical_root)
    print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, n, chemical_root))

for n in bp_namespaces:
    (matches, ns1_length) = compare_namespace_equivalences(n, bp_root)
    print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, n, bp_root))

for n in cc_namespaces:
    (matches, ns1_length) = compare_namespace_equivalences(n, cc_root)
    print('{0} of {1} values in {2} are equivalenced to {3}'.format(matches, ns1_length, n, cc_root))



