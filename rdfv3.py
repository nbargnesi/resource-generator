#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import parsed
import pickle
import time
import shutil
import annotate
from common import download
from constants import PARSER_TYPE, RES_LOCATION
import datasets
from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XSD
from urllib import parse

namespace = Namespace("http://www.openbel.org/bel/namespace/")
belv = Namespace("http://www.openbel.org/vocabulary/")

# command line arguments - directory for pickled data objects
parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
args = parser.parse_args()

if os.path.exists(args.n[0]):
    os.chdir(args.n[0])
else:
    print('data directory {0} not found!'.format(args.n[0]))


# loads parsed data from pickle file (after running phase 2 of gp_baseline.py)
def make_rdf(d, g):
	# build RDF and serialize
	# make namespace for data set (using data object attributes '_name' and '_prefix')
	n = Namespace("http://www.openbel.org/bel/namespace/" + d._name + '/')

	print('building RDF graph for {0} ...'.format(n))
	# bind namespace prefixes
	g.bind("skos", SKOS)
	g.bind("dcterms", DCTERMS)
	g.bind("belv", belv)
	g.bind(d._prefix, n)

	for term_id in d.get_values():
		term_clean = parse.quote(term_id)
		term_uri = URIRef(n[term_clean])
		# add primary identifier 
		g.add((term_uri, DCTERMS.identifier, Literal(term_id)))
		# add secondary/alternative identifiers (alt_ids)
		alt_ids = d.get_alt_ids(term_id)
		if alt_ids:
			for alt_id in alt_ids:
				g.add((term_uri, DCTERMS.identifier, Literal(alt_id)))

		# add official name (as title)
		name = d.get_name(term_id)
		if name:
			g.add((term_uri, DCTERMS.title, Literal(name)))

		# link to to Concept Scheme
		g.add((term_uri, SKOS.inScheme, namespace[d._name]))
		pref_label = d.get_label(term_id)
		if pref_label:
			g.add((term_uri, SKOS.prefLabel, Literal(pref_label)))

		# add species (tax id as literal)
		species = d.get_species(term_id)
		if species:
			g.add((term_uri, belv.fromSpecies, Literal(species)))

		# use encoding information to determine concept types
		encoding = d.get_encoding(term_id)
		if 'G' in encoding:
			g.add((term_uri, RDF.type, belv.GeneConcept))
		if 'R' in encoding:
			g.add((term_uri, RDF.type, belv.RNAConcept))
		if 'M' in encoding:
			g.add((term_uri, RDF.type, belv.MicroRNAConcept))
		if 'P' in encoding:
			g.add((term_uri, RDF.type, belv.ProteinConcept))
		if 'A' in encoding:
			g.add((term_uri, RDF.type, belv.AbundanceConcept))
		if 'B' in encoding:
			g.add((term_uri, RDF.type, belv.BiologicalProcessConcept))
		if 'C' in encoding:
			g.add((term_uri, RDF.type, belv.ComplexConcept))
		if 'O' in encoding:
			g.add((term_uri, RDF.type, belv.PathologyConcept))

		# get synonyms (alternative symbols and names)
		alt_symbols = d.get_alt_symbols(term_id)
		if alt_symbols:
			for symbol in alt_symbols:
				g.add((term_uri, SKOS.altLabel, Literal(symbol)))
		alt_names = d.get_alt_names(term_id)
		if alt_names:
			for name in alt_names:
				g.add((n[term_id], SKOS.altLabel, Literal(name)))

		# get equivalences to other namespaces (must be in data set)
		xrefs = d.get_xrefs(term_id)
		if xrefs:
			for x in xrefs:
				# xrefs are expected in format PREFIX:value
				if len(x.split(':')) == 2:
					prefix, value = x.split(':')
					# NOTE - only xrefs with prefixes that match namespaces in the data set will be used	
					if prefix.lower() in prefix_dict:
						xrefns = Namespace("http://www.openbel.org/bel/namespace/" + prefix_dict[prefix.lower()] + '/') 		
						g.bind(prefix.lower(), xrefns)
						xref_uri = URIRef(xrefns[value])
						g.add((term_uri, SKOS.exactMatch, xref_uri))

	
g = Graph()

# build dictionary of namespace prefixes to names (from dataset objects)
print('gathering namespace information ...')
prefix_dict = {}
for files in os.listdir("."):
	if files.endswith("parsed_data.pickle"):
		with open(files, 'rb') as f:
			d = pickle.load(f)
		if isinstance(d, datasets.NamespaceDataSet):
			prefix_dict[d._prefix] = d._name
			print('\t{0} - {1}'.format(d._prefix, d._name))
	
for files in os.listdir("."):
	if files.endswith("parsed_data.pickle"):
		with open(files,'rb') as f:
			d = pickle.load(f)
			if isinstance(d, datasets.NamespaceDataSet):
				make_rdf(d, g)
print('serializing RDF graph ...')
g.serialize("testfile.ttl", format='turtle')	
