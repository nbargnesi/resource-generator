# coding: utf-8

'''
 equiv.py

 Construct each of the .beleq files, given a particular dataset.
 This involves gathering all the terms and determining whether
 or not there are existing terms that refer to the same thing.
 Terms are either then equivalenced to something else, or given
 a new uuid.

'''

import uuid
import csv
import parsed
import configuration
import os
import time
from collections import defaultdict
from common import get_citation_info

# stores xrefs from EGID dataset to build equivalences
# to HGNC, MGI, and RGD - see resolve_entrez_id()
entrez_converter = {}
# primary root for all gene/protein data sets
# needed for HGNC, MGI, RGD, SP, and AFFX
entrez_eq = {}
# need hgnc, mgi, rgd id equivalence dicts for swissprot
hgnc_id_eq, mgi_id_eq, rgd_id_eq = {}, {}, {}
# need chebi id equivalence dict for schem
chebi_id_eq = {}
# need GOBP names for equivalencing MESHPP by string match
gobp_eq_dict = {}
# need GOCC ids for equivalencing to SCOMP
# need GOCC names for equivalencing MESHCL by string match
gocc_eq_dict, gocc_names_eq = {}, {}
# need DO ids for equivalencing to MESHD
do_id_eq = {}

def equiv(d, verbose):
	if str(d) == 'egid':
		id_temp_dict, name_temp_dict = write_root_beleq(d, verbose)
		entrez_eq.update(id_temp_dict)
		# Make entrez_converter equivalence dictionary for Entrez to HGNC, MGI, RGD
		for term_id in d.get_values():
			dbXrefs = d.get_xrefs(term_id)
			for dbXref in dbXrefs:
				entrez_converter[dbXref] = term_id

	elif str(d) == 'hgnc':
		id_temp_dict, name_temp_dict = resolve_entrez_id(d, verbose)
		hgnc_id_eq.update(id_temp_dict)
	
	elif str(d) == 'mgi':
		id_temp_dict, name_temp_dict = resolve_entrez_id(d, verbose)
		mgi_id_eq.update(id_temp_dict)

	elif str(d) == 'rgd':
		id_temp_dict, name_temp_dict = resolve_entrez_id(d, verbose)
		rgd_id_eq.update(id_temp_dict)

	elif str(d) == 'sp':
		acc_helper_dict = defaultdict(list)
		eq_name_dict, eq_id_dict = {}, {}	
		for term_id in d.get_values():
			uid = None
			name = d.get_label(term_id)
			dbrefs = d.get_xrefs(term_id)
			egids = [x for x in dbrefs if x.startswith('EGID:')]
			if len(egids) == 1:
				uid = entrez_eq.get(egids[0].replace('EGID:', ''))
			elif len(egids) > 1:
				uid = None
			elif len(egids) == 0:
				if len(dbrefs) > 1:
					uid = None
				elif len(dbrefs) == 1:
					prefix, xref = dbrefs.pop().split(':')
					if prefix == 'HGNC':	
						uid = hgnc_id_eq.get(xref)
					if prefix == 'MGI':
						uid = mgi_id_eq.get(xref)
					if prefix == 'RGD':
						uid = rgd_id_eq.get(xref)
									
			if uid is None:
				uid = uuid.uuid4()
			eq_name_dict[name] = uid
			eq_id_dict[term_id] = uid
			# build dictionary of  secondary accessions 
			# to identify those that map to multiple primary accessions/entry names
			accessions = d.get_alt_ids(term_id)
			for a in accessions:
				acc_helper_dict[a].append(term_id)	

		for sec_acc_id, v in acc_helper_dict.items():
			uid = None
		# only maps to one primary accession, same uuid
			if len(v) == 1:
				uid = eq_id_dict.get(v[0])
		# maps to > 1 primary accession, give it a new uuid.
			if uid is None:
				uid = uuid.uuid4()
			eq_id_dict[sec_acc_id] = uid
		if d.ids == True:
			write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
		if d.labels == True:
			write_beleq(eq_name_dict, d._name, d.source_file)
	
	elif str(d) == 'affx':
		affy_eq = {}
		if parsed.gene2acc_data is None or len(parsed.gene2acc_data._dict) == 0:
			print('Missing required dependency data gene2acc_data')
			refseq = {}
		else:
			refseq = build_refseq(parsed.gene2acc_data)

		ref_status = {'REVIEWED' : 0,
			  'VALIDATED' : 1,
			  'PROVISIONAL' : 2,
			  'PREDICTED' : 3,
			  'MODEL' : 4,
			  'INFERRED' : 5,
			  '-' : 6}

		for term_id in d.get_values():
			uid = None
			entrez_ids = d.get_xrefs(term_id)
			if entrez_ids:
				entrez_ids = [eid.replace('EGID:', '') for eid in entrez_ids]
			else: 
				entrez_ids = []
			# for 1 entrez mapping, use the entrez gene uuid
			if len(entrez_ids) == 1:
				uid = entrez_eq.get(entrez_ids.pop())
			# if > 1 entrez mapping, resolve to one, prioritizing by refseq status and lowest ID#.
			elif len(entrez_ids) > 1:
				adjacent_list = []
				for entrez_gene in entrez_ids:
					refstatus = refseq.get(entrez_gene)
					adjacent_list.append(ref_status.get(refstatus))
					# zipping yields a list of tuples like [('5307',0), ('104',2), ('3043',None)]
					# i.e. [(entrez_id, refseq_status)]
					list_of_tuples = list(zip(entrez_ids, adjacent_list))

					# get rid of all 'None' tuples (No entrez mapping)
					list_of_tuples = [tup for tup in list_of_tuples if tup[1] is not None]

					# no mapping
					if len(list_of_tuples) == 0:
						uid = None

					# multiple entrez, resolve by refseq status
					else:
						# min tuple is highest refseq status (0 the best)
						min_tuple = min(list_of_tuples, key=lambda x: x[1])
						min_refseq = min_tuple[1]
						lowest_tuples = []

						for item in list_of_tuples:
							if item[1] == min_refseq:
								lowest_tuples.append(item)

						# if mutiple genes with same refseq, resolve by lowest gene #
						target_tuple = min(lowest_tuples)
						uid = entrez_eq.get(target_tuple[0])
			# no entrez mapping, create a new uuid
			if uid == None:
				uid = uuid.uuid4()
			affy_eq[term_id] = uid
		write_beleq(affy_eq, d._name+'-ids', d.source_file) 

	elif str(d) == 'chebi':
		id_temp_dict, name_temp_dict = write_root_beleq(d, verbose)
		chebi_id_eq.update(id_temp_dict)

	elif str(d) == 'gobp':
		id_temp_dict, name_temp_dict = write_root_beleq(d, verbose)
		gobp_eq_dict.update(name_temp_dict)

	elif str(d) == 'gocc':
		id_temp_dict, name_temp_dict = write_root_beleq(d, verbose)
		gocc_eq_dict.update(id_temp_dict)
		gocc_names_eq.update(name_temp_dict)

	elif str(d) == 'do':
		id_temp_dict, name_temp_dict = write_root_beleq(d, verbose)
		do_id_eq.update(id_temp_dict)

	elif str(d) == 'sdis':
		resolve_xrefs(d, 'do', do_id_eq, verbose)

	elif str(d) == 'scomp':
		resolve_xrefs(d, 'gocc', gocc_eq_dict, verbose) 

	elif str(d) == 'schem':
		resolve_xrefs(d, 'chebi', chebi_id_eq, verbose)

	elif str(d) == 'meshpp':
		eq_name_dict = {}
		eq_id_dict = {}
		gobp_eq_cf = {k.casefold():v for k, v in gobp_eq_dict.items()}

		for term_id in d.get_values():
			uid = None
			# check MeSH synonyms for matches to GO
			name = d.get_label(term_id)
			synonyms = set()
			synonyms.add(name)
			synonyms.update(d.get_alt_names(term_id))
			for syn in synonyms:
				if syn.casefold() in gobp_eq_cf:
					uid = gobp_eq_cf.get(syn.casefold())
			if uid is None:
				uid = uuid.uuid4()
			eq_name_dict[name] = uid
			eq_id_dict[term_id] = uid
		if d.ids == True:
			write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
		if d.labels == True:
			write_beleq(eq_name_dict, d._name, d.source_file)

	elif str(d) == 'meshcs':
		eq_name_dict = {}
		eq_id_dict = {}
		gocc_eq_cf = {k.casefold():v for k, v in gocc_names_eq.items()}

		for term_id in d.get_values():
			uid = None
			# check MeSH synonyms for matches to GO
			name = d.get_label(term_id)
			synonyms = set()
			synonyms.add(name)
			synonyms.update(d.get_alt_names(term_id))
			for syn in synonyms:
				if syn.casefold() in gocc_eq_cf:
					uid = gocc_eq_cf.get(syn.casefold())
			if uid is None:
				uid = uuid.uuid4()
			eq_name_dict[name] = uid
			eq_id_dict[term_id] = uid
		if d.ids == True:
			write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
		if d.labels == True:
			write_beleq(eq_name_dict, d._name, d.source_file)

	elif str(d) == 'meshd':
		eq_name_dict = {}
		eq_id_dict = {}	
		do_data = parsed.do_data
		for term_id in d.get_values():
			name = d.get_label(term_id)
			xref = do_data.find_xref('MSH:'+term_id)
			if xref:
				uid = do_id_eq[xref]
			else:
				uid = uuid.uuid4()
			eq_name_dict[name] = uid
			eq_id_dict[term_id] = uid
		if d.ids == True:
			write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
		if d.labels == True:
			write_beleq(eq_name_dict, d._name, d.source_file)

	else:
		write_root_beleq(d, verbose)

