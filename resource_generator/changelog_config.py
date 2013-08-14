# coding: utf-8
#
# changelog_config.py
#
# Configuration for the change log script

from collections import OrderedDict
import parsers

changelog_data = OrderedDict()
changelog_data['swiss_lost_accessions'] = ('ftp://ftp.uniprot.org/pub/databases/uniprot/knowledgebase/docs/delac_sp.txt', parsers.SwissWithdrawnParser)
