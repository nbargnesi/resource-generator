# coding: utf-8
#
# parsed.py

import ipdb
from datasets import *
from collections import defaultdict

entrez_info = {}
entrez_history = {}
hgnc = {}
mgi = {}
rgd = {}
swiss = defaultdict(list)
affy = defaultdict(list)
gene2acc = {}
chebi = {}
pub_equiv_dict = {}
pub_ns_dict = defaultdict(list)

entrez_data = EntrezInfoData(entrez_info)
hgnc_data = HGNCData(hgnc)
mgi_data = MGIData(mgi)
rgd_data = RGDData(rgd)
swiss_data = SwissProtData(swiss)
affy_data = AffyData(affy)
chebi_data = CHEBIData(chebi)
pub_ns_data = PubNamespaceData(pub_ns_dict)
pub_equiv_data = PubEquivData(pub_equiv_dict)

# entry passed to this function will be one row from
# the file being parsed by its parser.
def build_data(entry, parser):

    # entrez_info['entrez_info'] = 'parsed from eg-gene_info.gz'
    # hgnc['hgnc'] = 'parsed from hgnc-hgnc_downloads.tsv'
    # mgi['mgi'] = 'parsed from MRK_list2.rpt'
    # rgd['rgd'] = 'parsed from rgd-genes_rat.tsv'
    # swiss['swiss_names'] = 'parsed from sprot-uniprot_sprot.xml.gz'
    # affy['affy'] = 'parsed from affy_data.xml.gz'
    # pubchem['pubchem'] = 'parsed fromo CID-Synonym-filtered.gz'
    # chebi['chebi'] = 'parsed from chebi.owl'

    if parser == 'EntrezGeneInfo_Parser':
        gene_id = entry.get('GeneID')
        type_of_gene = entry.get('type_of_gene')
        description = entry.get('description')
        tax_id = entry.get('tax_id')
        symbol = entry.get('Symbol_from_nomenclature_authority')
        entrez_info[gene_id] = {
            'type_of_gene' : type_of_gene,
            'description' : description,
            'tax_id' : tax_id,
            'Symbol_from_nomenclature_authority' : symbol }

    if parser == 'EntrezGeneHistory_Parser':
        gene_id = entry.get('GeneID')
        discontinued_id = entry.get('Discontinued_GeneID')

        entrez_history[gene_id] = {
            'Discontinued_GeneID' : discontinued_id }

    if parser == 'HGNC_Parser':
        app_symb = entry.get('Approved Symbol')
        loc_type = entry.get('Locus Type')
        hgnc_id = entry.get('HGNC ID')

        hgnc[app_symb] = {
            'Locus Type' : loc_type,
            'HGNC ID' : hgnc_id }

    if parser == 'MGI_Parser':
        m_symbol = entry.get('Marker Symbol')
        feature_type = entry.get('Feature Type')
        m_type = entry.get('Marker Type')
        acc_id = entry.get('MGI Accession ID')

        mgi[m_symbol] = {
            'Feature Type' : feature_type,
            'Marker Type' : m_type,
            'MGI Accession ID' : acc_id }

    if parser == 'RGD_Parser':
        gene_type = entry.get('GENE_TYPE')
        name = entry.get('NAME')
        symb = entry.get('SYMBOL')
        rgd_id = entry.get('GENE_RGD_ID')

        rgd[symb] = {
            'GENE_TYPE' : gene_type,
            'NAME' : name,
            'GENE_RGD_ID' : rgd_id }

    if parser == 'SwissProt_Parser':
        name = entry.get('name')
        acc = entry.get('accessions')
        gene_type = entry.get('type')
        dbref = entry.get('dbreference')

        swiss[name] = {
            'type' : gene_type,
            'accessions' : acc,
            'dbreference' : dbref }

    if parser == 'Affy_Parser':
        probe_id = entry.get('Probe Set ID')
        entrez_gene = entry.get('Entrez Gene')

        affy[probe_id] = {
            'Entrez Gene' : entrez_gene }

    if parser == 'Gene2Accession_Parser':
        status = entry.get('status')
        taxid = entry.get('tax_id')
        entrez_gene = entry.get('GeneID')

        gene2acc[entrez_gene] = {
            'status' : status,
            'tax_id' : taxid,
            'entrez_gene' : entrez_gene }

    if parser == 'CHEBI_Parser':
        name = entry.get('name')
        primary_id = entry.get('primary_id')
        alt_ids = entry.get('alt_ids')

        chebi[name] = {
            'primary_id' : primary_id,
            'alt_ids' : alt_ids }

    if parser == 'PUBCHEM_Parser':
        pub_id = entry.get('pubchem_id')
        synonym = entry.get('synonym')

        pub_ns_dict[pub_id] = {
            'synonym' : synonym }

    if parser == 'CID_Parser':
        source = entry.get('Source')
        cid = entry.get('PubChem CID')
        sid = entry.get('Pubchem SID')

        pub_equiv_dict[sid] = {
            'Source' : source,
            'PubChem CID' : cid }

def load_data(label):

    datasets = [entrez_data, hgnc_data, mgi_data, rgd_data,
                swiss_data, affy_data, chebi_data, pub_ns_data,
                gene2acc, entrez_history, pub_equiv_data]

    for d in datasets:
        if str(d) == label:
            return d
