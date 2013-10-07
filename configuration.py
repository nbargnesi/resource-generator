# coding: utf-8

'''
 configuration.py

 A mapping of each dataset to its proper parser. This dictionary
 is consumed by gp_baseline to generate the .belns and .beleq
 files. The datasets/parsers are themselves independant, and
 can be commented/uncommented based on the users desire to
 generate the files for a particular dataset.

'''

from collections import OrderedDict
from common import get_latest_GO_filename
import parsers


baseline_data = OrderedDict()
baseline_data['entrez_info.gz'] = ('ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz',
                                   parsers.EntrezGeneInfoParser)
baseline_data['entrez_history.gz'] = ('ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz',
                                      parsers.EntrezGeneHistoryParser)
baseline_data['hgnc.tsv'] = ('http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag',
                             parsers.HGNCParser)
baseline_data['mgi.rpt'] = ('ftp://ftp.informatics.jax.org/pub/reports/MRK_List2.rpt',
                            parsers.MGIParser)
baseline_data['rgd.txt'] = ('ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt',
                            parsers.RGDParser)
baseline_data['swiss.xml.gz'] = ('ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz',
                                 parsers.SwissProtParser)
baseline_data['gene2acc.gz'] = ('ftp://ftp.ncbi.nih.gov/gene/DATA/gene2accession.gz',
                                parsers.Gene2AccParser)
baseline_data['affy.xml'] = ('http://www.affymetrix.com/analysis/downloads/netaffxapi/GetFileList.jsp?licence=OPENBEL2013&user=jhourani@selventa.com&password=OPENBEL2013',
                             parsers.AffyParser)
baseline_data['chebi.owl'] = ('ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl',
                               parsers.CHEBIParser)
# baseline_data['pubchem_namespace.gz'] = ('ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz',
                                         # parsers.PubNamespaceParser)
# baseline_data['pubchem_equiv.gz'] = ('ftp://ftp.ncbi.nlm.nih.gov/pubchem/Substance/Extras/SID-Map.gz',
#                                      parsers.PubEquivParser)
baseline_data['SCHEM_to_CHEBIID.txt'] = ('datasets/SCHEM_to_CHEBIID.txt', parsers.SCHEMtoCHEBIParser)
baseline_data['schem'] = ('http://resource.belframework.org/belframework/1.0/namespace/selventa-legacy-chemical-names.belns', parsers.SCHEMParser)
baseline_data['SDIS_to_DO.txt'] = ('datasets/SDIS_to_DOID.txt', parsers.SDIStoDOParser)
baseline_data['sdis'] = ('http://resource.belframework.org/belframework/1.0/namespace/selventa-legacy-diseases.belns', parsers.SDISParser)
# need to change links to GO - date in filename will change with each update
# 2013-10-01 changes to GO resource file parser:
# get the latest GO archive file name and URL
go_file = get_latest_GO_filename('http://archive.geneontology.org/latest-full')
# - modified parsers.py uses archive URL to locate latest resource file
#baseline_data['gobp.xml.gz'] = ('http://archive.geneontology.org/latest-full/go_201309-termdb.obo-xml.gz',
#                                parsers.GOBPParser)
#baseline_data['gocc.xml.gz'] = ('http://archive.geneontology.org/latest-full/go_201309-termdb.obo-xml.gz',
#                                parsers.GOCCParser)
baseline_data['gobp.xml.gz'] = (go_file, parsers.GOBPParser)
baseline_data['gocc.xml.gz'] = (go_file, parsers.GOCCParser)                        
baseline_data['doid.owl'] = ('http://purl.obolibrary.org/obo/doid.owl',
                             parsers.DOParser)
baseline_data['mesh.bin'] = ('ftp://nlmpubs.nlm.nih.gov/online/mesh/.asciimesh/d2013.bin',
                              parsers.MESHParser)
