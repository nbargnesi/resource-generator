#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import pickle
import time
import datasets
import bel_functions
from collections import defaultdict

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

	data_list = ['rgd', 'hgnc', 'rgd_ortho', 'mgi']
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
						o_label = data_dict.get('hgnc').get_label(value)
					if prefix == 'MGI':
						o_label = data_dict.get('mgi').get_label(value)
					if o_label is None:
						print('WARNING - {2} missing label for {0}, {1}'.format(prefix, value, rgd_term))
						continue
					ortho_term = bel_functions.bel_term(o_label, prefix, 'g')
					rgd_ortho_statements.add('{0} orthologous {1}'.format(rgd_term, ortho_term)) 

	with open('gene-orthology.bel', 'w') as ortho:
		ortho.write('SET Citation = {"Online Resource", "HUGO Gene Nomenclature Committee data download", "ftp://ftp.ebi.ac.uk/pub/databases/genenames/hgnc_complete_set.txt.gz"}\n')
		for s in sorted(hgnc_ortho_statements):
			ortho.write(s + '\n')
		ortho.write('\n')
		ortho.write('SET Citation = {"Online Resource","RGD Orthology FTP file", "ftp://rgd.mcw.edu/pub/data_release/RGD_ORTHOLOGS.txt"}\n')
		for s in sorted(rgd_ortho_statements):
			ortho.write(s + '\n')
# vim: ts=4 sts=4 sw=4 noexpandtab
