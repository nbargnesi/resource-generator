# coding: utf-8
#
# changelog_config.py
#
# Configuration for the change log script

from collections import OrderedDict
import parsers

changelog_data = OrderedDict()
changelog_data['entrez'] = \
    ('ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz', parsers.EntrezGeneHistoryParser)
changelog_data['hgnc'] = \
    ('http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag', parsers.HGNCParser)
changelog_data['mgi'] = \
    ('ftp://ftp.informatics.jax.org/pub/reports/MRK_List1.rpt', parsers.MGIParser)
changelog_data['rgd'] = \
    ('ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt', parsers.RGDParser)
changelog_data['swiss_lost_accessions'] = \
    ('ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/delac_sp.txt', parsers.SwissWithdrawnParser)


changelog_data_opt = OrderedDict()
changelog_data_opt['entrez'] = \
    ('lions/datasets/eg-gene_history.gz', parsers.EntrezGeneHistoryParser)
changelog_data_opt['hgnc'] = \
    ('lions/datasets/hgnc-hgnc_downloads.tsv', parsers.HGNCParser)
changelog_data_opt['mgi'] = \
    ('lions/datasets/MRK_List1.rpt', parsers.MGIParser)
changelog_data_opt['rgd'] = \
    ('lions/datasets/GENES_RAT.txt', parsers.RGDParser)
changelog_data_opt['swiss_lost_accessions'] = \
    ('lions/datasets/delac_sp.txt', parsers.SwissWithdrawnParser)
