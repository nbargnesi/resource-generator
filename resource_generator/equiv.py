# coding: utf-8
#
# equiv.py
#

# build equivalencies, starting with Entrez. Assign UUID to each unique gene.
entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}
entrez_eq_dict = {}

hgnc_list = []
mgi_list = []
rgd_list = []

sp_eq = {}
sp_list = []
target_pool = ['HGNC', 'MGI', 'RGD']

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
            #hgnc_count = hgnc_count + 1
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
    gene_ids = []
    alt_ids = []

#    if row.get('name') == 'IL7_RAT':
#        print('DBREFS for ' +row.get('name')+ ' ' +str(dbrefs))
    for k, v in dbrefs.items():
        if k == 'GeneId':
            gene_ids.extend(v)
        if k in target_pool:
            # could be MGI or RGD or HGNC ids
            alt_ids.extend(v)
    # new ID if more than 1 entrez reference
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
                hgnc_key = hgnc_map.get(a_id)
                sp_eq[row.get('name')] = hgnc_eq.get(hgnc_key)
            elif 'MGI' in a_id:
                mgi_key = mgi_map.get(a_id)
                sp_eq[row.get('name')] = mgi_eq.get(mgi_key)
            else:
                rgd_key = rgd_map.get(a_id)
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
