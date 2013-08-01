# coding: utf-8

import os
import parsers


baseline_data = {
    'entrez_info' : 'ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/All_Mammalia.gene_info.gz',
    'entrez_history' : 'ftp://ftp.ncbi.nih.gov/gene/DATA/gene_history.gz',
    'hgnc' : 'http://www.genenames.org/cgi-bin/hgnc_downloads?title=HGNC+output+data&hgnc_dbtag=on&preset=all&status=Approved&status=Entry+Withdrawn&status_opt=2&level=pri&=on&where=&order_by=gd_app_sym_sort&limit=&format=text&submit=submit&.cgifields=&.cgifields=level&.cgifields=chr&.cgifields=status&.cgifields=hgnc_dbtag',
    'mgi' : 'ftp://ftp.informatics.jax.org/pub/reports/MRK_List2.rpt',
    'rgd' : 'ftp://rgd.mcw.edu/pub/data_release/GENES_RAT.txt',
    'swiss' : 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.xml.gz',
    'gene2acc' : 'ftp://ftp.ncbi.nih.gov/gene/DATA/gene2accession.gz',
    'affy' : 'http://www.affymetrix.com/analysis/downloads/netaffxapi/GetFileList.jsp?licence=OPENBEL2013&user=jhourani@selventa.com&password=OPENBEL2013',
    'chebi' : 'ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl',
    'pubchem' : 'ftp://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Synonym-filtered.gz' }

baseline_data_opt = {
    'entrez_info' : ('datasets/eg-gene_info.gz', parsers.EntrezGeneInfoParser),
    'entrez_history' : ('datasets/eg-gene_history.gz', parsers.EntrezGeneHistoryParser),
    'hgnc' : ('datasets/hgnc-hgnc_downloads.tsv', parsers.HGNCParser),
    'mgi' : ('datasets/MRK_List2.rpt', parsers.MGIParser),
    'rgd' : ('datasets/rgd-genes_rat.tsv', parsers.RGDParser),
    'swiss' : ('datasets/sprot-uniprot_sprot.xml.gz', parsers.SwissProtParser),
    'affy' : ('datasets/affy_data.xml.gz', parsers.AffyParser),
    'gene2acc' : ('datasets/gene2accession.gz', parsers.Gene2AccParser),
    'chebi' : ('datasets/chebi.owl', parsers.CHEBIParser),
    'pubchem_namespace' : ('datasets/CID-Synonym-filtered.gz', parsers.PubNamespaceParser),
    'pubchem_equiv' : ('datasets/SID-Map.gz', parsers.PubEquivParser)}
