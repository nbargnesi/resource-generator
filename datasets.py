# coding: utf-8

'''
 datasets.py

 Represent each parsed dataset as an object. This is
 really just a wrapper to the underlying dictionaries,
 but it also provides some useful functions that assist
 in the namespacing and equivalencing process.

'''

import os.path

class DataSet():
	def __init__(self, dictionary):
		self.dict = dictionary

	def get_dictionary(self):
		return self.dict

	def write_data(self, data, dir, name):
		if len(data) == 0:
			print('	   WARNING: skipping writing ' + name + '; no namespace data found.')
		else:
			with open(os.path.join(dir, name), mode='w', encoding='utf8') as f:
				# insert header chunk
				if os.path.exists(dir+'/templates/'+name):
					tf = open(dir+'/templates/'+name, encoding="utf-8")
					header = tf.read()
					tf.close()
				else:
					header = '[Values]\n'
				f.write(header)
				# write data
				for i in sorted(data.items()):
					f.write('|'.join(i) + '\n')

	def __str__(self):
		return 'DataSet_Object'


class EntrezInfoData(DataSet):

	NS = 'entrez-gene-ids.belns'
	ENC = {
		'protein-coding' : 'GRP', 'miscRNA' : 'GR', 'ncRNA' : 'GR',
		'snoRNA' : 'GR', 'snRNA' : 'GR', 'tRNA' : 'GR', 'scRNA' : 'GR',
		'other' : 'G', 'pseudo' : 'GR', 'unknown' : 'GRP', 'rRNA' : 'GR'
	}

	def __init__(self, dictionary):
		super(EntrezInfoData, self).__init__(dictionary)
		self.entrez_info_dict = dictionary

	def get_dictionary(self):
		return self.entrez_info_dict

	def get_ns_values(self):
		for gene_id in self.entrez_info_dict:
			mapping = self.entrez_info_dict.get(gene_id)
			gene_type = mapping.get('type_of_gene')
			description = mapping.get('description')
			yield gene_id, gene_type, description

	def write_ns_values(self, dir):
		data = {}
		for gene_id, gene_type, description in self.get_ns_values():
			encoding = EntrezInfoData.ENC.get(gene_type, 'G')
			if gene_type == 'miscRNA' and 'microRNA' in description:
				encoding = 'GRM'
			if gene_type not in EntrezInfoData.ENC:
				print('WARNING ' + gene_type + ' not defined for Entrez. G assigned as default encoding.')
			data[gene_id] = encoding
		name = EntrezInfoData.NS
		super(EntrezInfoData, self).write_data(data, dir, name)

	def get_eq_values(self):
		for gene_id in self.entrez_info_dict:
			yield gene_id

	def get_synonym_symbols(self):
		synonym_dict = {}
		for gene_id in self.entrez_info_dict:
			synonyms = set()
			mapping = self.entrez_info_dict.get(gene_id)
			if mapping.get('Synonyms') is not '-':
				 synonyms.update(mapping.get('Synonyms').split('|'))
			synonyms.add(mapping.get('Symbol'))
			synonym_dict[gene_id] = synonyms
		return synonym_dict
   
	def get_synonym_names(self):
		synonym_dict = {}
		for gene_id in self.entrez_info_dict:
			synonyms = set()
			mapping = self.entrez_info_dict.get(gene_id)
			if mapping.get('Other_designations') is not '-':
				synonyms.update(mapping.get('Other_designations').split('|'))
			if mapping.get('Full_name_from_nomenclature_authority') != '-':
				synonyms.add(mapping.get('Full_name_from_nomenclature_authority'))
			if mapping.get('description') != '-':
				synonyms.add(mapping.get('description'))
			synonym_dict[gene_id] = synonyms
		return synonym_dict

	def __str__(self):
		return 'entrez_info'


class EntrezHistoryData(DataSet):

	def __init__(self, dictionary):
		super(EntrezHistoryData, self).__init__(dictionary)
		self.entrez_history_dict = dictionary

	def get_dictionary(self):
		return self.entrez_history_dict

	def get_ns_values(self):
		for gene_id in self.entrez_history_dict:
			mapping = self.entrez_history_dict.get(gene_id)
			gene_type = mapping.get('type_of_gene')
			description = mapping.get('description')
			yield gene_id, gene_type, description

	def __str__(self):
		return 'entrez_history'


