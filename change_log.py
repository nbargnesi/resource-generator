#!/usr/bin/env python3
# coding: utf-8

'''
change_log.py

Compares "old" and "new" sets of pickled namespace data objects (output by gp_baseline) 
to track ID and label changes between namespace versions. Uses IDs and history, where
available to provide updated labels and ids (or "withdrawn" status) for namespace values
lost between the "old" and "new" versions.

inputs:
	-n directory for "new" set of pickled namespace data objects
	-o directory for "old" set of pickled namespace data objects

outputs: 
	change_log.json	json file to be used with bel.rb upgrade script

'''

import argparse
import os
import pickle
import time
import datasets
import json

# mapping of anno data set names to .belanno file names
# do not currently match
anno_match = True # use dict annotation_name_to_file to remap anno dataset names to belanno file names
annotation_name_to_file = {
		'uberon':'anatomy',
		'disease-ontology':'disease',
		'cell-line-ontology':'cell-line',
		'experimental-factor-ontology':'cell-line',
		'cell-ontology':'cell',
		'mesh-cellular-structures':'cell-structure',
		'ncbi-taxonomy':'species-taxonomy-id'
		}

def get_info(directory):
	''' Get set of namespace and annotation prefixes (from data set objects).
	data set objects include information about whether label and/or names are used
	in .belns files and whether the data set is for namespace values and/or annotations.'''
	print('gathering information from data pickle files...')
	prefixes = set()
	ns_dict = {}
	anno_dict = {}
	cwd = os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
	for files in os.listdir("."):
		if files.endswith("parsed_data.pickle"):
			with open(files, 'rb') as f:
				d = pickle.load(f)
			if not isinstance(d, datasets.NamespaceDataSet):
				continue
			if 'anno' in d.scheme_type:
				if anno_match:
					try:
						name = annotation_name_to_file[d._name]
					except:
						name = d._name
				else:
					name = d._name
				name = name + '.belanno'
				prefix = d._prefix.upper()
				prefixes.add(prefix)
				anno_dict[prefix] = name
			if 'ns' in d.scheme_type:
				if d.ids:
					id_name = d._name + '-ids.belns'
					id_prefix = d._prefix.upper() + 'ID'
					id_prefix = id_prefix.replace('IDID','ID') # catch EGID exception
					id_prefix = id_prefix.replace('AFFXID', 'AFFX') # catch AFFX exception
					prefixes.add(id_prefix)
					ns_dict[id_prefix] = id_name
				if d.labels:
					label_name = d._name + '.belns'
					label_prefix = d._prefix.upper()
					prefixes.add(label_prefix)
					ns_dict[label_prefix] = label_name
	os.chdir(cwd)
	return prefixes, ns_dict, anno_dict

def get_ns_data(directory):
	cwd = os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
	else:
		print('data directory {0} not found!'.format(directory))
		return None

	ns_dict = {}
	print('Gathering info for {0}'.format(directory))
	for files in os.listdir("."):
		if files.endswith("parsed_data.pickle"):
			with open(files, 'rb') as f:
				d = pickle.load(f)
			if isinstance(d, datasets.NamespaceDataSet):
				ns_dict[d._prefix] = {}
				print('\t{0} - {1}'.format(d._prefix, d._name))
				for term_id in d.get_values():
					name = d.get_label(term_id)
					ns_dict[d._prefix][term_id] = name
					if directory == args.n: #get alt_id information ONLY for new namespace
						if d.get_alt_ids(term_id):
							for alt_id in d.get_alt_ids(term_id):
								ns_dict[d._prefix][alt_id] = name
	os.chdir(cwd)
	return ns_dict
					
def get_history_data(directory):
	cwd = os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
	else:
		print('data directory {0} not found!'.format(directory))
		return None

	history_dict = {}
	print('Gathering history info for {0}'.format(directory))
	for files in os.listdir("."):
		if files.endswith("parsed_data.pickle"):
			with open(files, 'rb') as f:
				d = pickle.load(f)
			if isinstance(d, datasets.HistoryDataSet):
				history_dict[d._prefix] = d.get_obsolete_ids()
				print('\t{0}'.format(d._prefix))
				
	os.chdir(cwd)
	return history_dict
		

