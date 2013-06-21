# coding: utf-8
#
# equiv.py
#
import uuid
import namespaces
import pdb


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
        listo = [namespaces.hgnc_ns_dict, namespaces.mgi_ns_dict, namespaces.rgd_ns_dict]
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

    for k, v in dbrefs.items():
        if k == 'GeneId':
            gene_ids.extend(v)
        if k in target_pool:
            # could be MGI or RGD or HGNC ids
            alt_ids.extend(v)
    if len(gene_ids) == 1:
        sp_eq[row.get('name')] = entrez_eq.get(gene_ids[0])
    elif len(gene_ids) == 0:
        # are there hgnc, mgi or rgd refs?
        if len(alt_ids) == 0:
            sp_eq[row.get('name')] = uuid.uuid4()
            sp_list.append(row.get('name'))
        elif len(alt_ids) == 1:
            a_id = alt_ids[0]
            if 'HGNC' in a_id:
                hgnc_key = namespaces.hgnc_map.get(a_id)
                sp_eq[row.get('name')] = hgnc_eq.get(hgnc_key)
            elif 'MGI' in a_id:
                mgi_key = namespaces.mgi_map.get(a_id)
                sp_eq[row.get('name')] = mgi_eq.get(mgi_key)
            else:
                rgd_key = namespaces.rgd_map.get(a_id)
                sp_eq[row.get('name')] = rgd_eq.get(rgd_key)
            # more than one alt_id then generate a new uuid
        else:
            sp_eq[row.get('name')] = uuid.uuid4()
        # more than one Entrez id than generate a new uuid
    else:
        sp_eq[row.get('name')] = uuid.uuid4()

def to_entrez(gene_id):
    converted_id = entrez_eq_dict.get(gene_id)
    return converted_id

def changes():
    print('Size of the rgd_eq dict is ' +str(len(rgd_eq)))
    print('Size of the mgi_eq dict is ' +str(len(mgi_eq)))
    print('Size of the hgnc_eq dict is ' +str(len(hgnc_eq)))
    print('Size of the entrez_eq dict is ' +str(len(entrez_eq)))
