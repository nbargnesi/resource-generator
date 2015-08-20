#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import pickle
import datetime
import datasets
import bel_functions
from collections import defaultdict

# Info for BEL document header
doc_name = "BEL Framework Orthologous Genes Document"
description = "Gene orthology relationships from HGNC, RGD, and Homologene"
namespaces = {'HGNC': 'hgnc-human-genes.belns',
	'MGI': 'mgi-mouse-genes.belns',
	'RGD': 'rgd-rat-genes.belns',
	'EGID': 'entrez-gene-ids.belns'}
annotations = {}
base_url = 'http://resource.belframework.org/belframework/testing/'


if __name__=='__main__':	
	# command line arguments - directory for pickled data objects
	parser = argparse.ArgumentParser(description="""Generate BEL orthology file
	from pickled data objects.""")

	parser.add_argument("-n", required=True, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
	args = parser.parse_args()
	if os.path.exists(args.n):
		os.chdir(args.n)
	else:
		print('data directory {0} not found!'.format(args.n))

	# access and load required data objects
	data_list = ['rgd', 'hgnc', 'rgd_ortho', 'mgi', 'egid_ortho']
	data_dict = {}
	for files in os.listdir("."):
		if files.endswith("parsed_data.pickle"):
			with open(files,'rb') as f:
				d = pickle.load(f)
				if str(d) in data_list:
					data_dict[str(d)] = d
	for data in data_list:
		if data not in data_dict.keys():
			print('missing required dependency {0}!'.format(data))

	# Get ortho statements from HGNC data object
	# MGI and RGD namespaceDataSet objects are required for translation of MGI and RGD Ids to labels
	hgnc_ortho_statements = set()
	for term_id in data_dict.get('hgnc').get_values():
		term_label = data_dict.get('hgnc').get_label(term_id)
		hgnc_term = bel_functions.bel_term(term_label, 'HGNC', 'g')
		orthos = data_dict.get('hgnc').get_orthologs(term_id)
		if orthos is not None:
			for o in orthos:
				if len(o.split(':')) == 2:
					prefix, value = o.split(':')
					if prefix == 'RGD':
						o_label = data_dict.get('rgd').get_label(value)
					if prefix == 'MGI':
						o_label = data_dict.get('mgi').get_label(value)
					if o_label is None:
						print('WARNING - missing label for {0}, {1}'.format(prefix, value))
						continue
					ortho_term = bel_functions.bel_term(o_label, prefix, 'g')
					hgnc_ortho_statements.add('{0} orthologous {1}'.format(hgnc_term, ortho_term)) 
		
	# Get ortho statements from RGD data object (Rat to Mouse only)
	# requires HGNC and MGI Namespace DataSet onjects to translate HGNC and MGI Ids to labels	
	rgd_ortho_statements = set()	
	for term_id in data_dict.get('rgd_ortho').get_values():
		term_label = data_dict.get('rgd').get_label(term_id)
		rgd_term = bel_functions.bel_term(term_label, 'RGD', 'g')
		orthos = data_dict.get('rgd_ortho').get_orthologs(term_id)
		if orthos is not None:
			for o in orthos:
				prefix = ''
				if len(o.split(':')) == 2:
					prefix, value = o.split(':')
					if prefix == 'HGNC':
						#o_label = data_dict.get('hgnc').get_label(value)
						continue
					elif prefix == 'MGI':
						o_label = data_dict.get('mgi').get_label(value)
					if o_label is None:
						print('WARNING - {2} missing label for {0}, {1}'.format(prefix, value, rgd_term))
						continue
					ortho_term = bel_functions.bel_term(o_label, prefix, 'g')
					rgd_ortho_statements.add('{0} orthologous {1}'.format(rgd_term, ortho_term)) 

	# Get ortho statements from Homologene (egid_ortho) data object 
	egid_ortho_statements = set()	
	for term_id in data_dict.get('egid_ortho').get_values():
		term_label = term_id
		egid_term = bel_functions.bel_term(term_label, 'EGID', 'g')
		orthos = data_dict.get('egid_ortho').get_orthologs(term_id)
		print(orthos)
		if orthos is not None:
			for o in orthos:
				prefix = ''
				if len(o.split(':')) == 2:
					prefix, value = o.split(':')
					ortho_term = bel_functions.bel_term(value, prefix, 'g')
					egid_ortho_statements.add('{0} orthologous {1}'.format(egid_term, ortho_term)) 

	with open('gene-orthology.bel', 'w') as ortho:
		bel_functions.write_bel_header(ortho, doc_name=doc_name, description=description, namespaces=namespaces, annotations=annotations, base_url=base_url)
		ortho.write('SET Citation = {"Online Resource", "HUGO Gene Nomenclature Committee data download", "ftp://ftp.ebi.ac.uk/pub/databases/genenames/hgnc_complete_set.txt.gz"}\n')
		for s in sorted(hgnc_ortho_statements):
			ortho.write(s + '\n')
		ortho.write('\n')
		ortho.write('SET Citation = {"Online Resource","RGD Orthology FTP file", "ftp://rgd.mcw.edu/pub/data_release/RGD_ORTHOLOGS.txt"}\n')
		for s in sorted(rgd_ortho_statements):
			ortho.write(s + '\n')
		ortho.write('\n')
		ortho.write('SET Citation = {"Online Resource","NCBI Homologene FTP file", "ftp://ftp.ncbi.nih.gov/pub/HomoloGene/current"}\n')
		for s in sorted(egid_ortho_statements):
			ortho.write(s + '\n')
# vim: ts=4 sts=4 sw=4 noexpandtab
