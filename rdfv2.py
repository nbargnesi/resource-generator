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

parser = argparse.ArgumentParser(description="""Generate namespace and equivalence files
for gene/protein datasets.""")

parser.add_argument("-n", required=True, nargs=1, metavar="DIRECTORY",
					help="directory to store the new namespace equivalence data")
parser.add_argument("-d", required=True, type=str, 
					help="dataset name")
#parser.add_argument("-o", default='symbols', choices=['symbols', 'names', 'data','rdf'], help="output")
#parser.add_argument("-o", required=True, nargs=1, type=str, help="output file name")
args = parser.parse_args()

dataset = args.d
#output_file = args.o
if os.path.exists(args.n[0]):
    os.chdir(args.n[0])
else:
    print('data directory {0} not found!'.format(args.n[0]))

# loads parsed data from pickle file (after running phase 2 of gp_baseline.py)
if not os.path.exists(dataset+'.parsed_data.pickle'):
    print('WARNING !!! Required pickled data file %s not found.' % (dataset+'.parsed_data.pickle'))
else:
    with open(dataset+'.parsed_data.pickle', 'rb') as f:
        d = pickle.load(f)

# build RDF and serialize
print('building RDF graph ...')
namespace = Namespace("http://www.selventa.com/bel/namespace/")
belv = Namespace("http://www.selventa.com/vocabulary/")
g = Graph()

# make namespace for data set (using class attribute 'N'
n = Namespace("http://www.selventa.com/bel/namespace/" + d.N + '/')

# bind namespace prefixes
g.bind("skos", SKOS)
g.bind("dcterms", DCTERMS)
g.bind("belv", belv)
g.bind(d.N, n)

for term_id in d.get_values():
	term_clean = parse.quote(term_id)
	term_uri = URIRef(n[term_clean])
	# add primary identifier (may need to add/update for cases with alt ids)
	g.add((term_uri, DCTERMS.identifier, Literal(term_id)))
	# add alt ids
	alt_ids = d.get_alt_ids(term_id)
	if alt_ids:
		for alt_id in alt_ids:
			g.add((term_uri, DCTERMS.identifier, Literal(alt_id)))
	# add official name (as title - make general)
	name = d.get_name(term_id)
	if name:
		g.add((term_uri, DCTERMS.title, Literal(name)))
	# map to Concept Scheme
	g.add((term_uri, SKOS.inScheme, namespace[d.N]))
	# for EntrezGene, use Gene ID as prefLabel?
	# need to return pref label! make function?
	pref_label = d.get_label(term_id)
	if pref_label:
		g.add((term_uri, SKOS.prefLabel, Literal(pref_label)))
	# add species - make method for data set?
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

	# get synonyms (symbols and names)
	alt_symbols = d.get_alt_symbols(term_id)
	if alt_symbols:
		for symbol in alt_symbols:
			g.add((term_uri, SKOS.altLabel, Literal(symbol)))
	alt_names = d.get_alt_names(term_id)
	if alt_names:
		for name in alt_names:
			g.add((n[term_id], SKOS.altLabel, Literal(name)))
#with open(output_file, 'w') as f:
print('serializing RDF graph ...')
g.serialize("testfile.ttl", format='turtle')	
#g.serialize(destination=output_file, format='turtle')	
