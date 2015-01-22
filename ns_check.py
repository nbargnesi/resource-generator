#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(description='check resource-generator output files')
parser.add_argument('-p',required=False, help='path for .belns and .beleq file directory')
args = parser.parse_args()
path = args.p

namespaces = ['selventa-legacy-chemicals', 
		'selventa-legacy-diseases',
		'selventa-named-complexes',
		'disease-ontology-ids',
		'disease-ontology',
		'mesh-processes',
		'mesh-diseases', 
		'mesh-cellular-structures',
		'go-cellular-component',
		'go-cellular-component-ids',
		'go-biological-process', 
		'go-biological-process-ids', 
		'chebi-ids',
		'chebi',
		'affy-probeset-ids',
		'swissprot-ids',
		'swissprot',
		'rgd-rat-genes',
		'mgi-mouse-genes',
		'hgnc-human-genes',
		'entrez-gene-ids',
		'mesh-chemicals',
		'mesh-chemicals-ids']

gp_root = 'entrez-gene-ids'
disease_root = 'disease-ontology-ids'
chemical_root = 'chebi'
bp_root = 'go-biological-process'
cc_root = 'go-cellular-component'

gp_namespaces = ['affy-probeset-ids',
		'swissprot-ids',
		'swissprot',
		'rgd-rat-genes',
		'mgi-mouse-genes',
		'hgnc-human-genes']

disease_namespaces = ['mesh-diseases', 
		'selventa-legacy-diseases']

chemical_namespaces = ['selventa-legacy-chemicals', 'chebi-ids', 'mesh-chemicals-ids']


bp_namespaces = ['mesh-processes', 'go-biological-process-ids']

cc_namespaces = ['mesh-cellular-structures',
		'go-cellular-component-ids',
		'selventa-named-complexes']

def get_value_dict(f):
	""" Return dictionary of values and encoding or uuids from a 
	.belns or .beleq file. """
	value_dict = {}
	value_block = False
	for line in iter(f):
		if line.strip() == '[Values]':
			value_block = True
		elif value_block is True:
			(value, other) = line.split('|')
			value_dict[value] = other
	return value_dict
	

def test_namespace_values(ns):
	"""Outputsand compares number of values in .belns and .beleq files;
	number and identity of values is expected to match."""
	ns_name = n + '.belns'
	eq_name = n + '.beleq'
	try:
		with open(ns_name, 'r') as f:
			ns_dict = get_value_dict(f)
	
	except IOError:
		print('{0}.belns does not appear to exist'.format(ns))
		return None, None
	
	try:
		with open(eq_name, 'r') as eq:
			eq_dict = get_value_dict(eq)
	
	except IOError:
		print('{0}.beleq does not appear to exist.'.format(ns))
		return None, None
	
	if len(eq_dict.keys()) > 0 and len(ns_dict.keys()) >0:

		if len(eq_dict.keys()) != len(ns_dict.keys()):
			print(ns + ' .beleq {0} and .belns {1} value number mismatch!'.format(len(eq_dict.keys()), len(ns_dict.keys())))
			check =	 False
			extra_vals = set(ns_dict.keys()).symmetric_difference(set(eq_dict.keys()))
  
			if len(extra_vals) > 0:
				check = False
		else:
			check = True
	else:
		check = False
	length = len(ns_dict.keys())
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
			eq1_dict = get_value_dict(eq1)
			for value, uuid in eq1_dict.items():
				ns1_uids.append(uuid)
	except IOError:
		print('{0}.beleq does not appear to exist.'.format(ns1))
		
	ns1_length = len(ns1_uids)
	try:
		with open(eq_name2, 'r') as eq2:
			eq2_dict = get_value_dict(eq2)
			for value, uuid in eq2_dict.items():
				ns2_uids.add(uuid)
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
			eq_dict = get_value_dict(eq)
			for value, uuid in eq_dict.items():
				ns_uids.append(uuid)
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
		eq2_dict = get_value_dict(eq2)
		for value, uid in eq2_dict.items():
			ns2_uids.add(uid)
	with open(eq_name1, 'r') as eq1:
		eq1_dict = get_value_dict(eq1)
		for value, uid in eq1_dict.items():
			if uid not in ns2_uids:
				no_match[value] = uid
	return no_match	   

# checking namespaces and equivalence files
# check that values in ns and eq files match
for n in namespaces:
	length, check = test_namespace_values(n)
	print('{0} - {1} - {2}'.format(n, length, check))

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
(matches, ns1_length) = compare_namespace_equivalences('swissprot-ids', 'swissprot')
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



# vim: ts=4 sts=4 sw=4 noexpandtab
