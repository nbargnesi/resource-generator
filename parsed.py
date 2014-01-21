# coding: utf-8

'''
 parsed.py

 Acts as a storage module for the data being parsed by each parser.
 This data can get very large, and it has been shown that this module
 alone is not sufficient to meet the memory needs of the program,
 specifically of the PubChem dataset, which is currently commented out.
 Consider replacing with DBM or another type of storage management.

'''

from datasets import *
#import dbm.gnu
#import dbm
from collections import defaultdict


# Data needed for namespacing and equivalencing
entrez_info = {}
entrez_history = {}
hgnc = {}
mgi = {}
rgd = {}
swiss = defaultdict(list)
affy = defaultdict(list)
gene2acc = {}
chebi = {}
schem = {}
sdis = {}
schem_to_chebi = {}
sdis_to_do = {}
nch = {}
ctg = {}
pub_equiv_dict = {}
pub_ns_dict = defaultdict(list)
gobp_dict = {}
gocc_dict = {}
#mesh_dict = {}
meshcl_dict = {}
meshd_dict = {}
meshpp_dict = {}
do_dict = {}

entrez_data = EntrezInfoData(entrez_info)
entrez_history_data = EntrezHistoryData(entrez_history)
hgnc_data = HGNCData(hgnc)
mgi_data = MGIData(mgi)
rgd_data = RGDData(rgd)
swiss_data = SwissProtData(swiss)
affy_data = AffyData(affy)
chebi_data = CHEBIData(chebi)
gene2acc_data = Gene2AccData(gene2acc)
schem_data = SCHEMData(schem)
schem_to_chebi_data = SCHEMtoCHEBIData(schem_to_chebi)
sdis_data = SDISData(sdis)
sdis_to_do_data = SDIStoDOData(sdis_to_do)
pub_ns_data = PubNamespaceData(pub_ns_dict)
pub_equiv_data = PubEquivData(pub_equiv_dict)
gobp_data = GOBPData(gobp_dict)
gocc_data = GOCCData(gocc_dict)
#mesh_data = MESHData(mesh_dict)
meshcl_data = MESHData(meshcl_dict, 'meshcl', 'mesh-cellular-locations', 'meshcl')
meshd_data = MESHData(meshd_dict, 'meshd', 'mesh-diseases', 'meshd')
meshpp_data = MESHData(meshpp_dict, 'meshpp', 'mesh-biological-processes', 'meshpp')

do_data = DOData(do_dict)
nch_data = NCHData(nch)
ctg_data = CTGData(ctg)

count = 0

# Data needed for the change-log
swiss_withdrawn_acc_dict = {}

swiss_withdrawn_acc_data = SwissWithdrawnData(swiss_withdrawn_acc_dict)


