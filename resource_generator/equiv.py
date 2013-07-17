# coding: utf-8
#
# equiv.py
#
import uuid
import namespaces
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

# this method is called once, to build an equivalence dict used by SwissProt
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
        # > 1 alt_id then generate a new uuid
        else:
            sp_eq[row.get('name')] = uuid.uuid4()
    # > 1 entrez id than generate a new uuid
    else:
        sp_eq[row.get('name')] = uuid.uuid4()

acc_helper_dict = defaultdict(list)
sp_acc_eq = {}
def build_acc_data(accessions, gene_name):
    # turn list into a queue
    q = deque(accessions)
    # primary accession name is first one on the queue
    primary = q.popleft()
    for item in q:
        acc_helper_dict[item].append(gene_name)
    # map every primary one-to-one with SP entry uuid
    sp_acc_eq[primary] = sp_eq.get(gene_name)

def finish():
    for sec_acc_id, v in acc_helper_dict.items():
        # only maps to one primary accession, same uuid
        if len(v) == 1:
            sp_acc_eq[sec_acc_id] = sp_eq.get(v[0])
        # maps to > 1 primary accession, give it a new uuid.
        else:
            sp_acc_eq[sec_acc_id] = uuid.uuid4()

refseq = {}
sd = {}
# fills a dict mapping (entrez_gene -> refseq status)
def build_refseq(row):
    target_pool = ['9606', '10116', '10090']
    valid_status = ['REVIEWED', 'VALIDATED', 'PROVISIONAL', 'PREDICTED',
                    'MODEL', 'INFERRED']
    taxid = row.get('tax_id')
    status = row.get('status')
    entrez_gene = row.get('GeneID')
    if taxid in target_pool and status in valid_status:
        refseq[entrez_gene] = status

ref_status = {'REVIEWED' : 0,
              'VALIDATED' : 1,
              'PROVISIONAL' : 2,
              'PREDICTED' : 3,
              'MODEL' : 4,
              'INFERRED' : 5,
              '-' : 6}
affy_eq = {}
def affys(row):
    gene_id = row.get('Entrez Gene')
    probe_id = row.get('Probe Set ID')
    if probe_id == '100167_f_at':
        print('gene_id to start with - '+gene_id)

    if gene_id is not None and '---' not in gene_id:

        # need the space before and after '///' because that is how it is parsed.
        entrez_ids = gene_id.split(' /// ')

        # for 1 entrez mapping, use the entez uuid
        if len(entrez_ids) == 1:
            status = entrez_eq.get(entrez_ids[0])
            if status is None:
                affy_eq[probe_id] = uuid.uuid4()
            else:
                affy_eq[probe_id] = status
        # we have > 1 entrez mapping, resolve to one.
        else:
            adjacent_list = []
            for entrez_gene in entrez_ids:
                refstatus = refseq.get(entrez_gene)
                adjacent_list.append(ref_status.get(refstatus))

            # zipping yields a list of tuples like [('5307',0), ('104',2), ('3043',None)]
            # i.e. [(entrez_id, refseq_status)]
            list_of_tuples = list(zip(entrez_ids, adjacent_list))

            # get rid of all 'None' tuples (No entrez mapping)
            list_of_tuples = [tup for tup in list_of_tuples if tup[1] is not None]

            # no mapping, generate new uuid
            if len(list_of_tuples) == 0:
                affy_eq[probe_id] = uuid.uuid4()

            # multiple entrez, resolve by refseq status
            else:
                # min tuple is highest refseq status (0 the best choice)
                min_tuple = min(list_of_tuples, key=lambda x: x[1])
                min_refseq = min_tuple[1]
                lowest_tuples = []

                for item in list_of_tuples:
                    if item[1] == min_refseq:
                        lowest_tuples.append(item)

                # if mutiple genes with same refseq, resolve by lowest gene #
                target_tuple = min(lowest_tuples)
                affy_eq[probe_id] = entrez_eq.get(target_tuple[0])

    # no entrez mapping, create a new uuid
    else:
        affy_eq[probe_id] = uuid.uuid4()

def to_entrez(gene_id):
    converted_id = entrez_eq_dict.get(gene_id)
    return converted_id