class HGNCData(DataSet):

	NS = 'hgnc-approved-symbols.belns'
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

	def __init__(self, dictionary):
		super(HGNCData, self).__init__(dictionary)
		self.hgnc_dict = dictionary

	def get_dictionary(self):
		return self.hgnc_dict

	def get_ns_values(self):
		for symbol in self.hgnc_dict:
			mapping = self.hgnc_dict.get(symbol)
			loc_type = mapping.get('Locus Type')
			hgnc_id = mapping.get('HGNC ID')
			if '~withdrawn' not in symbol:
				yield symbol, loc_type, hgnc_id

	def write_ns_values(self, dir):
		data = {}
		for symbol, locus_type, hgnc_id in self.get_ns_values():
			encoding = HGNCData.ENC.get(locus_type, 'G')
			if locus_type not in HGNCData.ENC:
				print('WARNING ' + locus_type + ' not defined for HGNC. G assigned as default encoding.')
			data[symbol] = encoding
		name = HGNCData.NS
		super(HGNCData, self).write_data(data, dir, name)

	def get_eq_values(self):
		for symbol in self.hgnc_dict:
			if '~withdrawn' not in symbol:
				yield symbol

	def get_map(self):
		id_map = {}
		for symbol in self.hgnc_dict:
			mapping = self.hgnc_dict.get(symbol)
			hgnc_id = mapping.get('HGNC ID')
			map[hgnc_id] = symbol
		return id_map

	def get_synonym_symbols(self):
		synonym_dict = {}
		for symbol in self.hgnc_dict:
			synonyms = set()
			mapping = self.hgnc_dict.get(symbol)
			if mapping.get('Synonyms'):
				symbol_synonyms = [s.strip() for s in mapping.get('Synonyms').split(',')]
				synonyms.update(symbol_synonyms)
			if mapping.get('Previous Symbols'):
				old_symbols = [s.strip() for s in mapping.get('Previous Symbols').split(',')]
				synonyms.update(old_symbols)
			synonyms.add(symbol)
			if '~withdrawn' not in symbol:
				synonym_dict[symbol] = synonyms
		return synonym_dict

	def get_synonym_names(self):
		synonym_dict = {}
		for symbol in self.hgnc_dict:
			synonyms = set()
			mapping = self.hgnc_dict.get(symbol)
			name = mapping.get('Approved Name')
			synonyms.add(name)
			if mapping.get('Previous Names'):
				old_names = [s.strip('" ') for s in mapping.get('Previous Names').split(', "')]
				synonyms.update(old_names)
			if '~withdrawn' not in symbol:
				synonym_dict[symbol] = synonyms
		return synonym_dict

	def __str__(self):
		return 'hgnc'


class MGIData(DataSet):

	NS = 'mgi-approved-symbols.belns'
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

	def __init__(self, dictionary):
		super(MGIData, self).__init__(dictionary)
		self.mgi_dict = dictionary

	def get_dictionary(self):
		return self.mgi_dict

	def get_ns_values(self):
		for marker_symbol in self.mgi_dict:
			mapping = self.mgi_dict.get(marker_symbol)
			feature_type = mapping.get('Feature Type')
			acc_id = mapping.get('MGI Accession ID')
			marker_type = mapping.get('Marker Type')
			if marker_type == 'Gene' or marker_type == 'Pseudogene':
				yield marker_symbol, feature_type, acc_id

	def write_ns_values(self, dir):
		data = {}
		for marker_symbol, feature_type, acc_id in self.get_ns_values():
			encoding = MGIData.ENC.get(feature_type, 'G')
			if feature_type not in MGIData.ENC:
				print('WARNING ' + feature_type + ' not defined for MGI. G assigned as default encoding.')
			data[marker_symbol] = encoding
		name = MGIData.NS
		super(MGIData, self).write_data(data, dir, name)

	def get_eq_values(self):
		for marker_symbol in self.mgi_dict:
			mapping = self.mgi_dict.get(marker_symbol)
			marker_type = mapping.get('Marker Type')
			if marker_type == 'Gene' or marker_type == 'Pseudogene':
				yield marker_symbol
	
	def get_map(self):
		id_map = {}
		for marker_symbol in self.mgi_dict:
			mapping = self.mgi_dict.get(marker_symbol)
			acc_id = mapping.get('MGI Accession ID')
			id_map[acc_id] = marker_symbol
		return id_map

	def get_synonym_symbols(self):
		synonym_dict = {}
		for symbol in self.mgi_dict:
			synonyms = set()
			mapping = self.mgi_dict.get(symbol)
			marker_synonyms = mapping.get('Marker Synonyms')
			if marker_synonyms != '':
				synonyms.update(marker_synonyms.split('|'))
			synonyms.add(symbol)
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def get_synonym_names(self):
		synonym_dict = {}
		for symbol in self.mgi_dict:
			synonyms = set()
			mapping = self.mgi_dict.get(symbol)
			name = mapping.get('Marker Name')
			synonyms.add(name)
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def __str__(self):
		return 'mgi'