if __name__=='__main__':	
	# command line arguments - directory for pickled data objects
	parser = argparse.ArgumentParser(description="""replacement for track changes.
	.""")

	parser.add_argument("-n", required=True, metavar="NEWDIRECTORY",
					help="directory with new resource data")
	parser.add_argument("-o", required=True, metavar="OLDDIRECTORY",
					help="directory with old resource data")
	parser.add_argument("--new_version", metavar="NEWVERSION", default="testing",
					help="version for new resource data")
	parser.add_argument("--old_version", metavar="OLDVERSION", default="latest-release",
					help="version for old resource data")
	parser.add_argument("--base_url", metavar="BASEURL", default="http://resource.belframework.org/belframework/",
					help="base url for belns and belanno files")
	args = parser.parse_args()
	

	old_ns_dict = get_ns_data(args.o)
	new_ns_dict = get_ns_data(args.n)
	history_dict = get_history_data(args.n)
	prefixes, ns_info, anno_info = get_info(args.n)
	change_log = {}
	redefine = {}
	redefine['namespaces'] = {}
	redefine['annotations'] = {}
	for prefix, filename in ns_info.items():
		redefine['namespaces'][prefix] = {
			'old_url':args.base_url + args.old_version + '/namespace/' + filename,
			'new_url':args.base_url + args.new_version + '/namespace/' + filename,
			'new_keyword':prefix}
	for prefix, filename in anno_info.items():
		redefine['annotations'][prefix] = {
			'old_url':args.base_url + args.old_version + '/annotation/' + filename,
			'new_url':args.base_url + args.new_version + '/annotation/' + filename,
			'new_keyword':prefix}
	change_log['redefine'] = redefine	


	for prefix in old_ns_dict.keys():
		label_prefix = prefix.upper()
		if prefix.endswith('id'):
			id_prefix = prefix.upper()
		else:
			id_prefix = prefix.upper() + 'ID'
		label_log = None
		id_log = None	
		if prefix not in new_ns_dict.keys():
			print("WARNING - Namespace {0} missing from new data".format(prefix))
			continue
		else:
			if id_prefix in prefixes:
				change_log[id_prefix] = {}
				id_log = change_log.get(id_prefix)
			if label_prefix in prefixes:
				change_log[label_prefix] = {}
				label_log = change_log.get(label_prefix)
			for term_id, label in old_ns_dict[prefix].items():
				new_id_value = None
				new_label_value = None
				# handle case where label changes, but ID is same
				if term_id in new_ns_dict[prefix]:
					new_label_value = new_ns_dict[prefix].get(term_id)
					new_id_value = term_id
				# handle cases where ID changes and/or is withdrawn
				else: 
					# handle case where label does not change but ID does?
					# create warning, but do not designate label as 'withdrawn'
					if label in new_ns_dict[prefix].values():
						new_label_value = label
						print('WARNING! Label {0} appears valid but is associated with withdrawn/unresolved ID {1}:{2}'.format(label,label_prefix,term_id))
					if history_dict.get(prefix) and term_id in history_dict[prefix]:
						new_id_value = history_dict.get(prefix).get(term_id)
						if new_id_value is None:
							new_id_value = 'unresolved'
						elif new_id_value == 'withdrawn':
							pass
						elif new_id_value not in new_ns_dict[prefix].keys(): #confirm new_id_value is valid
							new_id_value = 'unresolved'
						else: # if valid new_id_value from history
							new_label_value = new_ns_dict.get(prefix).get(new_id_value)

					else:
						new_id_value = 'unresolved'

				if new_label_value is None:
					if new_id_value == 'withdrawn':
						new_label_value = 'withdrawn'
					else:	
						new_label_value = 'unresolved'


				# add data to change_log
				if new_label_value != label and label_log is not None:
					label_log[label] = new_label_value
				if new_id_value != term_id and id_log is not None:
					id_log[term_id] = new_id_value
							
	with open('change_log.json', 'w') as f:
		json.dump(change_log, f, sort_keys=True, indent=4, separators=(', ', ':'))
# vim: ts=4 sts=4 sw=4 noexpandtab
