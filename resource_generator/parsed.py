# coding: utf-8
#
# parsed.py

from datasets import *
import csv
import dbm
from collections import defaultdict

# Data needed for namespacing and equivalencing
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
mesh_dict = {}
do_dict = {}

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
mesh_data = MESHData(mesh_dict)
do_data = DOData(do_dict)

count = 0

# Data needed for the change-log
swiss_withdrawn_acc_dict = {}

swiss_withdrawn_acc_data = SwissWithdrawnData(swiss_withdrawn_acc_dict)


# entry passed to this function will be one row from
# the file being parsed by its parser.
def build_data(entry, parser):

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
        synonyms = entry.get('synonyms')
#        print('Name - ' +name)
#        ipdb.set_trace()
        chebi[name] = {
            'primary_id' : primary_id,
            'alt_ids' : alt_ids,
            'synonyms' : synonyms }

    elif parser == 'PubNamespace_Parser':
        pub_id = entry.get('pubchem_id')
        synonym = entry.get('synonym')
        global count
        count = count + 1
        if count % 1000 == 0:
            print('Entry number ' +str(count))
            print('Pub ID: '+pub_id)
        #delim = '|'
        #with open('test.txt', 'w') as fp:
        #    fp.write(delim.join((pub_id, 'A')))
        pub_db = dbm.open('pub-names', 'c')
        pub_db[bytes(pub_id, 'utf-8')] = bytes(synonym, 'utf-8')
        pub_db.close()
#        pub_ns_dict[pub_id].append(synonym)
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

    elif parser == 'MESH_Parser':
        ui = entry.get('ui')
        mh = entry.get('mesh_header')
        mns = entry.get('mns')
        sts = entry.get('sts')
        synonyms = entry.get('synonyms')

        mesh_dict[ui] = {
            'mesh_header' : mh,
            'sts' : sts,
            'mns' : mns,
            'synonyms' : synonyms }

    elif parser == 'SwissWithdrawn_Parser':
        acc = entry.get('accession')

        swiss_withdrawn_acc_dict['accessions'].append(acc)

    elif str(parser) == 'DO_Parser':
        name = entry.get('name')
        id = entry.get('id')
        dbxrefs = entry.get('dbxrefs')
        do_dict[name] = {
            'id' : id,
            'dbxrefs' : dbxrefs }

def load_data(label):

    datasets = [entrez_data, hgnc_data, mgi_data, rgd_data,
                swiss_data, affy_data, chebi_data, pub_ns_data,
                gene2acc_data, entrez_history_data, pub_equiv_data,
                schem_data, schem_to_chebi_data, gobp_data,
                gocc_data, mesh_data, swiss_withdrawn_acc_data,
                do_data]

    for d in datasets:
        if str(d) == label:
            return d