class RGDData(DataSet):

	NS = 'rgd-approved-symbols.belns'
	ENC = {
		'gene' : 'GRP', 'miscrna' : 'GR', 'predicted-high' : 'GRP',
		'predicted-low' : 'GRP', 'predicted-moderate' : 'GRP',
		'protein-coding' : 'GRP', 'pseudo' : 'GR', 'snrna' : 'GR',
		'trna' : 'GR', 'rrna' : 'GR'
	}

	def __init__(self, dictionary):
		super(RGDData, self).__init__(dictionary)
		self.rgd_dict = dictionary

	def get_dictionary(self):
		return self.rgd_dict

	def get_ns_values(self):
		for symbol in self.rgd_dict:
			mapping = self.rgd_dict.get(symbol)
			name = mapping.get('NAME')
			gene_type = mapping.get('GENE_TYPE')
			rgd_id = mapping.get('GENE_RGD_ID')
			yield symbol, gene_type, name, rgd_id

	def write_ns_values(self, dir):
		data = {}
		for symbol, gene_type, name, rgd_id in self.get_ns_values():
			encoding = RGDData.ENC.get(gene_type, 'G')
			if gene_type == 'miscrna' and 'microRNA' in name:
				encoding = 'GRM'
			if gene_type not in RGDData.ENC:
				print('WARNING ' + gene_type + ' not defined for RGD. G assigned as default encoding.')
			data[symbol] = encoding
		name = RGDData.NS
		super(RGDData, self).write_data(data, dir, name)

	def get_eq_values(self):
		for symbol in self.rgd_dict:
			yield symbol
  
	def get_map(self):
		id_map = {}
		for symbol in self.rgd_dict:
			mapping = self.rgd_dict.get(symbol)
			rgd_id = mapping.get('GENE_RGD_ID')
			id_map[rgd_id] = symbol
		return id_map

	def get_synonym_symbols(self):
		synonym_dict = {}
		for symbol in self.rgd_dict:
			synonyms = set()
			synonyms.add(symbol)
			mapping = self.rgd_dict.get(symbol)
			if mapping.get('OLD_SYMBOL'):
				old_symbols = mapping.get('OLD_SYMBOL').split(';')
				synonyms.update(old_symbols)
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def get_synonym_names(self):
		synonym_dict = {}
		for symbol in self.rgd_dict:
			synonyms = set()
			mapping = self.rgd_dict.get(symbol)
			name = mapping.get('NAME')
			synonyms.add(name)
			if mapping.get('OLD_NAME'):
				old_names = mapping.get('OLD_NAME').split(';')
				synonyms.update(old_names)
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def __str__(self):
		return 'rgd'


