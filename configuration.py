# coding: utf-8

'''
 configuration.py
 
 Data objects are initialized here; these objects are expected to be named 
 using the data object '_prefix' string attribute + '_data'.
 
 baseline_data - ordered dictionary mapping each source/input file
 to its parser and resulting data objects. The local file name is 
 mapped to a data tuple containing:
	[0] the source file url
	[1] the parser
	[2] the data object, or a list of data objects
		in the case that multiple objects are generated from the same file
 This dictionary is consumed by gp_baseline.

 data_file_info - dictionary mapping 'info' files for source files 
 to .belns/.beleq output files. This is used by common.get_citation_info
 only in the case where a different source file than the one used to generate
 the corresponding data object should be cited, e.g, the source of the HGNC/RGD/MGI
 equivalence mappings used for the HGNC/MGI/RGD .beleq files is EntrezGene.

 affy_array_names - list of array names to include in the AFFX (Affymetrix
 probe set) namespace. This list is consumed by parsers.AffyParser.  
 
 
'''

from collections import OrderedDict
from common import get_latest_GO_filename
from common import get_latest_MeSH_filename
from datasets import *
import parsers
import os

file_url = 'file://{0}/datasets/'.format(os.getcwd())

baseline_data = OrderedDict()

egid_data = EntrezInfoData()
baseline_data['entrez_info.gz'] = (
	'ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz',
	parsers.EntrezGeneInfoParser, egid_data
)

entrez_history_data = EntrezHistoryData()
baseline_data['entrez_history.gz'] = (
	'ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz',
	parsers.EntrezGeneHistoryParser, entrez_history_data
)

hgnc_data = HGNCData()
baseline_data['hgnc.tsv'] = (
	'http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag',
	parsers.HGNCParser, hgnc_data
)

mgi_data = MGIData()
baseline_data['mgi.rpt'] = (
	'ftp://ftp.informatics.jax.org/pub/reports/MRK_List2.rpt',
	parsers.MGIParser, mgi_data
)

rgd_data = RGDData()
baseline_data['rgd.txt'] = (
	'ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt',
	parsers.RGDParser, rgd_data
)

sp_data = SwissProtData() 
baseline_data['swiss.xml.gz'] = (
	'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz',
	parsers.SwissProtParser, sp_data
)

gene2acc_data = Gene2AccData()
baseline_data['gene2acc.gz'] = (
	'ftp://ftp.ncbi.nih.gov/gene/DATA/gene2accession.gz',
	parsers.Gene2AccParser, gene2acc_data
)

affx_data = AffyData()
baseline_data['affy.xml'] = (
	'http://www.affymetrix.com/analysis/downloads/netaffxapi/GetFileList.jsp?licence=OPENBEL2013&user=jhourani@selventa.com&password=OPENBEL2013',
	parsers.AffyParser, affx_data
)

chebi_data = CHEBIData()
baseline_data['chebi.owl'] = (
	'ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl',
	parsers.CHEBIParser, chebi_data
)

schem_to_chebi_data = SCHEMtoCHEBIData()
baseline_data['SCHEM_to_CHEBIID.txt'] = (
	file_url + 'SCHEM_to_CHEBIID.txt',
	parsers.SCHEMtoCHEBIParser, schem_to_chebi_data
)

schem_data = SCHEMData()
baseline_data['schem'] = (
	'http://resource.belframework.org/belframework/1.0/namespace/selventa-legacy-chemical-names.belns', 
	parsers.SCHEMParser, schem_data
)

sdis_to_do_data = SDIStoDOData()
baseline_data['SDIS_to_DO.txt'] = (
	file_url + 'SDIS_to_DO.txt',
	parsers.SDIStoDOParser, sdis_to_do_data
)

sdis_data = SDISData()
baseline_data['sdis'] = (
	'http://resource.belframework.org/belframework/1.0/namespace/selventa-legacy-diseases.belns',
	parsers.SDISParser, sdis_data
)

scomp_data = NCHData()
baseline_data['named_complex'] = (
	'http://resource.belframework.org/belframework/1.0/namespace/selventa-named-human-complexes.belns',
	parsers.ComplexParser, scomp_data
)

sfam_data = StandardCustomData(name='selventa-protein-families', prefix='sfam')
baseline_data['selventa-protein-families.txt'] = (
	file_url + 'selventa-protein-families.txt', parsers.NamespaceParser, sfam_data
)

ctg_data = CTGData()
baseline_data['named_complexes_to_GOCC.csv'] = (
	file_url + 'named_complexes_to_GOCC.csv',
	parsers.ComplexToGOParser, ctg_data
)

# - get the latest GO archive file name and URL
go_file = get_latest_GO_filename('http://archive.geneontology.org/latest-full')
gobp_dict, gocc_dict = {}, {}
gobp_data = GOData(gobp_dict, name='go-biological-processes', prefix='gobp')
gocc_data = GOData(gocc_dict, name='go-cellular-component', prefix='gocc')
baseline_data['go.xml.gz'] = (go_file, parsers.GOParser, [gobp_data, gocc_data])

do_data = DOData()
baseline_data['doid.owl'] = (
	'http://purl.obolibrary.org/obo/doid.owl',
	parsers.DOParser, do_data
)

mesh_file = get_latest_MeSH_filename('ftp://nlmpubs.nlm.nih.gov/online/mesh/.asciimesh/', 'd', '.bin')
meshcl_dict, meshd_dict, meshpp_dict = {}, {}, {}
meshcl_data = MESHData(meshcl_dict, name='mesh-cellular-locations', prefix='meshcl')
meshd_data = MESHData(meshd_dict, name='mesh-diseases', prefix='meshd')
meshpp_data = MESHData(meshpp_dict, name='mesh-biological-processes', prefix='meshpp')
baseline_data['mesh.bin'] = (
	mesh_file,
	parsers.MESHParser, [meshcl_data, meshd_data, meshpp_data]
)

affy_array_names = ['HG-U133A', 'HG-U133B', 'HG-U133_Plus_2', 'HG_U95Av2',
					   'MG_U74A', 'MG_U74B', 'MG_U74C', 'MOE430A', 'MOE430B',
					   'Mouse430A_2', 'Mouse430_2', 'RAE230A', 'RAE230B',
					   'Rat230_2', 'HT_HG-U133_Plus_PM', 'HT_MG-430A', 
						'HT_Rat230_PM', 'MG_U74Av2', 'MG_U74Bv2', 'MG_U74Cv2']

# location of info file used for each .belns/.beleq file
#  - ONLY if different from the source file; used for common.get_citation_info
data_file_info = {
	'hgnc-approved-symbols.beleq' : 'entrez_info.gz.info',
	'mesh-diseases.beleq' : 'doid.owl.info',
	'mgi-approved-symbols.beleq' : 'entrez_info.gz.info',
	'rgd-approved-symbols.beleq' : 'entrez_info.gz.info',
}

