# coding: utf-8

'''
 datasets.py

 Represent each parsed dataset as an object. This is
 really just a wrapper to the underlying dictionaries,
 but it also provides some useful functions that assist
 in the namespacing and equivalencing process.

'''

import os.path
import time
from common import get_citation_info

class DataSet():
	
	def __init__(self, dictionary):
		self._dict = dictionary

	def get_dictionary(self):
		return self._dict

	def __str__(self):
		return 'DataSet_Object'

class NamespaceDataSet(DataSet):

	# Make .belns file containing ids/labels
	ids = False
	labels = True

	def __init__(self, dictionary, label='namespace-label', name='namespace-name', prefix='namespace-prefix'):
		self._label = label
		self._name = name
		self._prefix = prefix
		super().__init__(dictionary)

	def get_values(self):
		''' Get all non-obsolete primary ids in dataset dict.
		Default is all keys. '''
		for term_id in self._dict:
			yield term_id

	def get_label(self, term_id):
		''' Return the value to be used as the preferred
		label for the associated term id. Use id as default, 
		but will generally be a name/symbol. '''
		return term_id

	def get_name(self, term_id):
		''' Return the term name to use as title (or None). '''
		try:
			name = self._dict.get(term_id).get('name')
			return name
		except:
			return None

	def get_species(self, term_id):
		''' Return species as NCBI tax ID (or None, as applicable). '''
		return None

	def get_encoding(self, term_id):
		''' Return encoding (allowed abundance types) for value. 
		Default = 'A' (Abundance). '''
		return 'A'

	def get_alt_symbols(self, term_id):
		''' Return set of symbol synonyms. Default = None. '''
		return None

	def get_alt_names(self, term_id):
		''' Return set of name synonyms. Default = None. '''
		return None

	def get_alt_ids(self, term_id):
		''' Returns set of alternative IDs. IDs should be
		unique.  '''
		try:
			alt_ids = self._dict.get(term_id).get('alt_ids')
			return alt_ids
		except:
			return None

	def write_ns_values(self, dir):
		data_names = {}
		data_ids = {}
		for term_id in self.get_values():
			encoding = self.get_encoding(term_id)
			label = self.get_label(term_id)
			data_names[label] = encoding
			data_ids[term_id] = encoding
			if self.get_alt_ids(term_id):
				for alt_id in self.get_alt_ids(term_id):
					data_ids[alt_id] = encoding
		if self.labels:
			self.write_data(data_names, dir, self._name+'.belns')
		if self.ids:
			self.write_data(data_ids, dir, self._name+'-ids.belns')

	def write_data(self, data, dir, name):
		if len(data) == 0:
			print('	   WARNING: skipping writing ' + name + '; no namespace data found.')
		else:
			with open(os.path.join(dir, name), mode='w', encoding='utf8') as f:
				# insert header chunk
				if os.path.exists(dir+'/templates/'+name):
					tf = open(dir+'/templates/'+name, encoding="utf-8")
					header = tf.read().rstrip()
					tf.close()
					# add Namespace, Citation and Author values
					header = get_citation_info(name, header)
				else:
					print('WARNING: Missing header template for {0}'.format(name))
					header = '[Values]'
				f.write(header+'\n')
				# write data
				for i in sorted(data.items()):
					f.write('|'.join(i) + '\n')

	def __str__(self):
		return self._label


