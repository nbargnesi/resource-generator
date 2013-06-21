# coding: utf-8
#
# equiv.py
#
import uuid
import namespaces
import pdb
from collections import deque, defaultdict

entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}
entrez_eq_dict = {}

hgnc_list = []
mgi_list = []
rgd_list = []

sp_list = []
booly = False

def build_equivs():
    global booly
    if not booly:
        listo = [namespaces.hgnc_ns_dict, namespaces.mgi_ns_dict, \
                     namespaces.rgd_ns_dict]
        for d in listo:
            for k, v in d.items():
                if d is namespaces.hgnc_ns_dict:
                    equiv(k, 'hgnc')
                if d is namespaces.mgi_ns_dict:
                    equiv(k, 'mgi')
                if d is namespaces.rgd_ns_dict:
                    equiv(k, 'rgd')
        booly = True

def make_eq_dict(entrez_id, symbol, tax_id):
    if tax_id == '9606':
        entrez_eq_dict['HGNC:'+symbol] = entrez_id
    if tax_id == '10116':
        entrez_eq_dict['RGD:'+symbol] = entrez_id
    if tax_id == '10090':
        entrez_eq_dict['MGI:'+symbol] = entrez_id

# gene_id = 'AKT1' data_type = 'hgnc'
def equiv(gene_id, data_type):
    if data_type is 'entrez':
        entrez_eq[gene_id] = uuid.uuid4()
    if data_type is 'hgnc':
        new_id = to_entrez('HGNC:'+gene_id)
        if new_id is None:
            # keep track of which hgnc genes need new uuids (dont map to entrez)
            hgnc_list.append(gene_id)
            # generate new uuid
            hgnc_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            hgnc_eq[gene_id] = entrez_eq.get(new_id)
    if data_type is 'mgi':
        new_id = to_entrez('MGI:'+gene_id)
        if new_id is None:
            # keep track of which genes need new uuids (dont map to entrez)
            mgi_list.append(gene_id)
            # generate new uuid
            mgi_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            mgi_eq[gene_id] = entrez_eq.get(new_id)
    if data_type is 'rgd':
        new_id = to_entrez('RGD:'+gene_id)
        if new_id is None:
            # keep track of which genes need new uuids (dont map to entrez)
            rgd_list.append(gene_id)
            # generate new uuid
            rgd_eq[gene_id] = uuid.uuid4()
        else:
            # use the entrez uuid
            rgd_eq[gene_id] = entrez_eq.get(new_id)

def build_sp_eq(row):

    # dbrefs is a dict, i.e { reference_type : id_of_that_gene}
    dbrefs = row.get('dbReference')
    target_pool = ['HGNC', 'MGI', 'RGD']
    gene_ids = []
    alt_ids = []
    sp_name = row.get('name')

    for k, v in dbrefs.items():
        if k == 'GeneId':
            gene_ids.extend(v)
        if k in target_pool:
            # could be MGI or RGD or HGNC ids
            alt_ids.extend(v)
    if len(gene_ids) == 1:
        temp_id = entrez_eq.get(gene_ids[0])
        if temp_id is None:
            sp_eq[sp_name] = uuid.uuid4()
        else:
            sp_eq[sp_name] = entrez_eq.get(gene_ids[0])
    elif len(gene_ids) == 0:
        # are there hgnc, mgi or rgd refs?
        if len(alt_ids) == 0:
            sp_eq[sp_name] = uuid.uuid4()
            sp_list.append(sp_name)
        elif len(alt_ids) == 1:
            a_id = alt_ids[0]
            if 'HGNC' in a_id:
                hgnc_key = namespaces.hgnc_map.get(a_id)
                temp_id = hgnc_eq.get(hgnc_key)
                # SwissProt may be referring to a since-removed gene.
                if temp_id is None:
                    sp_eq[sp_name] = uuid.uuid4()
                else:
                    sp_eq[sp_name] = temp_id
            elif 'MGI' in a_id:
                mgi_key = namespaces.mgi_map.get(a_id)
                temp_id = mgi_eq.get(mgi_key)
                # SwissProt may be referring to a since-removed gene.
                if temp_id is None:
                    sp_eq[sp_name] = uuid.uuid4()
                else:
                    sp_eq[sp_name] = temp_id
            else:
                rgd_key = namespaces.rgd_map.get(a_id)
                temp_id = rgd_eq.get(rgd_key)
                # SwissProt may be referring to a since-removed gene.
                if temp_id is None:
                    sp_eq[sp_name] = uuid.uuid4()
                else:
                    sp_eq[sp_name] = temp_id
        # more than one alt_id then generate a new uuid
        else:
            sp_eq[row.get('name')] = uuid.uuid4()
    # more than one Entrez id than generate a new uuid
    else:
        sp_eq[row.get('name')] = uuid.uuid4()

acc_helper_dict = defaultdict(list)
sp_acc_eq = {}
def build_acc_data(accessions, gene_name):
    # turn list into a queue
    q = deque(accessions)
    primary = q.popleft()
    for item in q:
        acc_helper_dict[item].append(gene_name)
    # map every primary one-to-one with SP entry uuid
    sp_acc_eq[primary] = sp_eq.get(gene_name)

def finish():
    for sec_acc_id, v in acc_helper_dict.items():
        # only maps to one primary accession, same uuid
        #pdb.set_trace()
        if len(v) == 1:
            sp_acc_eq[sec_acc_id] = sp_eq.get(v[0])
       # maps to > 1 primary accession, give it a new uuid.
        elif len(v) > 1:
            sp_acc_eq[sec_acc_id] = uuid.uuid4()
        else:
            print('YOU GOTTA PROBLEM MAN!!!')

def to_entrez(gene_id):
    converted_id = entrez_eq_dict.get(gene_id)
    return converted_id