def build_refseq(d):
	""" Uses parsed gene2acc file to build dict mapping (entrez_gene -> refseq status). """
	refseq = {}
	for entrez_gene, status, taxid in d.get_eq_values():
		target_pool = ['9606', '10116', '10090']
		valid_status = ['REVIEWED', 'VALIDATED', 'PROVISIONAL', 'PREDICTED',
						'MODEL', 'INFERRED']

		if taxid in target_pool and status in valid_status:
			refseq[entrez_gene] = status
	return refseq

def write_beleq(eq_dict, filename, source_file):
	""" Writes values and uuids from equivalence dictionary to .beleq file. """
	fullname = '.'.join((filename, 'beleq'))
	if len(eq_dict) == 0:
		print('	   WARNING: skipping writing ' + fullname + '; no equivalence data found.')
	else:
		with open(fullname, 'w') as f:
			# insert header chunk
			if os.path.exists('./templates/'+fullname):
				tf = open('./templates/'+fullname, encoding="utf-8")
				header = tf.read().rstrip()
				tf.close()
				# add Namespace and Author values
				header = get_citation_info(fullname, header, source_file)
			else:
				header = '[Values]'
			f.write(header+'\n')
			# write data
			for name, uid in sorted(eq_dict.items()):
				f.write('|'.join((name,str(uid))) + '\n')

