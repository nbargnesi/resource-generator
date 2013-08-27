# coding: utf-8
#
# changelog_config.py
#
# Configuration for the change log script

from collections import OrderedDict
import parsers

changelog_data = OrderedDict()
changelog_data['entrez_info.gz'] = \
    ('ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz', parsers.EntrezGeneHistoryParser)
changelog_data['hgnc.tsv'] = \
    ('http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag', parsers.HGNCParser)
changelog_data['mgi.rpt'] = \
    ('ftp://ftp.informatics.jax.org/pub/reports/MRK_List1.rpt', parsers.MGIParser)
changelog_data['rgd,txt'] = \
    ('ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt', parsers.RGDParser)
changelog_data['delac_sp.txt'] = \
    ('ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/delac_sp.txt', parsers.SwissWithdrawnParser)
changelog_data['gobp'] = \
    ('http://archive.geneontology.org/latest-full/go_201307-termdb.obo-xml.gz', parsers.GOBPParser)
changelog_data['gocc'] = \
    ('http://archive.geneontology.org/latest-full/go_201307-termdb.obo-xml.gz', parsers.GOCCParser)
changelog_data['chebi'] = \
    ('ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl', parsers.CHEBIParser)
changelog_data['mesh'] = \
    ('ftp://nlmpubs.nlm.nih.gov/online/mesh/.newterms/replace2013.txt', parsers.MESHChangesParser)
# changelog_data['do'] = \
#     ('datasets/doid.owl', parsers.DODeprecatedParser)
