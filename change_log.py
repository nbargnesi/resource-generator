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

def get_prefixes(directory):
	''' Get set of namespace prefixes for belns files (from data set objects). '''
	print('gathering namespace information ...')
	prefixes = set()
	cwd = os.getcwd()
	if os.path.exists(directory):
		os.chdir(directory)
	for files in os.listdir("."):
		if files.endswith("parsed_data.pickle"):
			with open(files, 'rb') as f:
				d = pickle.load(f)
			if isinstance(d, datasets.NamespaceDataSet):
				if d.ids:
					prefixes.add(d._prefix.upper() + 'ID')
				if d.labels:
					prefixes.add(d._prefix.upper())
	os.chdir(cwd)
	return prefixes

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
					help="directory with new namespace equivalence data")
	parser.add_argument("-o", required=True, metavar="OLDDIRECTORY",
					help="directory with old namespace equivalence data")
	args = parser.parse_args()
	
	old_ns_dict = get_ns_data(args.o)
	new_ns_dict = get_ns_data(args.n)
	history_dict = get_history_data(args.n)
	prefixes = get_prefixes(args.n)
	change_log = {}

	for prefix in old_ns_dict.keys():
		label_prefix = prefix.upper()
		id_prefix = prefix.upper() + 'ID'
		label_log = {}
		id_log = {}	
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
				# handle case where label changes, but ID is same
				if term_id in new_ns_dict[prefix]:
					new_label_value = new_ns_dict[prefix].get(term_id)
					new_id_value = term_id
				# handle case where ID changes (and presumably label)
				else:
					if history_dict.get(prefix) and term_id in history_dict[prefix]:
						new_id_value = history_dict.get(prefix).get(term_id)
						if new_id_value == 'withdrawn':
							new_label_value = 'withdrawn'
						elif new_id_value == None:
							new_label_value = 'unresolved'
						else:
							try:
								new_label_value = new_ns_dict.get(prefix).get(new_id_value)
							except:
								print('No label found for {0}:{1}'.format(prefix.upper(),new_id_value))
								new_label_value = 'unresolved'
					else:
						new_id_value = 'unresolved'
						new_label_value = 'unresolved'

				# add data to change_log
				if new_label_value != label and label_log is not None:
					label_log[label] = new_label_value
				if new_id_value != term_id and id_log is not None:
					id_log[term_id] = new_id_value
							
	with open('change_log.json', 'w') as f:
		json.dump(change_log, f, sort_keys=True, indent=4, separators=(', ', ':'))
# vim: ts=4 sts=4 sw=4 noexpandtab