class SwissProtData(DataSet):

	NS_NAMES = 'swissprot-entry-names.belns'
	NS_ACCESSION = 'swissprot-accession-numbers.belns'

	def __init__(self, dictionary):
		super(SwissProtData, self).__init__(dictionary)
		self.sp_dict = dictionary

	def get_dictionary(self):
		return self.sp_dict

	def get_ns_values(self):
		for name in self.sp_dict:
			mapping = self.sp_dict.get(name)
			acc = mapping.get('accessions')
			yield name, acc

	def write_ns_values(self, dir):
		data_name = {}
		data_acc = {}
		ns_name = SwissProtData.NS_NAMES
		ns_acc = SwissProtData.NS_ACCESSION
		encoding = 'GRP'
		for gene_name, accessions in self.get_ns_values():
			data_name[gene_name] = encoding
			for acc in accessions:
				data_acc[acc] = encoding
		super(SwissProtData, self).write_data(data_name, dir, ns_name)
		super(SwissProtData, self).write_data(data_acc, dir, ns_acc)

	def get_eq_values(self):
		for name in self.sp_dict:
			mapping = self.sp_dict.get(name)
			dbrefs = mapping.get('dbreference')
			acc = mapping.get('accessions')
			yield name, dbrefs, acc

	def get_synonym_symbols(self):
		synonym_dict = {}
		for symbol in self.sp_dict:
			synonyms = set()
			synonyms.add(symbol)
			mapping = self.sp_dict.get(symbol)
			synonyms.update(mapping.get('alternativeShortNames'))
			if mapping.get('recommendedShortName'):
				synonyms.add(mapping.get('recommendedShortname'))
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def get_synonym_names(self):
		synonym_dict = {}
		for symbol in self.sp_dict:
			synonyms = set()
			mapping = self.sp_dict.get(symbol)
			synonyms.add(mapping.get('recommendedFullName'))
			synonyms.update(mapping.get('alternativeFullNames'))
			synonym_dict[symbol] = synonyms
		return synonym_dict

	def __str__(self):
		return 'swiss'


class AffyData(DataSet):

	NS = 'affy-probeset-ids.belns'

	def __init__(self, dictionary):
		super(AffyData, self).__init__(dictionary)
		self.affy_dict = dictionary

	def get_dictionary(self):
		return self.affy_dict

	def get_ns_values(self):
		for probe_id in self.affy_dict:
			yield probe_id

	def write_ns_values(self, dir):
		data = {}
		encoding = 'R'
		for pid in self.get_ns_values():
			data[pid] = encoding
		super(AffyData, self).write_data(data, dir, AffyData.NS)

	def get_eq_values(self):
		for probe_id in self.affy_dict:
			mapping = self.affy_dict.get(probe_id)
			gene_id	 = mapping.get('Entrez Gene')
			yield probe_id, gene_id

	def __str__(self):
		return 'affy'


class CHEBIData(DataSet):

	NS_NAMES = 'chebi-names.belns'
	NS_IDS = 'chebi-ids.belns'

	def __init__(self, dictionary):
		super(CHEBIData, self).__init__(dictionary)
		self.chebi_dict = dictionary

	def get_dictionary(self):
		return self.chebi_dict

	def get_ns_values(self):
		for name in self.chebi_dict:
			mapping = self.chebi_dict.get(name)
			primary_id = mapping.get('primary_id')
			altIds = mapping.get('alt_ids')
			yield name, primary_id, altIds

	def write_ns_values(self, dir):
		data_names = {}
		data_ids = {}
		encoding = 'A'
		for name, primary_id, altids in self.get_ns_values():
			data_names[name] = encoding
			data_ids[primary_id] = encoding
			for i in altids:
				data_ids[i] = encoding
		super(CHEBIData, self).write_data(data_names, dir, CHEBIData.NS_NAMES)
		super(CHEBIData, self).write_data(data_ids, dir, CHEBIData.NS_IDS)

	def get_names(self):
		for name in self.chebi_dict:
			yield name

	def get_primary_ids(self):
		for name in self.chebi_dict:
			mapping = self.chebi_dict.get(name)
			primary_id = mapping.get('primary_id')
			yield primary_id

	def get_alt_ids(self):
		for name in self.chebi_dict:
			mapping = self.chebi_dict.get(name)
			altIds = mapping.get('alt_ids')
			if altIds is not None:
				for alt in altIds:
					yield alt

	def alt_to_primary(self, alt):
		for name in self.chebi_dict:
			mapping = self.chebi_dict.get(name)
			altIds = mapping.get('alt_ids')
			if alt in altIds:
				primary_id = mapping.get('primary_id')
				return primary_id

	def name_to_primary(self, name):
		mapping = self.chebi_dict.get(name)
		primary_id = mapping.get('primary_id')
		return primary_id

	def get_synonym_symbols(self):
		return None

	def get_synonym_names(self):
		synonym_dict = {}
		for name in self.chebi_dict:
			synonyms = set()
			mapping = self.chebi_dict.get(name)
			synonyms.add(name)
			if mapping.get('synonyms'):
				alt_names = mapping.get('synonyms')
				synonyms.update(alt_names)
			synonym_dict[name] = synonyms
		return synonym_dict

	def __str__(self):
		return 'chebi'


