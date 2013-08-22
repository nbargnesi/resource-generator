# coding: utf-8

import os
from collections import OrderedDict
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
baseline_data['CID-Synonym-filtered.gz'] = ('ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz',
                                         parsers.PubNamespaceParser)
baseline_data['SID-map.gz'] = ('ftp://ftp.ncbi.nlm.nih.gov/pubchem/Substance/Extras/SID-Map.gz',
                                     parsers.PubEquivParser)
baseline_data['d2013.bin'] = ('ftp://nlmpubs.nlm.nih.gov/online/mesh/.asciimesh/d2013.bin',
                             parsers.MESHParser)
#baseline_data['schem_to_chebi.txt'] = 'datasets/SCHEM_to_CHEBI.txt'
baseline_data['go_201307-termdb.obo-xml.gz'] = ('http://archive.geneontology.org/latest-full/go_201307-termdb.obo-xml.gz',
                                parsers.GOBPParser)
baseline_data['go_201307-termdb.obo-xml.gz'] = ('http://archive.geneontology.org/latest-full/go_201307-termdb.obo-xml.gz',
                                parsers.GOBParser)
baseline_data['doid.owl'] = ('http://purl.obolibrary.org/obo/doid.owl',
                             parsers.DOParser)


baseline_data_opt = OrderedDict()
baseline_data_opt['entrez_info.gz'] = ('datasets/All_Mammalia.gene_info.gz', parsers.EntrezGeneInfoParser)
baseline_data_opt['entrez_history.gz'] = ('datasets/gene_history.gz', parsers.EntrezGeneHistoryParser)
baseline_data_opt['hgnc.tsv'] = ('datasets/hgnc-hgnc_downloads.tsv', parsers.HGNCParser)
baseline_data_opt['mgi.rpt'] = ('datasets/MRK_List2.rpt', parsers.MGIParser)
baseline_data_opt['rgd.txt'] = ('datasets/rgd-genes_rat.tsv', parsers.RGDParser)
baseline_data_opt['chebi.owl'] = ('datasets/chebi.owl', parsers.CHEBIParser)
baseline_data_opt['mesh.bin'] = ('datasets/d2013.bin', parsers.MESHParser)
baseline_data_opt['swiss.xml.gz'] = ('datasets/sprot-uniprot_sprot.xml.gz', parsers.SwissProtParser)
baseline_data_opt['affy.xml'] = ('datasets/affy_data.xml.gz', parsers.AffyParser)
baseline_data_opt['gene2acc.gz'] = ('datasets/gene2accession.gz', parsers.Gene2AccParser)
#baseline_data_opt['schem'] = ('datasets/selventa-legacy-chemical-names.belns', parsers.SCHEMParser)
baseline_data_opt['schem_to_chebi.txt'] = ('datasets/SCHEM_to_CHEBIID.txt', parsers.SCHEMtoCHEBIParser)
# baseline_data_opt['puchem_namespace.gz'] = ('datasets/CID-Synonym-filtered.gz', parsers.PubNamespaceParser)
# baseline_data_opt['pubchem_equiv.gz'] = ('datasets/SID-Map.gz', parsers.PubEquivParser)
baseline_data_opt['gobp.xml.gz'] = ('datasets/go_201307-termdb.obo-xml.gz', parsers.GOBPParser)
baseline_data_opt['gocc.xml.gz'] = ('datasets/go_201307-termdb.obo-xml.gz', parsers.GOCCParser)
baseline_data_opt['doid.owl'] = ('datasets/doid.owl', parsers.DOParser)