def resolve_xrefs(d, root_prefix, root_eq_dict, verbose):
	""" Writes .beleq file for dataset d, given the prefix from the 'root' dataset
	and the (already built) equivalence dictionary from the root dataset. """
	count = 0
	eq_name_dict = {}
	eq_id_dict = {}
	prefix_string = root_prefix.upper() + ':'
	for term_id in d.get_values():
		label = d.get_label(term_id)
		uid = None
		xref_id = d.get_xrefs(term_id)
		xref_id = {i.replace(prefix_string,'') for i in xref_id if i.startswith(prefix_string)}
		if xref_id:
			if len(xref_id) == 1:
				count += 1
				xref_id = xref_id.pop()
				uid = root_eq_dict.get(xref_id)
		if uid is None:
			uid = uuid.uuid4()
		eq_name_dict[label] = uid
		eq_id_dict[term_id] = uid
		if d.get_alt_ids(term_id):
			for alt_id in d.get_alt_ids(term_id):
				eq_id_dict[alt_id] = uid
	if d.ids == True:
		write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
	if d.labels == True:
		write_beleq(eq_name_dict, d._name, d.source_file)
	if verbose:
		print('Able to resolve {0} {1} terms to {2}.'.format(str(count), d._name, root_prefix.upper()))
	return eq_id_dict	

def write_root_beleq(d, verbose):
	""" Writes .beleq file for data sets to be used as a 'root' or datasets
	that will not be equivalenced. Returns ID equivalence dictionary. """
	eq_name_dict = {}
	eq_id_dict = {}
	for term_id in d.get_values():
		name = d.get_label(term_id)
		uid = uuid.uuid4()
		eq_name_dict[name] = uid
		eq_id_dict[term_id] = uid
		if d.get_alt_ids(term_id):
			for alt_id in d.get_alt_ids(term_id):
				eq_id_dict[alt_id] = uid
	if d.ids == True:
		write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
	if d.labels == True:
		write_beleq(eq_name_dict, d._name, d.source_file)
	return eq_id_dict, eq_name_dict

def resolve_entrez_id(d, verbose):
	""" For HGNC, MGI, RGD, writes .beleq file(s) using equivalences 
	from Entrez Gene, stored in entrez_converter dictionary. Returns
	equivalence dictionaries. """
	prefix_string = d._prefix.upper() + ':'
	eq_name_dict = {}
	eq_id_dict = {}
	for term_id in d.get_values():
		uid = None
		name = d.get_label(term_id)
		entrez_id = entrez_converter.get(prefix_string + term_id)
		if entrez_id:
			uid = entrez_eq.get(entrez_id)
		if uid is None:
			uid = uuid.uuid4()
		eq_name_dict[name] = uid
		eq_id_dict[term_id] = uid
		if d.get_alt_ids(term_id):
			for alt_id in d.get_alt_ids(term_id):
				eq_id_dict[alt_id] = uid
	if d.ids == True:
		write_beleq(eq_id_dict, d._name + '-ids', d.source_file)
	if d.labels == True:
		write_beleq(eq_name_dict, d._name, d.source_file)
	return eq_id_dict, eq_name_dict
	
# vim: ts=4 sts=4 sw=4 noexpandtab
