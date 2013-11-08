# coding: utf-8

'''
 changelog_config.py

 Configuration for the change-log script. Provides a
 mapping for each dataset to its proper parser. Each
 dataset is independant, and can be commented/uncommented
 as desired by the user.

'''

from collections import OrderedDict
from common import get_latest_GO_filename
import parsers

changelog_data = OrderedDict()
changelog_data['gene_history.gz'] = \
	('ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz', parsers.EntrezGeneHistoryParser)
changelog_data['hgnc.tsv'] = \
	('http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag', parsers.HGNCParser)
changelog_data['MRK_List1.rpt'] = \
	('ftp://ftp.informatics.jax.org/pub/reports/MRK_List1.rpt', parsers.MGIParser)
changelog_data['rgd.txt'] = \
	('ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt', parsers.RGDParser)
changelog_data['rgd_obsolete.txt'] = \
	('ftp://rgd.mcw.edu/pub/data_release/GENES_OBSOLETE_IDS.txt', parsers.RGDObsoleteParser)
changelog_data['delac_sp.txt'] = \
	('ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/delac_sp.txt', parsers.SwissWithdrawnParser)
# get the latest GO archive file name and URL
go_file = get_latest_GO_filename('http://archive.geneontology.org/latest-full')
changelog_data['gobp.xml.gz'] = (go_file, parsers.GOBPParser)
changelog_data['gocc.xml.gz'] = (go_file, parsers.GOCCParser)
#changelog_data['gobp.xml.gz'] = \
#	 ('http://archive.geneontology.org/latest-full/go_201309-termdb.obo-xml.gz', parsers.GOBPParser)
#changelog_data['gocc.xml.gz'] = \
#	 ('http://archive.geneontology.org/latest-full/go_201309-termdb.obo-xml.gz', parsers.GOCCParser)
changelog_data['chebi.owl'] = \
	('ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl', parsers.CHEBIParser)
changelog_data['replace2013.txt'] = \
	('ftp://nlmpubs.nlm.nih.gov/online/mesh/.newterms/replace2013.txt', parsers.MESHChangesParser)
changelog_data['doid.owl'] = \
	('http://purl.obolibrary.org/obo/doid.owl', parsers.DODeprecatedParser)