# entry passed to this function will be one row from
# the file being parsed by its parser.
def build_data(entry, parser):

	if parser == 'EntrezGeneInfo_Parser':
		gene_id = entry.get('GeneID')
		type_of_gene = entry.get('type_of_gene')
		description = entry.get('description')
		tax_id = entry.get('tax_id')
		official_symbol = entry.get('Symbol_from_nomenclature_authority')
		synonyms = entry.get('Synonyms')
		alternative_names = entry.get('Other_designations')
		name = entry.get('Full_name_from_nomenclature_authority')
		symbol = entry.get('Symbol')
		description = entry.get('description')
		dbXrefs = entry.get('dbXrefs')
		entrez_info[gene_id] = {
			'dbXrefs' : dbXrefs,
			'type_of_gene' : type_of_gene,
			'description' : description,
			'tax_id' : tax_id,
			'Symbol_from_nomenclature_authority' : official_symbol,
			'Symbol' : symbol,
			'Synonyms': synonyms,
			'Other_designations': alternative_names,
			'Full_name_from_nomenclature_authority': name,
			'description': description }

	elif parser == 'EntrezGeneHistory_Parser':
		gene_id = entry.get('GeneID')
		discontinued_id = entry.get('Discontinued_GeneID')

		entrez_history[gene_id] = {
			'Discontinued_GeneID' : discontinued_id }

	elif parser == 'HGNC_Parser':
		app_symb = entry.get('Approved Symbol')
		loc_type = entry.get('Locus Type')
		hgnc_id = entry.get('HGNC ID').replace('HGNC:','')
		old_symbols = entry.get('Previous Symbols')
		old_names = entry.get('Previous Names')
		synonyms = entry.get('Synonyms')
		name_synonyms = entry.get('Name Synonyms')
		name = entry.get('Approved Name')

		hgnc[hgnc_id] = {
			'Locus Type' : loc_type,
			'Symbol' : app_symb, 
			'Previous Symbols' : old_symbols,
			'Previous Names' : old_names,
			'Synonyms' : synonyms,
			'Name Synonyms' : name_synonyms,
			'Approved Name' : name }

	elif parser == 'MGI_Parser':
		m_symbol = entry.get('Marker Symbol')
		feature_type = entry.get('Feature Type')
		m_type = entry.get('Marker Type')
		acc_id = entry.get('MGI Accession ID').replace('MGI:','')
		m_name = entry.get('Marker Name')
		m_syn = entry.get('Marker Synonyms (pipe-separated)')

		mgi[acc_id] = {
			'Feature Type' : feature_type,
			'Marker Type' : m_type,
			'Symbol' : m_symbol,
			'Marker Name' : m_name,
			'Marker Synonyms' : m_syn }

	elif parser == 'RGD_Parser':
		gene_type = entry.get('GENE_TYPE')
		name = entry.get('NAME')
		symb = entry.get('SYMBOL')
		rgd_id = entry.get('GENE_RGD_ID')
		old_symbol = entry.get('OLD_SYMBOL')
		old_name = entry.get('OLD_NAME')

		rgd[rgd_id] = {
			'GENE_TYPE' : gene_type,
			'NAME' : name,
			'SYMBOL' : symb,
			'OLD_SYMBOL' : old_symbol,
			'OLD_NAME' : old_name }

	elif parser == 'SwissProt_Parser':
		name = entry.get('name')
		acc = entry.get('accessions')
		primary_acc = acc[0]
		gene_type = entry.get('type')
		dbref = entry.get('dbreference')
		alt_fullnames = entry.get('alternativeFullNames')
		alt_shortnames = entry.get('alternativeShortNames')
		rec_fullname = entry.get('recommendedFullName')
		rec_shortname = entry.get('recommededShortName')
		gene_name = entry.get('geneName')
		gene_syn = entry.get('geneSynonyms')
		tax_id = entry.get('NCBI Taxonomy')

		swiss[primary_acc] = {
			'name' : name,
			'type' : gene_type,
			'accessions' : acc,
			'dbreference' : dbref,
			'alternativeFullNames' : alt_fullnames,
			'alternativeShortNames' : alt_shortnames,
			'recommendedFullName' : rec_fullname,
			'recommendedShortName' : rec_shortname,
			'geneName' : gene_name,
			'geneSynonym' : gene_syn,
			'tax_id': tax_id }

	elif parser == 'Affy_Parser':
		probe_id = entry.get('Probe Set ID')
		entrez_gene = entry.get('Entrez Gene')
		species = entry.get('Species Scientific Name')

		affy[probe_id] = {
			'Entrez Gene' : entrez_gene,
			'Species' : species }

	elif parser == 'Gene2Acc_Parser':
		status = entry.get('status')
		taxid = entry.get('tax_id')
		entrez_gene = entry.get('GeneID')

		gene2acc[entrez_gene] = {
			'status' : status,
			'tax_id' : taxid,
			'entrez_gene' : entrez_gene }

	elif parser == 'SCHEM_Parser':
		schem_id = entry.get('schem_id')

		schem[schem_id] = 'A'

	elif parser == 'SCHEMtoCHEBI_Parser':
		schem_term = entry.get('SCHEM_term')
		chebi_id = entry.get('CHEBIID')
		chebi_name = entry.get('CHEBI_name')

		schem_to_chebi[schem_term] = {
			'CHEBIID' : chebi_id,
			'CHEBI_name' : chebi_name }

	elif parser == 'SDIS_Parser':
		sdis_id = entry.get('sdis_id')

		sdis[sdis_id] = 'O'

	elif parser == 'SDIStoDO_Parser':
		sdis_term = entry.get('SDIS_term')
		do_id = entry.get('DOID')
		do_name = entry.get('DO_name')

		sdis_to_do[sdis_term] = {
			'DOID' : do_id,
			'DO_name' : do_name }
	
	elif parser == 'Complex_Parser':
		complex_term = entry.get('term')

		nch[complex_term] = 'C'
  
	elif parser == 'Complex_To_GO_Parser':
		term = entry.get('NCH_Value')
		go_id = entry.get('GO_Id')
		go_id = go_id.replace('GO:', '')
		ctg[term] = {
			'go_id' : go_id }
			

	elif parser == 'CHEBI_Parser':
		name = entry.get('name')
		primary_id = entry.get('primary_id')
		alt_ids = entry.get('alt_ids')
		synonyms = entry.get('synonyms')

		chebi[primary_id] = {
			'name' : name,
			'alt_ids' : alt_ids,
			'synonyms' : synonyms }

	# elif parser == 'PubNamespace_Parser':
	#	  pub_id = entry.get('pubchem_id')
	#	  synonym = entry.get('synonym')
	#	  global count
	#	  count = count + 1
	#	  if count % 1000 == 0:
	#		  print('Entry number ' +str(count))
	#		  print('Pub ID: '+pub_id)
	#	  pub_db = dbm.open('pub-names', 'cf')
	#	  pub_db = dbm.gnu.open('pub-names', 'cfu')
	#	  pub_db[bytes(pub_id, 'utf-8')] = bytes(synonym, 'utf-8')
	#	  pub_db.close()
	#	  pub_ns_dict[pub_id].append(synonym)

	# elif parser == 'PubEquiv_Parser':
	#	  source = entry.get('Source')
	#	  cid = entry.get('PubChem CID')
	#	  sid = entry.get('PubChem SID')
	#	  global count
	#	  count = count + 1
	#	  if count % 50000 == 0:
	#		  print(str(count))
	#	  pub_equiv_dict[sid] = {
	#		  'Source' : source,
	#		  'PubChem CID' : cid }

	elif parser == 'GOBP_Parser':
		termid = entry.get('termid')
		termname = entry.get('termname')
		alt_ids = entry.get('altids')
		syn = entry.get('synonyms')

		gobp_dict[termid] = {
			'termname' : termname,
			'alt_ids' : alt_ids,
			'synonyms' : syn }

	elif parser == 'GOCC_Parser':
		termid = entry.get('termid')
		termname = entry.get('termname')
		complex = entry.get('complex')
		alt_ids = entry.get('altids')
		syn = entry.get('synonyms')

		gocc_dict[termid] = {
			'termname' : termname,
			'complex' : complex,
			'alt_ids' : alt_ids,
			'synonyms' : syn }

	elif parser == 'MESH_Parser':
		ui = entry.get('ui')
		mh = entry.get('mesh_header')
		mns = entry.get('mns')
		sts = entry.get('sts')
		synonyms = entry.get('synonyms')
		
		if any(branch.startswith('A11.284') for branch in mns):
			meshcl_dict[ui] = {
				'mesh_header' : mh,
				'sts' : sts,
				'mns' : mns,
				'synonyms' : synonyms }
		if any(branch.startswith('C') for branch in mns):
			meshd_dict[ui] = {
				'mesh_header' : mh,
				'sts' : sts,
				'mns' : mns,
				'synonyms' : synonyms }
		if any(branch.startswith('G') for branch in mns):
			excluded = ('G01', 'G15', 'G17')
			if not all(branch.startswith(excluded) for branch in mns):	
				meshpp_dict[ui] = {
					'mesh_header' : mh,
					'sts' : sts,
					'mns' : mns,
					'synonyms' : synonyms }

	elif parser == 'SwissWithdrawn_Parser':
		acc = entry.get('accession')

		swiss_withdrawn_acc_dict['accessions'].append(acc)

	elif str(parser) == 'DO_Parser':
		name = entry.get('name')
		id = entry.get('id')
		dbxrefs = entry.get('dbxrefs')
		synonyms = entry.get('synonyms')
		do_dict[id] = {
			'name' : name,
			'dbxrefs' : dbxrefs,
			'synonyms' : synonyms }

def load_data(string):

	datasets = [entrez_data, hgnc_data, mgi_data, rgd_data,
				swiss_data, affy_data, chebi_data, pub_ns_data,
				gene2acc_data, entrez_history_data, pub_equiv_data,
				schem_data, schem_to_chebi_data, gobp_data,
				gocc_data, swiss_withdrawn_acc_data,
				do_data, sdis_data, sdis_to_do_data, ctg_data, nch_data,
				meshcl_data, meshd_data, meshpp_data]

	for d in datasets:
		if str(d) == string:
			return d