class SCHEMData(DataSet):
	
	NS = 'selventa-legacy-chemical-names.belns'

	def __init__(self, dictionary):
		super(SCHEMData, self).__init__(dictionary)
		self.schem_dict = dictionary

	def get_dictionary(self):
		return self.schem_dict

	def get_ns_values(self):
		for entry in self.schem_dict:
			yield entry

	def write_ns_values(self, dir):
		data = {}
		encoding = 'A'
		for entry in self.get_ns_values():
			data[entry] = encoding
		super(SCHEMData, self).write_data(data, dir, SCHEMData.NS)

	def get_eq_values(self):
		for entry in self.schem_dict:
			yield entry

	def __str__(self):
		return 'schem'


class SCHEMtoCHEBIData(DataSet):

	def __init__(self, dictionary):
		super(SCHEMtoCHEBIData, self).__init__(dictionary)
		self.schem_to_chebi = dictionary

	def get_dictionary(self):
		return self.schem_to_chebi

	def get_equivalence(self, schem_term):
		mapping = self.schem_to_chebi.get(schem_term)
		if mapping:
			chebi_id = mapping.get('CHEBIID')
			return chebi_id
		else:
			return None

	def __str__(self):
		return 'schem_to_chebi'

class NCHData(DataSet):

	NS = 'selventa-named-complexes.belns'

	def __init__(self, dictionary):
		super(NCHData, self).__init__(dictionary)
		self.nch_dict = dictionary

	def get_dictionary(self):
		return self.nch_dict

	def get_ns_values(self):
		for entry in self.nch_dict:
			yield entry

	def write_ns_values(self, dir):
		data = {}
		encoding = 'C'
		for entry in self.get_ns_values():
			data[entry] = encoding
		super(NCHData, self).write_data(data, dir, NCHData.NS)

	def get_eq_values(self):
		for entry in self.nch_dict:
			yield entry

	def __str__(self):
		return 'nch'

class CTGData(DataSet):

	def __init__(self, dictionary):
		super(CTGData, self).__init__(dictionary)
		self.ctg = dictionary

	def get_dictionary(self):
		return self.ctg

	def get_equivalence(self, term):
		mapping = self.ctg.get(term)
		if mapping:
			go_id = mapping.get('go_id')
			return go_id
		else:
			return None

	def __str__(self):
		return 'ctg'

class SDISData(DataSet):

	NS = 'selventa-legacy-diseases.belns'

	def __init__(self, dictionary):
		super(SDISData, self).__init__(dictionary)
		self.sdis_dict = dictionary

	def get_dictionary(self):
		return self.sdis_dict

	def get_ns_values(self):
		for entry in self.sdis_dict:
			yield entry

	def write_ns_values(self, dir):
		data = {}
		encoding = 'O'
		for entry in self.get_ns_values():
			data[entry] = encoding
		super(SDISData, self).write_data(data, dir, SDISData.NS)

	def get_eq_values(self):
		for entry in self.sdis_dict:
			yield entry

	def __str__(self):
		return 'sdis'


class SDIStoDOData(DataSet):

	def __init__(self, dictionary):
		super(SDIStoDOData, self).__init__(dictionary)
		self.sdis_to_do = dictionary

	def get_dictionary(self):
		return self.sdis_to_do

	def get_equivalence(self, sdis_term):
		mapping = self.sdis_to_do.get(sdis_term)
		if mapping:
			do_id = mapping.get('DOID').replace('DOID_', '')
			return do_id
		else:
			return None

	def __str__(self):
		return 'sdis_to_do'


class PubNamespaceData(DataSet):

	NS = 'pubchem.belns'

	def __init__(self, dictionary):
		super(PubNamespaceData, self).__init__(dictionary)
		self.pub_dict = dictionary

	def get_dictionary(self):
		return self.pub_dict

	def get_ns_values(self):
		for pid in self.pub_dict:
			yield pid

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
		self.pub_eq_dict = dictionary

	def get_dictionary(self):
		return self.pub_eq_dict

	def get_eq_values(self):
		for sid in self.pub_eq_dict:
			mapping = self.pub_eq_dict.get(sid)
			source = mapping.get('Source')
			cid = mapping.get('PubChem CID')

			yield sid, source, cid

	def __str__(self):
		return 'pubchem_equiv'


