#!/usr/bin/env python3.3
import urllib.request
import datetime
from string import Template
from bel_functions import bel_term

""" Generates Gene Scaffolding BEL script document used in Phase III.
Given the urls for gene/protein domain .belns files, uses the 
encodings to generate transcribedTo and translatedTo BEL statements. """

namespaces = {'HGNC': 'http://resource.belframework.org/belframework/testing/namespace/hgnc-approved-symbols.belns',
		'MGI': 'http://resource.belframework.org/belframework/testing/namespace/mgi-approved-symbols.belns',
		'RGD': 'http://resource.belframework.org/belframework/testing/namespace/rgd-approved-symbols.belns'}

output_file = 'gene_scaffolding_document_9606_10090_10116.bel'


def translated_to(value,ns):
	""" Create bel translatedTo statement, given 
	namespace keyword string and value. """
	source = bel_term(value, ns, 'r')
	target = bel_term(value, ns, 'p')
	s = Template('${source} translatedTo ${target}').substitute(source=source, target=target)
	return s

def transcribed_to(value,ns):
	""" Create bel transcribedTo statement, given
	namespace keyword string and value. """
	source = bel_term(value, ns, 'g')
	target = bel_term(value, ns, 'r')
	s = Template('${source} transcribedTo ${target}').substitute(source=source, target=target)
	return s

def micro_rna(value,ns):
	""" Create bel transcribedTo statement for microRNA,
	given namespace keyword string and value. """
	source = bel_term(value, ns, 'g')
	target = bel_term(value, ns, 'm')
	s = Template('${source} transcribedTo ${target}').substitute(source=source, target=target)
	return s

def scaffold(belns_url):
	""" Returns set of gene scaffolding statements from .belns url, 
	along with species, name, and date values needed for annotations. """
	field = ''
	belns = urllib.request.urlopen(url)
	statements = set()
	for line in belns:
		line = line.decode('ISO-8859-1')
		if not line.strip():
			continue
		if line.startswith('['):
			field = line.strip()
			continue
		elif '[Namespace]' in field:
			if line.startswith('SpeciesString='):
				species = line.split('=')[1].strip()
			elif line.startswith('NameString='):
				name = line.split('=')[1].strip()
			elif line.startswith('CreatedDateTime'):
				date = line.split('=')[1].strip()
		elif '[Values]' in field:
			(value, encoding) = line.split('|')
			encoding = encoding.strip()
			if encoding == 'G':
				continue
			elif encoding == 'GR':
				statements.add(transcribed_to(value, ns))
			elif encoding == 'GRM':
				statements.add(micro_rna(value, ns))
			elif encoding == 'GRP':
				statements.add(transcribed_to(value, ns))
				statements.add(translated_to(value, ns))
	return statements, name, species, date

annotations = {'Species': 'http://resource.belframework.org/belframework/testing/annotation/species-taxonomy-id.belanno'}
today = datetime.date.today()
version = str(today.year) + str(today.month) + str(today.day)

separator = '#' * 50

with open(output_file, 'w') as bel:
	print('\nWriting file {0} ...'.format(output_file))
	bel.write(separator)
	bel.write('\n# Document Properties Section\n')
	bel.write('SET DOCUMENT Name = "Phase III Gene Scaffolding"\n')
	bel.write('SET DOCUMENT Description = "Gene scaffolding for use with the BEL compiler."\n')
	bel.write('SET DOCUMENT Version = "{0}"\n'.format(version))
	bel.write('SET DOCUMENT Copyright = "Copyright (c) {0}, OpenBEL Project. This work is licensed under a Creative Commons Attribution 3.0 Unported License."\n'.format(str(today.year)))
	bel.write('SET DOCUMENT Authors = "OpenBEL"\n')
	bel.write('\n'+separator+ '\n')
	bel.write('# Definitions Section\n')
	for ns, url in namespaces.items():
		bel.write('DEFINE NAMESPACE {0} AS URL "{1}"\n'.format(ns, url))
	bel.write('\n')
	for anno, url in annotations.items():
		bel.write('DEFINE ANNOTATION {0} AS URL "{1}"\n'.format(anno, url))
	bel.write(separator + '\n')
	bel.write('# Statements Section\n\n')
	for ns, url in namespaces.items():
		statements, name, species, date = scaffold(url)
		bel.write('SET Species = {0}\n'.format(species))
		bel.write('SET Citation = {3}"Online Resource", "{0}", "{1}", "{2}", "", ""{4}\n\n'.format(name, url, date, '{', '}'))
		print('\n\tGenerated {0} scaffolding statements for {1}. '.format(str(len(statements)), name))
		for s in sorted(statements):
			bel.write(s + '\n')
		bel.write('\n\n')
		


				

			
	

