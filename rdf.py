#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import pickle
import time
import datasets
from collections import defaultdict
from rdflib import URIRef, BNode, Literal, Namespace, Graph
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, OWL, XSD
from urllib import parse

namespace = Namespace("http://www.openbel.org/bel/namespace/")
belv = Namespace("http://www.openbel.org/vocabulary/")

# command line arguments - directory for pickled data objects
parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-n", required=True, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
parser.add_argument("-d", required=False, action='append', help="dataset by prefix; if none specified, all datasets in directory will be run")
args = parser.parse_args()
if os.path.exists(args.n):
    os.chdir(args.n)
else:
    print('data directory {0} not found!'.format(args.n))


# loads parsed data from pickle file (after running phase 2 of gp_baseline.py)
def make_rdf(d, g):
	''' Given namepsace data object d and graph g,
	adds to  namespace rdf graph. ''' 
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

def get_close_matches(concept_type, g):
	''' Given namespace concept type and graph, g, 
	searches graph for items of the given concept type and 
	identifies close matches based on case-insensitive string matching 
	of synonyms. Adds skos:closeMatch edges to graph. '''

	print('gathering string matches for {0}s ...'.format(concept_type))
	concept_dict = defaultdict(dict)
	for c in g.subjects(RDF.type, belv[concept_type]):
		labels = list(g.objects(c, SKOS["altLabel"]))
		labels.extend(g.objects(c, SKOS["prefLabel"]))
		labels = [l.casefold() for l in labels]
		scheme =  set(g.objects(c, SKOS["inScheme"])).pop()
		concept_dict[scheme][c] = set(labels)

#	concepts = list(sorted(concept_dict.keys()))
#	count = 0
#	while len(concepts) > 0:
#		concept = concepts.pop()
#		synonyms = concept_dict.pop(concept)
#		for concept2, synonyms2 in concept_dict.items():
#			if len(synonyms.intersection(synonyms2)) > 0:
#				g.add((concept, SKOS.closeMatch, concept2))
#				count += 1
	count = 0
	for scheme, concept_map in concept_dict.items():
		for concept, labels in concept_map.items():
			# iterate concept_dict a 2nd time, skipping items in same scheme
			for scheme2 in concept_dict.keys():
				if scheme2 == scheme:
					continue
				else:
					for concept2, labels2 in concept_dict[scheme2].items():
					#for concept2, labels2 in concept_map2.items():
						if len(labels.intersection(labels2)) > 0:
							g.add((concept, SKOS.closeMatch, concept2))
							count += 1 
	print('\tadded {0} closeMatches for {1}s'.format(count, concept_type))

if __name__=='__main__':	
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
				if isinstance(d, datasets.NamespaceDataSet) and args.d == None:
					make_rdf(d, g)
				elif isinstance(d, datasets.NamespaceDataSet) and d._prefix in args.d:
					make_rdf(d, g)

	get_close_matches('BiologicalProcessConcept', g)
	get_close_matches('AbundanceConcept', g)
	
	print('serializing RDF graph ...')
	g.serialize("testfile.ttl", format='turtle')	