class Gene2AccData(DataSet):

	def __init__(self, dictionary):
		super(Gene2AccData, self).__init__(dictionary)
		self.g2a_dict = dictionary

	def get_dictionary(self):
		return self.g2a_dict

	def get_eq_values(self):
		for entrez_gene in self.g2a_dict:
			mapping = self.g2a_dict.get(entrez_gene)
			status = mapping.get('status')
			taxid = mapping.get('tax_id')
			yield entrez_gene, status, taxid

	def __str__(self):
		return 'gene2acc'


class GOBPData(DataSet):

	NS_NAMES = 'go-biological-processes-names.belns'
	NS_IDS = 'go-biological-processes-ids.belns'

	def __init__(self, dictionary):
		super(GOBPData, self).__init__(dictionary)
		self.gobp_dict = dictionary

	def get_dictionary(self):
		return self.gobp_dict

	def get_ns_values(self):
		for termid in self.gobp_dict:
			mapping = self.gobp_dict.get(termid)
			termname = mapping.get('termname')
			altids = mapping.get('altids')

			yield termid, termname, altids

	def write_ns_values(self, dir):
		data_names = {}
		data_ids = {}
		encoding = 'B'
		for termid, termname, altids in self.get_ns_values():
			data_names[termname] = encoding
			data_ids[termid] = encoding
			if altids is not None:
				for i in altids:
					data_ids[i] = encoding
		super(GOBPData, self).write_data(data_names, dir, GOBPData.NS_NAMES)
		super(GOBPData, self).write_data(data_ids, dir, GOBPData.NS_IDS)

	def get_eq_values(self):
		for termid in self.gobp_dict:
			mapping = self.gobp_dict.get(termid)
			termname = mapping.get('termname')
			altids = mapping.get('altids')

			yield termid, termname, altids

	def get_synonym_symbols(self):
		return None

	def get_synonym_names(self):
		synonym_dict = {}
		for termid in self.gobp_dict:
			synonyms = set()
			mapping = self.gobp_dict.get(termid)
			synonyms.update(mapping.get('synonyms'))
			synonyms.add(mapping.get('termname'))
			synonym_dict[termid] = synonyms
		return synonym_dict

	def __str__(self):
		return 'gobp'


class GOCCData(DataSet):

	NS_NAMES = 'go-cellular-component-names.belns'
	NS_IDS = 'go-cellular-component-ids.belns'

	def __init__(self, dictionary):
		super(GOCCData, self).__init__(dictionary)
		self.gocc_dict = dictionary

	def get_dictionary(self):
		return self.gocc_dict

	def get_ns_values(self):
		for termid in self.gocc_dict:
			mapping = self.gocc_dict.get(termid)
			termname = mapping.get('termname')
			complex = mapping.get('complex')
			altids = mapping.get('altids')

			yield termid, termname, altids, complex

	def write_ns_values(self, dir):
		data_names = {}
		data_ids = {}
		for termid, termname, altids, complex in self.get_ns_values():
			if complex:
				encoding = 'C'
			else:
				encoding = 'A'
			data_names[termname] = encoding
			data_ids[termid] = encoding
			if altids is not None:
				for i in altids:
					data_ids[i] = encoding
		super(GOCCData, self).write_data(data_names, dir, GOCCData.NS_NAMES)
		super(GOCCData, self).write_data(data_ids, dir, GOCCData.NS_IDS)

	def get_eq_values(self):
		for termid in self.gocc_dict:
			mapping = self.gocc_dict.get(termid)
			termname = mapping.get('termname')
			altids = mapping.get('altids')

			yield termid, termname, altids

	def get_synonym_symbols(self):
		return None

	def get_synonym_names(self):
		synonym_dict = {}
		for termid in self.gocc_dict:
			synonyms = set()
			mapping = self.gocc_dict.get(termid)
			synonyms.update(mapping.get('synonyms'))
			synonyms.add(mapping.get('termname'))
			synonym_dict[termid] = synonyms
		return synonym_dict

	def __str__(self):
		return 'gocc'