class EntrezInfoData(NamespaceDataSet):

	labels = False
	ids = True
	#NS = 'entrez-gene-ids.belns'
	#N = 'entrez-gene'
	ENC = {
		'protein-coding' : 'GRP', 'miscRNA' : 'GR', 'ncRNA' : 'GR',
		'snoRNA' : 'GR', 'snRNA' : 'GR', 'tRNA' : 'GR', 'scRNA' : 'GR',
		'other' : 'G', 'pseudo' : 'GR', 'unknown' : 'GRP', 'rRNA' : 'GR'
	}
	subject = "gene/RNA/protein"
	description = "NCBI Entrez Gene identifiers for Homo sapiens, Mus musculus, and Rattus norvegicus."

	def __init__(self, dictionary, label='entrez_info', name='entrez-gene', prefix='egid'):
		super().__init__(dictionary, label, name, prefix)
	# get rid of this block (find where used)
	#def get_ns_values(self):
	#	for gene_id in self._dict:
	#		mapping = self._dict.get(gene_id)
	#		gene_type = mapping.get('type_of_gene')
	#		description = mapping.get('description')
	#		yield gene_id, gene_type, description

	def get_label(self, term_id):
		''' Return the value to be used as the preffered
		label for the associated term id. For Entrez, 
		using the gene ID. '''
		return term_id

	def get_values(self):
		''' Get non-obsolete term values. '''
		for term_id in self._dict:
			yield term_id
	
	def get_species(self, term_id):
		''' Return species as NCBI tax ID (or None, as applicable). '''
		species = self._dict.get(term_id).get('tax_id')
		return species

	def get_encoding(self, gene_id):
		''' Return encoding (allowed abundance types) for value. '''
		mapping = self._dict.get(gene_id)
		gene_type = mapping.get('type_of_gene')
		description = mapping.get('description')
		encoding = EntrezInfoData.ENC.get(gene_type, 'G')
		if gene_type == 'miscRNA' and 'microRNA' in description:
			encoding = 'GRM'
		if gene_type not in EntrezInfoData.ENC:
			print('WARNING ' + gene_type + ' not defined for Entrez. G assigned as default encoding.')
		return encoding		

	def get_alt_symbols(self, gene_id):
		''' Return set of symbol synonyms. '''
		synonyms = set()
		mapping = self._dict.get(gene_id)
		if mapping.get('Synonyms') is not '-':
			synonyms.update(mapping.get('Synonyms').split('|'))
			synonyms.add(mapping.get('Symbol'))
		return synonyms

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		if mapping.get('Other_designations') is not '-':
			synonyms.update(mapping.get('Other_designations').split('|'))
		if mapping.get('description') != '-':
			synonyms.add(mapping.get('description'))
		return synonyms

	#def write_ns_values(self, dir):
	#	''' Write .belns file. '''
	#	data = {}
	#	for gene_id in self.get_values():
	#		encoding = self.get_encoding(gene_id)
	#		data[gene_id] = encoding
	#	name = EntrezInfoData.NS
	#	super(EntrezInfoData, self).write_data(data, dir, name)

	# get rid of this block (find where used)
	def get_eq_values(self):
		for gene_id in self._dict:
			yield gene_id

	# can get rid of this and use get_alt_symbols
	#def get_synonym_symbols(self):
	#	synonym_dict = {}
	#	for gene_id in self._dict:
	#		synonyms = set()
	#		mapping = self.entrez_info_dict.get(gene_id)
	#		if mapping.get('Synonyms') is not '-':
	#			 synonyms.update(mapping.get('Synonyms').split('|'))
	#		synonyms.add(mapping.get('Symbol'))
	#		synonym_dict[gene_id] = synonyms
	#	return synonym_dict
   
	def get_name(self, term_id):
		''' Get official term name. '''
		mapping = self._dict.get(term_id)
		name = mapping.get('Full_name_from_nomenclature_authority')
		return name
	
	# can get rid of this and use get_alt_names
	#def get_synonym_names(self):
	#	synonym_dict = {}
	#	for gene_id in self.entrez_info_dict:
	#		synonyms = set()
	#		mapping = self.entrez_info_dict.get(gene_id)
	#		if mapping.get('Other_designations') is not '-':
	#			synonyms.update(mapping.get('Other_designations').split('|'))
	#		if mapping.get('Full_name_from_nomenclature_authority') != '-':
	#			synonyms.add(mapping.get('Full_name_from_nomenclature_authority'))
	#		if mapping.get('description') != '-':
	#			synonyms.add(mapping.get('description'))
	#		synonym_dict[gene_id] = synonyms
	#	return synonym_dict

	#def __str__(self):
	#	return 'entrez_info'


class EntrezHistoryData(DataSet):

	def __init__(self, dictionary):
		super().__init__(dictionary)

	# this is likely never used, not a namespace data set
	#def get_ns_values(self):
	#	for gene_id in self.entrez_history_dict:
	#		mapping = self.entrez_history_dict.get(gene_id)
	#		gene_type = mapping.get('type_of_gene')
	#		description = mapping.get('description')
	#		yield gene_id, gene_type, description

	def __str__(self):
		return 'entrez_history'


class HGNCData(NamespaceDataSet):
	
