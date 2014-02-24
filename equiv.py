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
from collections import deque, defaultdict
from common import get_citation_info

entrez_converter = {}
entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}
sp_acc_eq = {}
affy_eq = {}
refseq = {}
chebi_id_eq = {}
chebi_name_eq = {}
pub_eq_dict = {}
gobp_eq_dict = {}
gobp_id_eq = {}
gocc_eq_dict = {}
gocc_names_eq = {}
do_eq_dict = {}
do_id_eq = {}
schem_eq = {}
sdis_eq = {}
mesh_cl_eq = {}
mesh_d_eq = {}
mesh_pp_eq = {}

def equiv(d, verbose):
	if str(d) == 'egid':
		for term_id in d.get_values():
			uid = uuid.uuid4()
			entrez_eq[term_id] = uid
		write_beleq(entrez_eq, 'entrez-gene-ids')
		# Make entrez_converter equivalence dictionary for Entrez to HGNC, MGI, RGD
		target = ('HGNC:', 'MGI:', 'RGD:')
		for term_id in d.get_values():
			dbXrefs = d.get_xrefs(term_id)
			for dbXref in dbXrefs:
				entrez_converter[dbXref] = term_id

	elif str(d) == 'hgnc':
		for term_id in d.get_values():
			entrez_id = entrez_converter.get('HGNC:'+term_id)
			if entrez_id is None:
				uid = uuid.uuid4()
			else:
				# use the entrez uuid
				uid = entrez_eq.get(entrez_id)
			hgnc_eq[d.get_label(term_id)] = uid
		write_beleq(hgnc_eq, d._name)

	elif str(d) == 'mgi':
		for term_id in d.get_values():
			entrez_id = entrez_converter.get('MGI:'+term_id)
			if entrez_id is None:
				uid = uuid.uuid4()
			else:
				# use the entrez uuid
				uid = entrez_eq.get(entrez_id)
			mgi_eq[d.get_label(term_id)] = uid
		write_beleq(mgi_eq, d._name)	   

	elif str(d) == 'rgd':
		for term_id in d.get_values():
			entrez_id = entrez_converter.get('RGD:'+term_id)
			if entrez_id is None:
				uid = uuid.uuid4()
			else:
				# use the entrez uuid
				uid = entrez_eq.get(entrez_id)
			rgd_eq[d.get_label(term_id)] = uid
		write_beleq(rgd_eq, d._name)		

	elif str(d) == 'sp':
		#check for dependencies
		if parsed.hgnc_data == None or len(parsed.hgnc_data._dict) == 0:
			print('Missing required dependency data hgnc_data')
		if parsed.mgi_data == None or len(parsed.mgi_data._dict) == 0:
			print('Missing required dependency data mgi_data')
		if parsed.rgd_data == None or len(parsed.rgd_data._dict) == 0:
			print('Missing required dependency data rgd_data')
		acc_helper_dict = defaultdict(list)
		for term_id in d.get_values():
			uid = None
			gene_ids = []
			other_ids = []
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
						hgnc_key = parsed.hgnc_data.get_label(xref)
						uid = hgnc_eq.get(hgnc_key)
					if prefix == 'MGI':
						mgi_key = parsed.mgi_data.get_label(xref)
						uid = mgi_eq.get(mgi_key)
					if prefix == 'RGD':
						rgd_key = parsed.rgd_data.get_label(xref)
						uid = rgd_eq.get(rgd_key)
									
			if uid is None:
				uid = uuid.uuid4()
			sp_eq[name] = uid
			sp_acc_eq[term_id] = uid
			# build dictionary of  secondary accessions 
			# to identify those that map to multiple primary accessions/entry names
			accessions = d.get_alt_ids(term_id)
			for a in accessions:
				acc_helper_dict[a].append(term_id)	

		for sec_acc_id, v in acc_helper_dict.items():
		# only maps to one primary accession, same uuid
			if len(v) == 1:
				uid = sp_acc_eq.get(v[0])
		# maps to > 1 primary accession, give it a new uuid.
			else:
				uid = uuid.uuid4()
			sp_acc_eq[sec_acc_id] = uid
		write_beleq(sp_eq, d._name)
		write_beleq(sp_acc_eq, d._name+'-ids')
	
	elif str(d) == 'affx':
		if parsed.gene2acc_data is None or if len(parsed.gene2acc_data._dict == 0):
			print('Missing required dependency data gene2acc_data')

		ref_status = {'REVIEWED' : 0,
			  'VALIDATED' : 1,
			  'PROVISIONAL' : 2,
			  'PREDICTED' : 3,
			  'MODEL' : 4,
			  'INFERRED' : 5,
			  '-' : 6}

		refseq = build_refseq(parsed.gene2acc_data)
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
		write_beleq(affy_eq, d._name+'-ids') 

	elif str(d) == 'chebi':
		for term_id in d.get_values():
			uid = uuid.uuid4()
			chebi_id_eq[term_id] = uid
			for alt_id in d.get_alt_ids(term_id):
				chebi_id_eq[alt_id] = uid
			name = d.get_label(term_id)
			chebi_name_eq[name] = uid
		write_beleq(chebi_name_eq,d._name)
		write_beleq(chebi_id_eq,d._name+'-ids')

	elif str(d) == 'gobp':
		for term_id in d.get_values():
			uid = uuid.uuid4()
			term_name = d.get_label(term_id)
			alt_ids = d.get_alt_ids(term_id)
			gobp_eq_dict[term_name] = uid
			gobp_id_eq[term_id] = uid
			if alt_ids:
				for i in alt_ids:
					gobp_id_eq[i] = uid
		write_beleq(gobp_eq_dict, d._name)
		write_beleq(gobp_id_eq, d._name+'-ids')

	elif str(d) == 'gocc':
		for term_id in d.get_values():
			uid = uuid.uuid4()
			term_name = d.get_label(term_id)
			alt_ids = d.get_alt_ids(term_id)
			gocc_names_eq[term_name] = uid
			gocc_eq_dict[term_id] = uid
			if alt_ids:
				for i in alt_ids:
					gocc_eq_dict[i] = uid
		write_beleq(gocc_names_eq, d._name)
		write_beleq(gocc_eq_dict, d._name+'-ids')

	elif str(d) == 'do':
		# assign DO a new uuid and use as the primary for diseases
		for term_id in d.get_values():
			uid = uuid.uuid4()
			name = d.get_label(term_id)
			do_eq_dict[name] = uid
			do_id_eq[term_id] = uid
		write_beleq(do_eq_dict, d._name)
		write_beleq(do_id_eq, d._name + '-ids')

	elif str(d) == 'sdis':
		sdis_to_do = parsed.sdis_to_do_data
		# map to disease ontology using mapping  file sdis_to_do
		count = 0
		for entry in d.get_values():
			do_id = sdis_to_do.get_equivalence(entry)
			if do_id:
				count = count + 1
				uid = do_id_eq.get(do_id)
			else:
				uid = uuid.uuid4()
			sdis_eq[entry] = uid
		write_beleq(sdis_eq, d._name)
		if verbose:
			print('Able to resolve ' +str(count)+ ' legacy disease terms to DO.')

	elif str(d) == 'scomp':
		# Selventa named complexes (human) - equivalence to GOCC using manually generated .csv mapping file
		ctg = parsed.ctg_data
		count = 0
		nch_eq = {}
		for entry in d.get_values():
			go_id = ctg.get_equivalence(entry)
			if go_id:
				count += 1
				uid = gocc_eq_dict.get(go_id)
			else:
				uid = uuid.uuid4()
			nch_eq[entry] = uid
		write_beleq(nch_eq,d._name)
		if verbose:
			print('Able to resolve {0} Selventa named complexes to GOCC'.format(str(count)))
 
	elif str(d) == 'schem':
		# try to resolve schem terms to CHEBI. If there is not one,
		# assign a new uuid.
		count = 0
		#schem_to_chebi = parsed.load_data('schem_to_chebi')
		schem_to_chebi = parsed.schem_to_chebi_data
		for term in d.get_values():
			chebi_id = schem_to_chebi.get_equivalence(term)
			if chebi_id:
				count = count + 1
				uid = chebi_id_eq.get(chebi_id)
				if uid is None:
					uid = uuid.uuid4()
			else:
				uid = uuid.uuid4()
			schem_eq[term] = uid
		write_beleq(schem_eq,d._name)
		if verbose:
			print('Able to resolve ' +str(count)+ ' legacy chemical terms to CHEBI.')

	elif str(d) == 'meshpp':

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
			mesh_pp_eq[name] = uid
		write_beleq(mesh_pp_eq,d._name)

	elif str(d) == 'meshcl':

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
			mesh_cl_eq[name] = uid
		write_beleq(mesh_cl_eq,d._name)

	elif str(d) == 'meshd':

		#do_data = parsed.load_data('do')
		do_data = parsed.do_data
		for term_id in d.get_values():
			name = d.get_label(term_id)
			xref = do_data.find_xref('MSH:'+term_id)
			if xref:
				uid = do_id_eq[xref]
			else:
				uid = uuid.uuid4()
			mesh_d_eq[name] = uid
		write_beleq(mesh_d_eq, d._name)

	else:
		# if data set not handled above, generate new uuid for each term/name
		# and write .beleq file(s) as directed by d.ids and d.labels
		eq_name_dict = {}
		eq_id_dict = {}
		for term_id in d.get_values():
			name = d.get_label(term_id)
			uid = uuid.uuid4()
			eq_name_dict[term_id] = uid
			eq_id_dict[term_id] = uid
		if d.ids is True:
			write_beleq(eq_id_dict, d._name)
		if d.labels is True:
			write_beleq(eq_name_dict, d._name)

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

def write_beleq(eq_dict, filename):
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
				header = get_citation_info(fullname, header)
			else:
				header = '[Values]'
			f.write(header+'\n')
			# write data
			for name, uid in sorted(eq_dict.items()):
				f.write('|'.join((name,str(uid))) + '\n')