class MESHData(DataSet):

	NS_CL = 'mesh-cellular-locations.belns'
	NS_DS = 'mesh-diseases.belns'
	NS_BP = 'mesh-biological-processes.belns'

	def __init__(self, dictionary):
		super(MESHData, self).__init__(dictionary)
		self.mesh_dict = dictionary

	def get_dictionary(self):
		return self.mesh_dict

	def get_ns_values(self):
		for ui in self.mesh_dict:
			mapping = self.mesh_dict.get(ui)
			mh = mapping.get('mesh_header')
			mns = mapping.get('mns')
			sts = mapping.get('sts')

			yield ui, mh, mns, sts

	def write_ns_values(self, dir):
		data_cl = {}
		data_ds = {}
		data_bp = {}
		for ui, mh, mns, sts in self.get_ns_values():
			if any(branch.startswith('A11.284') for branch in mns):
				# MeSH Cellular Locations; encoding = 'A'
				data_cl[mh] = 'A'
			if any(branch.startswith('C') for branch in mns):
				# MeSH Diseases; encoding = 'O'
				data_ds[mh] = 'O'
			if any(branch.startswith('G') for branch in mns):
				# MeSH Phenomena and Processes; encoding = 'B'
				excluded = ('G01', 'G15', 'G17')
				if not all(branch.startswith(excluded) for branch in mns):
					data_bp[mh] = 'B'
		super(MESHData, self).write_data(data_cl, dir, MESHData.NS_CL)
		super(MESHData, self).write_data(data_ds, dir, MESHData.NS_DS)
		super(MESHData, self).write_data(data_bp, dir, MESHData.NS_BP)

	def get_eq_values(self):
		for ui in self.mesh_dict:
			mapping = self.mesh_dict.get(ui)
			mh = mapping.get('mesh_header')
			mns = mapping.get('mns')
			synonyms = mapping.get('synonyms')

			yield ui, mh, mns, synonyms

	def get_annot_values(self):
		for ui in self.mesh_dict:
			mapping = self.mesh_dict.get(ui)
			mh = mapping.get('mesh_header')
			mns = mapping.get('mns')
			synonyms = mapping.get('synonyms')

			yield ui, mh, mns, synonyms
  
	def get_synonym_names(self):
		synonym_dict = {}
		for ui in self.mesh_dict:
			mapping = self.mesh_dict.get(ui)
			mh  = mapping.get('mesh_header')
			synonyms = set(mapping.get('synonyms'))
			synonyms.add(mh)
			synonym_dict[ui] = synonyms
		return synonym_dict

	def get_synonym_symbols(self):
		return None
  
	def __str__(self):
		return 'mesh'

class SwissWithdrawnData(DataSet):

	def __init__(self, dictionary):
		super(SwissWithdrawnData, self).__init__(dictionary)
		self.s_dict = dictionary

	def get_dictionary(self):
		return self.s_dict

	def get_withdrawn_accessions(self):
		accessions = self.s_dict.get('accessions')
		return accessions

	def __str__(self):
		return 'swiss-withdrawn'


class DOData(DataSet):

	NS_NAMES = 'disease-ontology-names.belns'
	NS_IDS = 'disease-ontology-ids.belns'

	def __init__(self, dictionary):
		super(DOData, self).__init__(dictionary)
		self.do_dict = dictionary

	def get_dictionary(self):
		return self.do_dict

	def get_ns_values(self):
		for name, mapping in self.do_dict.items():
			yield name, mapping.get('id')

	def write_ns_values(self, dir):
		data_names = {}
		data_ids = {}
		encoding = 'O'
		for name, id in self.get_ns_values():
			data_names[name] = encoding
			data_ids[id] = encoding
		super(DOData, self).write_data(data_names, dir, DOData.NS_NAMES)
		super(DOData, self).write_data(data_ids, dir, DOData.NS_IDS)

	def get_eq_values(self):
		for name, mapping in self.do_dict.items():
			yield name, mapping.get('id')

	def get_xrefs(self, ref):
		for name, mapping in self.do_dict.items():
			dbxrefs = mapping.get('dbxrefs')
			if ref in dbxrefs:
				return name

	def get_synonym_names(self):
		synonym_dict = {}
		for name in self.do_dict:
			mapping = self.do_dict.get(name)
			synonyms  = set(mapping.get('synonyms'))
			synonyms.add(name)
			synonym_dict[name] = synonyms
		return synonym_dict

	def get_synonym_symbols(self):
		return None

	def __str__(self):
		return 'do'