#	N = 'hgnc'
#	NS = 'hgnc-approved-symbols.belns'
#	prefix = 'hgnc'
#	name = 'hgnc'
	ENC = {
		'gene with protein product' : 'GRP', 'RNA, cluster' : 'GR',
		'RNA, long non-coding' : 'GR', 'RNA, micro' : 'GRM',
		'RNA, ribosomal' : 'GR', 'RNA, small cytoplasmic' : 'GR',
		'RNA, small misc' : 'GR', 'RNA, small nuclear' : 'GR',
		'RNA, small nucleolar' : 'GR', 'RNA, transfer' : 'GR',
		'phenotype only' : 'G', 'RNA, pseudogene' : 'GR',
		'T cell receptor pseudogene' : 'GR',
		'immunoglobulin pseudogene' : 'GR', 'pseudogene' : 'GR',
		'T cell receptor gene' : 'GRP',
		'complex locus constituent' : 'GRP',
		'endogenous retrovirus' : 'G', 'fragile site' : 'G',
		'immunoglobulin gene' : 'GRP', 'protocadherin' : 'GRP',
		'readthrough' : 'GR', 'region' : 'G',
		'transposable element' : 'G', 'unknown' : 'GRP',
		'virus integration site' : 'G', 'RNA, micro' : 'GRM',
		'RNA, misc' : 'GR', 'RNA, Y' : 'GR', 'RNA, vault' : 'GR',
	}

	def __init__(self, dictionary, label='hgnc', name='hgnc-approved-symbols', prefix='hgnc'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	# ideally, make this obsolete - output not consistent
	#	for symbol in self._dict:
	#		mapping = self._dict.get(symbol)
	#		loc_type = mapping.get('Locus Type')
	#		hgnc_id = mapping.get('HGNC ID')
	#		if '~withdrawn' not in symbol:
	#			yield symbol, loc_type, hgnc_id

	def get_values(self):
		for term_id in self._dict:
			if '~withdrawn' not in self._dict.get(term_id).get('Symbol'):
				yield term_id

	def get_label(self, term_id):
		''' Return preferred label associated with term id. '''
		label = self._dict.get(term_id).get('Symbol')
		return label

	def get_encoding(self, term_id):
		mapping = self._dict.get(term_id)
		locus_type = mapping.get('Locus Type')
		encoding = HGNCData.ENC.get(locus_type, 'G')
		if locus_type not in HGNCData.ENC:
			print('WARNING ' + locus_type + ' not defined for HGNC. G assigned as default encoding.')
		return encoding

	def get_species(self, term_id):
		return '9606'		

	def get_alt_symbols(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		if mapping.get('Synonyms'):
			symbol_synonyms = [s.strip() for s in mapping.get('Synonyms').split(',')]
			synonyms.update(symbol_synonyms)
		if mapping.get('Previous Symbols'):
			old_symbols = [s.strip() for s in mapping.get('Previous Symbols').split(',')]
			synonyms.update(old_symbols)
		return synonyms

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		if mapping.get('Previous Names'):
			old_names = [s.strip('" ') for s in mapping.get('Previous Names').split(', "')]
			synonyms.update(old_names)
		return synonyms

	def get_eq_values(self):
		for symbol in self._dict:
			if '~withdrawn' not in symbol:
				yield symbol

	def get_map(self):
		id_map = {}
		for term_id in self._dict:
			mapping = self._dict.get(term_id)
			symbol = mapping.get('Symbol')
			map[term_id] = symbol
		return id_map

	# may replace with get_alt_symbols()
#	def get_synonym_symbols(self):
#		synonym_dict = {}
#		for term_id in self.get_values():
		#	synonyms = set()
		#	mapping = self._dict.get(symbol)
		#	if mapping.get('Synonyms'):
		#		symbol_synonyms = [s.strip() for s in mapping.get('Synonyms').split(',')]
		#		synonyms.update(symbol_synonyms)
	#		if mapping.get('Previous Symbols'):
	#			old_symbols = [s.strip() for s in mapping.get('Previous Symbols').split(',')]
	#			synonyms.update(old_symbols)
	#		synonyms.add(symbol)
	#		if '~withdrawn' not in symbol:
	#			synonym_dict[symbol] = synonyms
	#	return synonym_dict

	# may replace with get_alt_names()
#	def get_synonym_names(self):
#		synonym_dict = {}
#		for term_id in self.get_values():
#			synonyms = set()
#			mapping = self._dict.get(term_id)
#			name = mapping.get('Approved Name')
#			synonyms.add(name)
#			if mapping.get('Previous Names'):
#				old_names = [s.strip('" ') for s in mapping.get('Previous Names').split(', "')]
#				synonyms.update(old_names)
#		return synonym_dict

	def get_name(self, term_id):
		mapping = self._dict.get(term_id)
		name = mapping.get('Approved Name')
		return name


class MGIData(NamespaceDataSet):

	#N = 'mgi'
	#NS = 'mgi-approved-symbols.belns'
	ENC = {
		'gene' : 'GRP', 'protein coding gene' : 'GRP',
		'non-coding RNA gene' : 'GR', 'rRNA gene' : 'GR',
		'tRNA gene' : 'GR', 'snRNA gene' : 'GR', 'snoRNA gene' : 'GR',
		'miRNA gene' : 'GRM', 'scRNA gene' : 'GR',
		'lincRNA gene' : 'GR', 'RNase P RNA gene' : 'GR',
		'RNase MRP RNA gene' : 'GR', 'telomerase RNA gene' : 'GR',
		'unclassified non-coding RNA gene' : 'GR',
		'heritable phenotypic marker' : 'G', 'gene segment' : 'G',
		'unclassified gene' : 'GRP', 'other feature types' : 'G',
		'pseudogene' : 'GR', 'transgene' : 'G',
		'other genome feature' : 'G', 'pseudogenic region' : 'GR',
		'polymorphic pseudogene' : 'GRP',
		'pseudogenic gene segment' : 'GR', 'SRP RNA gene' : 'GR'
	}

	def __init__(self, dictionary, label='mgi', name='mgi-approved-symbols', prefix='mgi'):
		super().__init__(dictionary, label, name, prefix)

	def get_values(self):
		for term_id in self._dict:
			mapping = self._dict.get(term_id)
			marker_type = mapping.get('Marker Type')
			if marker_type =='Gene' or marker_type == 'Pseudogene':
				yield term_id
	
	def get_species(self, term_id):
		return '10090'

	# get rid of this, after removing references to 
	#def get_ns_values(self):
	#	for marker_symbol in self._dict:
	#		mapping = self._dict.get(marker_symbol)
	#		feature_type = mapping.get('Feature Type')
	#		acc_id = mapping.get('MGI Accession ID')
	#		marker_type = mapping.get('Marker Type')
	#		if marker_type == 'Gene' or marker_type == 'Pseudogene':
	#			yield marker_symbol, feature_type, acc_id
	
	def get_encoding(self, term_id):
		feature_type = self._dict.get(term_id).get('Feature Type')
		encoding = self.ENC.get(feature_type, 'G')
		if feature_type not in self.ENC:
			print('WARNING ' + feature_type + ' not defined for MGI. G assigned as default encoding.')
		return encoding

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('Symbol')
		return label

	def get_name(self, term_id):
		mapping = self._dict.get(term_id)
		name = mapping.get('Marker Name')
		return name

	def get_alt_symbols(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		synonyms = mapping.get('Marker Synonyms').split('|')
		synonyms = {s for s in synonyms if s}
		return synonyms

	#def write_ns_values(self, dir):
	#	data = {}
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		symbol = self.get_label(term_id)
	#		data[symbol] = encoding
	#	name = MGIData.NS
	#	super(MGIData, self).write_data(data, dir, name)

	# remove references to this
	def get_eq_values(self):
		for marker_symbol in self._dict:
			mapping = self._dict.get(marker_symbol)
			marker_type = mapping.get('Marker Type')
			if marker_type == 'Gene' or marker_type == 'Pseudogene':
				yield marker_symbol
	
	# remove dependency on, if possible
	def get_map(self):
		id_map = {}
		for term_id in self._dict:
			symbol = self.get_label(term_id) 
			id_map[term_id] = symbol
		return id_map


class RGDData(NamespaceDataSet):

	#N = 'rgd'
	#NS = 'rgd-approved-symbols.belns'
	ENC = {
		'gene' : 'GRP', 'miscrna' : 'GR', 'predicted-high' : 'GRP',
		'predicted-low' : 'GRP', 'predicted-moderate' : 'GRP',
		'protein-coding' : 'GRP', 'pseudo' : 'GR', 'snrna' : 'GR',
		'trna' : 'GR', 'rrna' : 'GR', 'ncrna': 'GR'
	}

	def __init__(self, dictionary, label='rgd', name='rgd-approved-symbols', prefix='rgd'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for symbol in self._dict:
	#		mapping = self._dict.get(symbol)
	#		name = mapping.get('NAME')
	#		gene_type = mapping.get('GENE_TYPE')
	#		rgd_id = mapping.get('GENE_RGD_ID')
	#		yield symbol, gene_type, name, rgd_id
	
	def get_species(self, term_id):
		''' Rat '''
		return '10116'

	def get_label(self, term_id):
		''' Use Symbol as preferred label for RGD. '''
		label = self._dict.get(term_id).get('SYMBOL')
		return label

	def get_name(self, term_id):
		name = self._dict.get(term_id).get('NAME')
		return name

	def get_encoding(self, term_id):
		gene_type = self._dict.get(term_id).get('GENE_TYPE')
		name = self.get_name(term_id)
		encoding = RGDData.ENC.get(gene_type, 'G')
		if gene_type == 'miscrna' and 'microRNA' in name:
			encoding = 'GRM'
		if gene_type not in RGDData.ENC:
			print('WARNING ' + gene_type + ' not defined for RGD. G assigned as default encoding.')
		return encoding

	def get_alt_symbols(self, term_id):
		synonyms = set()
		if self._dict.get(term_id).get('OLD_SYMBOL'):
			old_symbols = self._dict.get(term_id).get('OLD_SYMBOL').split(';')
			synonyms.update(old_symbols)
		return synonyms

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		if mapping.get('OLD_NAME'):
			old_names = mapping.get('OLD_NAME').split(';')
			synonyms.update(old_names)
		synonyms = {s for s in synonyms if s}
		return synonyms

	#def write_ns_values(self, dir):
	#	data = {}
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		symbol = self.get_label(term_id)
	#		data[symbol] = encoding
	#	name = RGDData.NS
	#	super(RGDData, self).write_data(data, dir, name)

	def get_eq_values(self):
		for symbol in self._dict:
			yield symbol
  
	def get_map(self):
		id_map = {}
		for term_id in self._dict:
			symbol = get_label(term_id)
			id_map[term_id] = symbol
		return id_map


class SwissProtData(NamespaceDataSet):

	#N = 'swissprot'
	#NS_NAMES = 'swissprot-entry-names.belns'
	#NS_ACCESSION = 'swissprot-accession-numbers.belns'
	ids = True

	def __init__(self, dictionary, label='swiss', name='swissprot', prefix='sp'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for name in self._dict:
	#		mapping = self._dict.get(name)
	#		acc = mapping.get('accessions')
	#		yield name, acc

	def get_encoding(self, term_id):
		return 'GRP'

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('name')
		return label

	def get_name(self, term_id):
		mapping = self._dict.get(term_id)
		name = mapping.get('recommendedFullName')
		return name 

	def get_alt_ids(self, term_id):
		alt_ids = self._dict.get(term_id).get('accessions')
		alt_ids = set(alt_ids)
		alt_ids = {alt_id for alt_id in alt_ids if alt_id != term_id}
		return alt_ids

	def get_alt_symbols(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		synonyms.update(mapping.get('alternativeShortNames'))
		if mapping.get('recommendedShortName'):
			synonyms.add(mapping.get('recommendedShortname'))
		if mapping.get('geneName'):
			synonyms.add(mapping.get('geneName'))
		if mapping.get('geneSynonyms'):
			synonyms.update(mapping.get('geneSynonyms'))
		return synonyms

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		synonyms.update(mapping.get('alternativeFullNames'))
		return synonyms

	def get_species(self, term_id):
		species = self._dict.get(term_id).get('tax_id')
		return species

	#def write_ns_values(self, dir):
	#	data_name = {}
	#	data_acc = {}
	#	ns_name = SwissProtData.NS_NAMES
	#	ns_acc = SwissProtData.NS_ACCESSION
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		label = self.get_label(term_id)
	#		data_name[label] = encoding
	#		accessions = self.get_alt_ids(term_id)
	#		for acc in accessions:
	#			data_acc[acc] = encoding
	#	super(SwissProtData, self).write_data(data_name, dir, ns_name)
	#	super(SwissProtData, self).write_data(data_acc, dir, ns_acc)

	def get_eq_values(self):
		for name in self._dict:
			mapping = self._dict.get(name)
			dbrefs = mapping.get('dbreference')
			acc = mapping.get('accessions')
			yield name, dbrefs, acc

#	def get_synonym_symbols(self):
#		synonym_dict = {}
#		for symbol in self._dict:
#			synonyms = set()
#			synonyms.add(symbol)
#			mapping = self._dict.get(symbol)
#			synonyms.update(mapping.get('alternativeShortNames'))
#			if mapping.get('recommendedShortName'):
#				synonyms.add(mapping.get('recommendedShortname'))
#			if mapping.get('geneName'):
#				synonyms.add(mapping.get('geneName'))
#			if mapping.get('geneSynonyms'):
#				synonyms.update(mapping.get('geneSynonyms'))
#			synonym_dict[symbol] = synonyms
#		return synonym_dict
#
#	def get_synonym_names(self):
#		synonym_dict = {}
#		for symbol in self._dict:
#			synonyms = set()
#			mapping = self._dict.get(symbol)
#			synonyms.add(mapping.get('recommendedFullName'))
#			synonyms.update(mapping.get('alternativeFullNames'))
#			synonym_dict[symbol] = synonyms
#		return synonym_dict


class AffyData(NamespaceDataSet):

	#N = 'affy'
	#NS = 'affy-probeset-ids.belns'
	labels = False
	ids = True

	def __init__(self, dictionary, label='affy', name='affy-probeset', prefix='affx'):
		super().__init__(dictionary, label, name, prefix)

	def get_species(self, term_id):
		species = self._dict.get(term_id).get('Species')
		species_dict = {'Homo sapiens': '9606', 
			'Mus musculus': '10090',
			'Rattus norvegicus' : '10116'}
		tax_id = species_dict.get(species)
		return tax_id

	def get_encoding(self, term_id):
		''' Return encoding (allowed abundance types) for value. 
		R - RNAAbundance. '''
		return 'R'

#	def write_ns_values(self, dir):
#		data = {}
#		for pid in self.get_values():
#			encoding = self.get_encoding(pid)
#			data[pid] = encoding
#		super(AffyData, self).write_data(data, dir, AffyData.NS)

	def get_eq_values(self):
		for probe_id in self.affy_dict:
			mapping = self.affy_dict.get(probe_id)
			gene_id	 = mapping.get('Entrez Gene')
			yield probe_id, gene_id


class CHEBIData(NamespaceDataSet):

	#N = 'chebi'
	#NS_NAMES = 'chebi-names.belns'
	#NS_IDS = 'chebi-ids.belns'
	ids = True

	def __init__(self, dictionary, label='chebi', name='chebi', prefix='chebi'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for name in self._dict:
	#		mapping = self._dict.get(name)
	#		primary_id = mapping.get('primary_id')
	#		altIds = mapping.get('alt_ids')
	#		yield name, primary_id, altIds
	
	def get_label(self, term_id):
		label = self._dict.get(term_id).get('name')
		return label

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		if mapping.get('synonyms'):
			synonyms.update(mapping.get('synonyms'))
		return synonyms

	#def write_ns_values(self, dir):
	#	data_names = {}
	#	data_ids = {}
	#	for term_id in self.get_values():
	#		label = self.get_label(term_id)
	#		encoding = self.get_encoding(term_id)
	#		alt_ids = self.get_alt_ids(term_id)
	#		data_names[label] = encoding
	#		data_ids[term_id] = encoding
	#		for i in alt_ids:
	#			data_ids[i] = encoding
	#	super(CHEBIData, self).write_data(data_names, dir, CHEBIData.NS_NAMES)
	#	super(CHEBIData, self).write_data(data_ids, dir, CHEBIData.NS_IDS)

	# remove if possible
	def get_names(self):
		for name in self._dict:
			yield name

	# remove if possible
	def get_primary_ids(self):
		for name in self._dict:
			mapping = self._dict.get(name)
			primary_id = mapping.get('primary_id')
			yield primary_id

	# TODO remove if possible
	def alt_to_primary(self, alt):
		for name in self._dict:
			mapping = self._dict.get(name)
			altIds = mapping.get('alt_ids')
			if alt in altIds:
				primary_id = mapping.get('primary_id')
				return primary_id

	# TODO remove if possible
	def name_to_primary(self, name):
		mapping = self._dict.get(name)
		primary_id = mapping.get('primary_id')
		return primary_id

	def get_synonym_names(self):
		synonym_dict = {}
		for name in self._dict:
			synonyms = set()
			mapping = self._dict.get(name)
			synonyms.add(name)
			if mapping.get('synonyms'):
				alt_names = mapping.get('synonyms')
				synonyms.update(alt_names)
			synonym_dict[name] = synonyms
		return synonym_dict


class SCHEMData(NamespaceDataSet):
	#N = 'schem'	
	#NS = 'selventa-legacy-chemical-names.belns'
	
	def __init__(self, dictionary, label='schem', name='selventa-legacy-chemical-names', prefix='schem'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for entry in self._dict:
	#		yield entry

	#def write_ns_values(self, dir):
	#	data = {}
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		data[term_id] = encoding
	#	super(SCHEMData, self).write_data(data, dir, SCHEMData.NS)

	def get_eq_values(self):
		for entry in self.schem_dict:
			yield entry


class SCHEMtoCHEBIData(DataSet):

	def __init__(self, dictionary):
		super().__init__(dictionary)

	def get_equivalence(self, schem_term):
		mapping = self._dict.get(schem_term)
		if mapping:
			chebi_id = mapping.get('CHEBIID')
			return chebi_id
		else:
			return None

	def __str__(self):
		return 'schem_to_chebi'

class NCHData(NamespaceDataSet):

	#N = 'selventa-named-complexes'
	#PREFIX = 'SCOMP'
	#NS = 'selventa-named-complexes.belns'

	def __init__(self, dictionary, label='nch', name='selventa-named-complexes', prefix='scomp'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for entry in self._dict:
	#		yield entry

	def get_encoding(self, term_id):
		''' Return encoding (allowed abundance types) for 
		value - 'C' complexAbundance. ''' 
		return 'C'

	#def write_ns_values(self, dir):
	#	data = {}
	#	for entry in self.get_values():
	#		data[entry] = self.get_encoding(entry)
	#	super(NCHData, self).write_data(data, dir, NCHData.NS)

	def get_eq_values(self):
		for entry in self.nch_dict:
			yield entry


class CTGData(DataSet):

	def __init__(self, dictionary):
		super().__init__(dictionary)

	def get_equivalence(self, term):
		mapping = self._dict.get(term)
		if mapping:
			go_id = mapping.get('go_id')
			return go_id
		else:
			return None

	def __str__(self):
		return 'ctg'

class SDISData(NamespaceDataSet):

	#N = 'selventa-legacy-diseases'
	#NS = 'selventa-legacy-diseases.belns'

	def __init__(self, dictionary, label='sdis', name='selventa-legacy-diseases', prefix='sdis'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for entry in self.sdis_dict:
	#		yield entry

	def get_encoding(self, term_id):
		return 'O'

	#def write_ns_values(self, dir):
	#	data = {}
	#	for term_id in self.get_ns_values():
	#		encoding = self.get_encoding(term_id)
	#		data[term_id] = encoding
	#	super(SDISData, self).write_data(data, dir, SDISData.NS)

	def get_eq_values(self):
		for entry in self._dict:
			yield entry

	#def __str__(self):
	#	return 'sdis'


class SDIStoDOData(DataSet):

	def __init__(self, dictionary):
		super().__init__(dictionary)

	def get_equivalence(self, sdis_term):
		mapping = self.sdis_to_do.get(sdis_term)
		if mapping:
			do_id = mapping.get('DOID').replace('DOID_', '')
			return do_id
		else:
			return None

	def __str__(self):
		return 'sdis_to_do'


class PubNamespaceData(NamespaceDataSet):

	#NS = 'pubchem.belns'

	def __init__(self, dictionary):
		super(PubNamespaceData, self).__init__(dictionary)

	#def get_ns_values(self):
	#	for pid in self._dict:
	#		yield pid

	def write_ns_values(self, dir):
		data = {}
		encoding = 'A'
		for pid in self.get_ns_values():
			data[pid] = encoding
		super(PubNamespaceData, self).write_data(data, dir, PubNamespaceData.NS)

	def __str__(self):
		return 'pubchem_namespace'


class PubEquivData(DataSet):

	def __init__(self, dictionary):
		super(PubEquivData, self).__init__(dictionary)

	def get_eq_values(self):
		for sid in self._dict:
			mapping = self._dict.get(sid)
			source = mapping.get('Source')
			cid = mapping.get('PubChem CID')

			yield sid, source, cid

	def __str__(self):
		return 'pubchem_equiv'


class Gene2AccData(DataSet):

	def __init__(self, dictionary):
		super(Gene2AccData, self).__init__(dictionary)

	def get_eq_values(self):
		for entrez_gene in self._dict:
			mapping = self._dict.get(entrez_gene)
			status = mapping.get('status')
			taxid = mapping.get('tax_id')
			yield entrez_gene, status, taxid

	def __str__(self):
		return 'gene2acc'


class GOBPData(NamespaceDataSet):

	#N = 'go-biological-process'
	#NS_NAMES = 'go-biological-processes-names.belns'
	#NS_IDS = 'go-biological-processes-ids.belns'
	ids = True

	def __init__(self, dictionary, label='gobp', name='go-biological-processes', prefix='gobp'):
		super().__init__(dictionary, label, name, prefix)

	def get_encoding(self, term_id):
		return 'B'

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('termname')
		return label

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		synonyms.update(mapping.get('synonyms'))
		return synonyms

	#def get_ns_values(self):
	#	for termid in self._dict:
	#		mapping = self._dict.get(termid)
	#		termname = mapping.get('termname')
	#		alt_ids = mapping.get('alt_ids')
#
#			yield termid, termname, alt_ids

	#def write_ns_values(self, dir):
	#	data_names = {}
	#	data_ids = {}
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		label = self.get_label(term_id)
	#		data_names[label] = encoding
	#		data_ids[term_id] = encoding
	#		alt_ids = self.get_alt_ids(term_id)
	#		if alt_ids is not None:
	#			for i in alt_ids:
	#				data_ids[i] = encoding
	#	super(GOBPData, self).write_data(data_names, dir, GOBPData.NS_NAMES)
	#	super(GOBPData, self).write_data(data_ids, dir, GOBPData.NS_IDS)

	def get_eq_values(self):
		for termid in self._dict:
			mapping = self._dict.get(termid)
			termname = mapping.get('termname')
			alt_ids = mapping.get('alt_ids')

			yield termid, termname, alt_ids

	#def get_synonym_names(self):
	#	synonym_dict = {}
	#	for termid in self._dict:
	#		synonyms = set()
	#		mapping = self._dict.get(termid)
	#		synonyms.update(mapping.get('synonyms'))
	#		synonyms.add(mapping.get('termname'))
	#		synonym_dict[termid] = synonyms
	#	return synonym_dict

	#def __str__(self):
	#	return 'gobp'


class GOCCData(NamespaceDataSet):

#	N = 'go-cellular-component'
#	NS_NAMES = 'go-cellular-component-names.belns'
#	NS_IDS = 'go-cellular-component-ids.belns'
	ids = True

	def __init__(self, dictionary, label='gocc', name='go-cellular-component', prefix='gocc'):
		super().__init__(dictionary, label, name, prefix)
	#def get_ns_values(self):
	#	for termid in self._dict:
	#		mapping = self._dict.get(termid)
	#		termname = mapping.get('termname')
	#		complex = mapping.get('complex')
	#		alt_ids = mapping.get('alt_ids')

	#		yield termid, termname, alt_ids, complex

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('termname')
		return label

	def get_alt_names(self, term_id):
		synonyms = set()
		mapping = self._dict.get(term_id)
		synonyms.update(mapping.get('synonyms'))
		return synonyms

	def get_encoding(self, term_id):
		if self._dict.get(term_id).get('complex'):
			encoding = 'C'
		else:
			encoding = 'A'
		return encoding

	#def write_ns_values(self, dir):
	#	data_names = {}
	#	data_ids = {}
	#	for term_id in self.get_values():
	#		encoding = self.get_encoding(term_id)
	#		label = self.get_label(term_id)
	#		data_names[label] = encoding
	#		data_ids[term_id] = encoding
	#		alt_ids = self.get_alt_ids(term_id)
	#		if alt_ids is not None:
	#			for i in alt_ids:
	#				data_ids[i] = encoding
	#	super(GOCCData, self).write_data(data_names, dir, GOCCData.NS_NAMES)
	#	super(GOCCData, self).write_data(data_ids, dir, GOCCData.NS_IDS)

	def get_eq_values(self):
		for termid in self._dict:
			mapping = self._dict.get(termid)
			termname = mapping.get('termname')
			alt_ids = mapping.get('alt_ids')

			yield termid, termname, alt_ids

	#def get_synonym_names(self):
	#	synonym_dict = {}
	#	for termid in self._dict:
	#		synonyms = set()
	#		mapping = self._dict.get(termid)
	#		synonyms.update(mapping.get('synonyms'))
	#		synonyms.add(mapping.get('termname'))
	#		synonym_dict[termid] = synonyms
	#	return synonym_dict

	#def __str__(self):
	#	return 'gocc'


class MESHData(NamespaceDataSet):

	#N = 'mesh'
#	NS_CL = 'mesh-cellular-locations.belns'
#	NS_DS = 'mesh-diseases.belns'
#	NS_BP = 'mesh-biological-processes.belns'

	def __init__(self, dictionary, label, prefix='mesh', name='mesh-temp'):
		super().__init__(dictionary, label, prefix, name)

	#def get_ns_values(self):
	#	for ui in self._dict:
	#		mapping = self._dict.get(ui)
	#		mh = mapping.get('mesh_header')
	#		mns = mapping.get('mns')
	#		sts = mapping.get('sts')
#
#			yield ui, mh, mns, sts

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('mesh_header')
		return label

	def get_encoding(self, term_id):
		if self._label == 'meshcl':
			return 'A'
		elif self._label == 'meshd':
			return 'O'
		elif self._label == 'meshpp':
			return 'B'
		else:
			return 'A'		

#	def write_ns_values(self, dir):
#		data_labels = {}
#		data_ds = {}
#		data_bp = {}
#		for ui, mh, mns, sts in self.get_ns_values():
#		for term_id in self.get_values():
#			label = self.get_label(term_id)
#			encoding = self.get_encoding(term_id)
#			data_labels[label] = encoding
#			if any(branch.startswith('A11.284') for branch in mns):
#				# MeSH Cellular Locations; encoding = 'A'
#				data_cl[mh] = 'A'
#			if any(branch.startswith('C') for branch in mns):
#				# MeSH Diseases; encoding = 'O'
#				data_ds[mh] = 'O'
#			if any(branch.startswith('G') for branch in mns):
#				# MeSH Phenomena and Processes; encoding = 'B'
#				excluded = ('G01', 'G15', 'G17')
#				if not all(branch.startswith(excluded) for branch in mns):
#					data_bp[mh] = 'B'
#		super(MESHData, self).write_data(data_cl, dir, MESHData.NS_CL)
#		super(MESHData, self).write_data(data_ds, dir, MESHData.NS_DS)
#		super(MESHData, self).write_data(data_bp, dir, MESHData.NS_BP)
#		super(MESHData, self).write_data(data_labels, dir, str(self))

	def get_eq_values(self):
		for ui in self._dict:
			mapping = self._dict.get(ui)
			mh = mapping.get('mesh_header')
			mns = mapping.get('mns')
			synonyms = mapping.get('synonyms')

			yield ui, mh, mns, synonyms

	def get_annot_values(self):
		for ui in self._dict:
			mapping = self._dict.get(ui)
			mh = mapping.get('mesh_header')
			mns = mapping.get('mns')
			synonyms = mapping.get('synonyms')

			yield ui, mh, mns, synonyms
  
#	def get_synonym_names(self):
#		synonym_dict = {}
#		for ui in self._dict:
#			mapping = self._dict.get(ui)
#			mh  = mapping.get('mesh_header')
#			synonyms = set(mapping.get('synonyms'))
#			synonyms.add(mh)
#			synonym_dict[mh] = synonyms
#		return synonym_dict

	#def __str__(self):
	#	return 'meshcs'

class SwissWithdrawnData(DataSet):

	def __init__(self, dictionary):
		super(SwissWithdrawnData, self).__init__(dictionary)

	def get_withdrawn_accessions(self):
		accessions = self._dict.get('accessions')
		return accessions

	def __str__(self):
		return 'swiss-withdrawn'


class DOData(NamespaceDataSet):

	#N = 'disease-ontology'
	#NS_NAMES = 'disease-ontology-names.belns'
	#NS_IDS = 'disease-ontology-ids.belns'
	ids = True

	def __init__(self, dictionary, label='do', name='disease-ontology', prefix ='do'):
		super(DOData, self).__init__(dictionary, label, name, prefix)

	#def get_ns_values(self):
	#	for name, mapping in self._dict.items():
	#		yield name, mapping.get('id')

	def get_label(self, term_id):
		label = self._dict.get(term_id).get('name')
		return label

	def get_encoding(self, term_id):
		return 'O'

	def get_alt_names(self,term_id):
		mapping = self._dict.get(term_id)
		synonyms  = set(mapping.get('synonyms'))
		return synonyms

#	def write_ns_values(self, dir):
#		data_names = {}
#		data_ids = {}
#		for term_id in self.get_values():
#			encoding = self.get_encoding(term_id)
#			label = self.get_label(term_id)
#			data_names[label] = encoding
#			data_ids[term_id] = encoding
#		super(DOData, self).write_data(data_names, dir, DOData.NS_NAMES)
#		super(DOData, self).write_data(data_ids, dir, DOData.NS_IDS)

	def get_eq_values(self):
		for name, mapping in self._dict.items():
			yield name, mapping.get('id')

	def get_xrefs(self, ref):
		for name, mapping in self._dict.items():
			dbxrefs = mapping.get('dbxrefs')
			if ref in dbxrefs:
				return name

#	def get_synonym_names(self):
#		synonym_dict = {}
#		for name in self.do_dict:
#			mapping = self.do_dict.get(name)
#			synonyms  = set(mapping.get('synonyms'))
#			synonyms.add(name)
#			synonym_dict[name] = synonyms
#		return synonym_dict

