# coding: utf-8
#
# parsed.py

import ipdb
from datasets import *
import csv
from collections import defaultdict

# if os.path.exists('cached_data'):
#     c_data = []
#     indir = '/home/jhourani/openbel-contributions/resource_generator/touchdown/cached_data'
#     for root, dirs, filenames in os.walk(indir):
#         for f in filenames:
#             with open(os.path.join(root, f), 'r') as fp:
#                 c_data.append(pickle.load(fp))


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
schem_to_chebi = {}
pub_equiv_dict = {}
pub_ns_dict = defaultdict(list)
gobp_dict = {}
gocc_dict = {}

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
pub_ns_data = PubNamespaceData(pub_ns_dict)
pub_equiv_data = PubEquivData(pub_equiv_dict)
gobp_data = GOBPData(gobp_dict)
gocc_data = GOCCData(gocc_dict)

count = 0
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

    elif parser == 'EntrezGeneHistory_Parser':
        gene_id = entry.get('GeneID')
        discontinued_id = entry.get('Discontinued_GeneID')

        entrez_history[gene_id] = {
            'Discontinued_GeneID' : discontinued_id }

    elif parser == 'HGNC_Parser':
        app_symb = entry.get('Approved Symbol')
        loc_type = entry.get('Locus Type')
        hgnc_id = entry.get('HGNC ID')

        hgnc[app_symb] = {
            'Locus Type' : loc_type,
            'HGNC ID' : hgnc_id }

    elif parser == 'MGI_Parser':
        m_symbol = entry.get('Marker Symbol')
        feature_type = entry.get('Feature Type')
        m_type = entry.get('Marker Type')
        acc_id = entry.get('MGI Accession ID')

        mgi[m_symbol] = {
            'Feature Type' : feature_type,
            'Marker Type' : m_type,
            'MGI Accession ID' : acc_id }

    elif parser == 'RGD_Parser':
        gene_type = entry.get('GENE_TYPE')
        name = entry.get('NAME')
        symb = entry.get('SYMBOL')
        rgd_id = entry.get('GENE_RGD_ID')

        rgd[symb] = {
            'GENE_TYPE' : gene_type,
            'NAME' : name,
            'GENE_RGD_ID' : rgd_id }

    elif parser == 'SwissProt_Parser':
        name = entry.get('name')
        acc = entry.get('accessions')
        gene_type = entry.get('type')
        dbref = entry.get('dbreference')

        swiss[name] = {
            'type' : gene_type,
            'accessions' : acc,
            'dbreference' : dbref }

    elif parser == 'Affy_Parser':
        probe_id = entry.get('Probe Set ID')
        entrez_gene = entry.get('Entrez Gene')

        affy[probe_id] = {
            'Entrez Gene' : entrez_gene }

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

    elif parser == 'CHEBI_Parser':
        name = entry.get('name')
        primary_id = entry.get('primary_id')
        alt_ids = entry.get('alt_ids')

        chebi[name] = {
            'primary_id' : primary_id,
            'alt_ids' : alt_ids }

    elif parser == 'PubNamespace_Parser':
        pub_id = entry.get('pubchem_id')
        synonym = entry.get('synonym')
        global count
        count = count + 1
        if count % 50000 == 0:
            print('Entry number ' +str(count))
            print('Pub ID: '+pub_id)
        #delim = '|'
        #with open('test.txt', 'w') as fp:
        #    fp.write(delim.join((pub_id, 'A')))
        pub_ns_dict[pub_id].append(synonym)
#        ipdb.set_trace()

    elif parser == 'PubEquiv_Parser':
        source = entry.get('Source')
        cid = entry.get('PubChem CID')
        sid = entry.get('PubChem SID')
        global count
        count = count + 1
        if count % 50000 == 0:
            print(str(count))
        pub_equiv_dict[sid] = {
            'Source' : source,
            'PubChem CID' : cid }

    elif parser == 'GOBP_Parser':
        termid = entry.get('termid')
        termname = entry.get('termname')
        altids = entry.get('altids')

        gobp_dict[termid] = {
            'termname' : termname,
            'altids' : altids }

    elif parser == 'GOCC_Parser':
        termid = entry.get('termid')
        termname = entry.get('termname')
        complex = entry.get('complex')
        altids = entry.get('altids')

        gocc_dict[termid] = {
            'termname' : termname,
            'complex' : complex,
            'altids' : altids }

def load_data(label):

    datasets = [entrez_data, hgnc_data, mgi_data, rgd_data,
                swiss_data, affy_data, chebi_data, pub_ns_data,
                gene2acc_data, entrez_history_data, pub_equiv_data,
                schem_data, schem_to_chebi_data, gobp_data,
                gocc_data]

    for d in datasets:
        if str(d) == label:
            return d
