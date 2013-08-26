# coding: utf-8
#
# equiv.py
#
import uuid
import namespaces
import csv
import parsed
from collections import deque, defaultdict

hgnc_list = []
mgi_list = []
rgd_list = []
sp_list = []

entrez_eq = {}
hgnc_eq = {}
mgi_eq = {}
rgd_eq = {}
sp_eq = {}
entrez_converter = {}
affy_eq = {}
refseq = {}
sd = {}
chebi_id_eq = {}
chebi_name_eq = {}
pub_eq_dict = {}
gobp_eq_dict = {}
gocc_eq_dict = {}
do_eq_dict = {}

ref_status = {'REVIEWED' : 0,
              'VALIDATED' : 1,
              'PROVISIONAL' : 2,
              'PREDICTED' : 3,
              'MODEL' : 4,
              'INFERRED' : 5,
              '-' : 6}

delim = '|'

# create a reference, used in MeSH equivalencing
mesh_to_gocc = '/home/jhourani/openbel-contributions/resource_generator/lions/datasets/meshcs_to_gocc.csv'
mg_eq = {}
with open(mesh_to_gocc, 'r') as meshf:
    mg_eq = dict([(rec[0], rec[2]) for rec in csv.reader(meshf, delimiter=',', quotechar='"')])

# this method is called once, to build an equivalence dict used by SwissProt
def build_equivs():

    ns_dicts = [namespaces.hgnc_ns_dict, namespaces.mgi_ns_dict, \
                 namespaces.rgd_ns_dict]
    for d in ns_dicts:
        for k, v in d.items():
            if d is namespaces.hgnc_ns_dict:
                equiv(k, 'hgnc')
            if d is namespaces.mgi_ns_dict:
                equiv(k, 'mgi')
            if d is namespaces.rgd_ns_dict:
                equiv(k, 'rgd')

def make_eq_dict(d):
    temp_dict = d.get_dictionary()
    for entry in temp_dict:
        entrez_id = entry
        mapping = temp_dict.get(entrez_id)
        tax_id = mapping.get('tax_id')
        symbol = mapping.get('Symbol_from_nomenclature_authority')
        if tax_id == '9606':
            entrez_converter['HGNC:'+symbol] = entrez_id
        if tax_id == '10116':
            entrez_converter['RGD:'+symbol] = entrez_id
        if tax_id == '10090':
            entrez_converter['MGI:'+symbol] = entrez_id

# 'd' is a DataObject, which wraps a nested dictionary. Currently, a copy
# of each .beleq file is stored in a dictionary as well, (like entrez_eq).
# This may not be needed in final implementation.
def equiv(d):
    if str(d) == 'entrez_info':
        with open('entrez_eq.beleq', 'w') as fp:
            for gene_id in d.get_eq_values():
                uid = uuid.uuid4()
                fp.write(delim.join((gene_id, str(uid)))+'\n')
                entrez_eq[gene_id] = uuid.uuid4()
        make_eq_dict(d)

    elif str(d) == 'hgnc':
        with open('hgnc_eq.beleq', 'w') as fp:
            for approved_symbol in d.get_eq_values():
                if '~withdrawn' in approved_symbol:
#                    ipdb.set_trace()
                    continue
                new_id = to_entrez('HGNC:'+approved_symbol)
                if new_id is None:
                    # keep track of which hgnc genes need new uuids (dont map to entrez)
                    hgnc_list.append(approved_symbol)
                    # generate new uuid
                    uid = uuid.uuid4()
                    fp.write(delim.join((approved_symbol, str(uid)))+'\n')
                    hgnc_eq[approved_symbol] = uid
                else:
                    # use the entrez uuid
                    uid = entrez_eq.get(new_id)
                    fp.write(delim.join((approved_symbol, str(uid)))+'\n')
                    hgnc_eq[approved_symbol] = uid

    elif str(d) == 'mgi':
        with open('mgi_eq.beleq', 'w') as fp:
            for marker_symbol in d.get_eq_values():
                new_id = to_entrez('MGI:'+marker_symbol)
                if new_id is None:
                    # keep track of which genes need new uuids (dont map to entrez)
                    mgi_list.append(marker_symbol)
                    # generate new uuid
                    uid = uuid.uuid4()
                    fp.write(delim.join((marker_symbol, str(uid)))+'\n')
                    mgi_eq[marker_symbol] = uid
                else:
                    # use the entrez uuid
                    uid = entrez_eq.get(new_id)
                    fp.write(delim.join((marker_symbol, str(uid)))+'\n')
                    mgi_eq[marker_symbol] = uid

    elif str(d) == 'rgd':
        with open('rgd_eq.beleq', 'w') as fp:
            for symbol in d.get_eq_values():
                new_id = to_entrez('RGD:'+symbol)
                if new_id is None:
                    # keep track of which genes need new uuids (dont map to entrez)
                    rgd_list.append(symbol)
                    # generate new uuid
                    uid = uuid.uuid4()
                    fp.write(delim.join((symbol, str(uid)))+'\n')
                    rgd_eq[symbol] = uid
                else:
                    # use the entrez uuid
                    uid = entrez_eq.get(new_id)
                    fp.write(delim.join((symbol, str(uid)))+'\n')
                    rgd_eq[symbol] = uid

    elif str(d) == 'swiss':
        with open('swiss_eq.beleq', 'w') as fp:
            # dbrefs is a dict, i.e { reference_type : id_of_that_gene}
            for name, dbrefs, accessions in d.get_eq_values():
                target_pool = ['HGNC', 'MGI', 'RGD']
                gene_ids = []
                alt_ids = []

                if dbrefs is not None:
                    for k, v in dbrefs.items():
                        if k == 'GeneId':
                            gene_ids.extend(v)
                        if k in target_pool:
                            # could be MGI or RGD or HGNC ids
                            alt_ids.extend(v)
                if len(gene_ids) == 1:
                    temp_id = entrez_eq.get(gene_ids[0])
                    if temp_id is None:
                        uid = uuid.uuid4()
                        fp.write(delim.join((name, str(uid)))+'\n')
                        sp_eq[name] = uid
                    else:
                        uid = entrez_eq.get(gene_ids[0])
                        fp.write(delim.join((name, str(uid)))+'\n')
                        sp_eq[name] = uid
                elif len(gene_ids) == 0:
                    # are there hgnc, mgi or rgd refs?
                    if len(alt_ids) == 0:
                        uid = uuid.uuid4()
                        fp.write(delim.join((name, str(uid)))+'\n')
                        sp_eq[name] = uid
                        sp_list.append(name)
                    elif len(alt_ids) == 1:
                        a_id = alt_ids[0]
                        if 'HGNC' in a_id:
                            hgnc_key = namespaces.hgnc_map.get(a_id)
                            uid = hgnc_eq.get(hgnc_key)
                            # SwissProt may be referring to a since-removed gene.
                            if uid is None:
                                uid = uuid.uuid4()
                                fp.write(delim.join((name, str(uid)))+'\n')
                                sp_eq[name] = uid
                            else:
                                sp_eq[name] = uid
                        elif 'MGI' in a_id:
                            mgi_key = namespaces.mgi_map.get(a_id)
                            uid = mgi_eq.get(mgi_key)
                            # SwissProt may be referring to a since-removed gene.
                            if uid is None:
                                uid = uuid.uuid4()
                                fp.write(delim.join((name, str(uid)))+'\n')
                                sp_eq[name] = uid
                            else:
                                sp_eq[name] = uid
                        else:
                            rgd_key = namespaces.rgd_map.get(a_id)
                            uid = rgd_eq.get(rgd_key)
                            # SwissProt may be referring to a since-removed gene.
                            if uid is None:
                                uid = uuid.uuid4()
                                fp.write(delim.join((name, str(uid)))+'\n')
                                sp_eq[name] = uid
                            else:
                                fp.write(delim.join((name, str(uid)))+'\n')
                                sp_eq[name] = uid
                    # > 1 alt_id then generate a new uuid
                    else:
                        uid = uuid.uuid4()
                        fp.write(delim.join((name, str(uid)))+'\n')
                        sp_eq[name] = uid
                # > 1 entrez id than generate a new uuid
                else:
                    uid = uuid.uuid4()
                    fp.write(delim.join((name, str(uid)))+'\n')
                    sp_eq[name] = uid
                # finally, generate .beleq for accession data also
                build_acc_data(accessions, name)
            finish()

    elif str(d) == 'affy':
        with open('aff_eq.beleq', 'w') as fp:
            for probe_id, gene_id in d.get_eq_values():

                if gene_id is not None and '---' not in gene_id:

                    # need the space before and after '///' because that is how it is parsed.
                    entrez_ids = gene_id.split(' /// ')

                    # for 1 entrez mapping, use the entez uuid
                    if len(entrez_ids) == 1:
                        status = entrez_eq.get(entrez_ids[0])
                        if status is None:
                            uid = uuid.uuid4()
                            fp.write(delim.join((probe_id, str(uid)))+'\n')
                            affy_eq[probe_id] = uid
                        else:
                            uid = status
                            fp.write(delim.join((probe_id, str(uid)))+'\n')
                            affy_eq[probe_id] = uid
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
                            uid = uuid.uuid4()
                            fp.write(delim.join((probe_id, str(uid)))+'\n')
                            affy_eq[probe_id] = uid

                        # multiple entrez, resolve by refseq status
                        else:
                            # min tuple is highest refseq status (0 the best)
                            min_tuple = min(list_of_tuples, key=lambda x: x[1])
                            min_refseq = min_tuple[1]
                            lowest_tuples = []

                            for item in list_of_tuples:
                                if item[1] == min_refseq:
                                    lowest_tuples.append(item)

                            # if mutiple genes with same refseq, resolve by lowest gene #
                            target_tuple = min(lowest_tuples)
                            uid = entrez_eq.get(target_tuple[0])
                            fp.write(delim.join((probe_id, str(uid)))+'\n')
                            affy_eq[probe_id] = uid
                # no entrez mapping, create a new uuid
                else:
                    uid = uuid.uuid4()
                    fp.write(delim.join((probe_id, str(uid)))+'\n')
                    affy_eq[probe_id] = uid

    # equiv for alt ids and names relies on the equivalence for
    # primary ids being completely generated.
    elif str(d) == 'chebi':
        with open('chebi-ids_eq.beleq', 'w') as fp, open('chebi-names_eq.beleq', 'w') as f:
            # like Entrez, new uuid for primary ids only the FIRST time.
            for primary_id in d.get_primary_ids():
                uid = uuid.uuid4()
                fp.write(delim.join((primary_id, str(uid)))+'\n')
                chebi_id_eq[primary_id] = uid
            for alt_id in d.get_alt_ids():
                if alt_id not in chebi_id_eq:
                    # get its primary equivalent and use its uuid
                    primary = d.alt_to_primary(alt_id)
                    uid = chebi_id_eq[primary]
                    fp.write(delim.join((alt_id, str(uid)))+'\n')
                    chebi_id_eq[alt_id] = uid
            for name in d.get_names():
                primary = d.name_to_primary(name)
                uid = chebi_id_eq.get(primary)
                f.write(delim.join((name, str(uid)))+'\n')
                chebi_name_eq[name] = uid

    elif str(d) == 'pubchem_equiv':
        with open('pubchem_eq.beleq', 'w') as fp:
            for sid, source, cid in d.get_eq_values():
                if 'ChEBI' in source and cid is not None:  # <-- verify that NO PubChem CID == 'None'
                    # use the CHEBI uuid
                    chebi_equiv = source.split(':')[1]
                    uid = chebi_id_eq.get(chebi_equiv)
                    fp.write(delim.join((sid, str(uid)))+'\n')
                    pub_eq_dict[sid] = uid
                else:
                    # generate a new uuid
                    uid = uuid.uuid4()
                    fp.write(delim.join((sid, str(uid)))+'\n')

    elif str(d) == 'gobp':
        with open('gobp-eq.beleq', 'w') as gobp, open('gobp_id-eq.beleq', 'w') as gobp_id:
            for vals in d.get_eq_values():
                termid, termname = vals
                uid = uuid.uuid4()
                gobp_id.write(delim.join((termid, str(uid)))+'\n')
                gobp.write(delim.join((termname, str(uid)))+'\n')
                gobp_eq_dict[termname] = uid

    # GO is the baseline for processes, so new uuids the first time.
    elif str(d) == 'gocc':

        with open('gocc-eq.beleq', 'w') as gocc, open('gocc_id-eq.beleq', 'w') as gocc_id:

            for vals in d.get_eq_values():
                termid, termname = vals
                uid = uuid.uuid4()
                gocc_id.write(delim.join((termid, str(uid)))+'\n')
                gocc.write(delim.join((termname, str(uid)))+'\n')
                gocc_eq_dict[termid] = uid

    elif str(d) == 'do':
        # assign DO a new uuid and use as the primary for diseases
        with open('disease-ontology.beleq', 'w') as dof:
            for vals in d.get_eq_values():
                name = vals
                uid = uuid.uuid4()
                dof.write(delim.join((name, str(uid)))+'\n')
                do_eq_dict[name] = uid

    # elif str(d) == 'sdis':
    #     # try to resolve sdis terms to DO. If there is not one,
    #     # assign a new uuid.
    #     sdis_to_do = parsed.load_data('sdis_to_do')
    #     count = 0
    #     with open('selventa-legacy-diseases.beleq', 'w') as dof:
    #         for vals in d.get_eq_values():
    #             uid = None
    #             sdis_term = vals
    #             if sdis_to_do.has_equivalence(sdis_term):
    #                 count = count + 1
    #                 do_term = sdis_to_do.get_equivalence(sdis_term)
    #                 uid = do_eq_dict[do_term]
    #             else:
    #                 uid = uuid.uuid4()
    #             dof.write(delim.join((sdis_term, uid))+'\n')
    #     print('Able to resolve ' +str(count)+ ' legacy disease terms to DO.')

    elif str(d) == 'sdis_to_do':
        # try to resolve sdis terms to DO. If there is not one,
        # assign a new uuid.
        count = 0
        sdis = parsed.load_data('sdis')
        with open('selventa-legacy-diseases.beleq', 'w') as dof:
            for vals in sdis.get_eq_values():
                uid = None
                sdis_term = vals
                if d.has_equivalence(sdis_term):
                    count = count + 1
                    do_term = d.get_equivalence(sdis_term)
                    if do_term in do_eq_dict:
                        uid = do_eq_dict[do_term]
                    else:
                        uid = do_eq_dict[do_term.lower()]
                else:
                    uid = uuid.uuid4()
                dof.write(delim.join((sdis_term, str(uid)))+'\n')
        print('Able to resolve ' +str(count)+ ' legacy disease terms to DO.')

    elif str(d) == 'schem_to_chebi':
        # try to resolve schem terms to CHEBI. If there is not one,
        # assign a new uuid.
        count = 0
        schem = parsed.load_data('schem')
        with open('selventa-legacy-chemical-names.beleq', 'w') as schemf:
            for vals in schem.get_eq_values():
                uid = None
                schem_term = vals
                if d.has_equivalence(schem_term):
                    count = count + 1
                    chebi_term = d.get_equivalence(schem_term)
                    if chebi_term in chebi_name_eq:
                        uid = chebi_name_eq[chebi_term]
                    elif chebi_term.lower() in chebi_name_eq:
                        uid = chebi_name_eq[chebi_term.lower()]
                else:
                    uid = uuid.uuid4()
                schemf.write(delim.join((schem_term, str(uid)))+'\n')
        print('Able to resolve ' +str(count)+ ' legacy chemical terms to CHEBI.')

    elif str(d) == 'mesh':

        with open('mesh-cellular-locations.beleq', 'w') as mesha, \
                open('mesh-diseases.beleq', 'w') as meshc, \
                open('mesh-biological-processes.beleq', 'w') as meshg:
            do_data = parsed.load_data('do')
            for vals in d.get_eq_values():
                ui, mh, mns, synonyms = vals
                if any('A11.284' in branch for branch in mns):
                    # get GO equiv if there is one
                    uid = None
                    go_id = mg_eq.get(mh)
                    # meshcs_to_gocc contains OBSOLETE GO terms at the moment.
                    # It is possible this lookup will return None, in that
                    # case generate a new uuid.
                    if go_id is not None:
                        uid = gocc_eq_dict.get(go_id.split(':')[1])
                        # try to find out why lookups fail - maybe OBSOLETE?
                        if uid is None:
                            print('Lookup failed for: '+str(go_id.split(':')[1]))
                            uid = uuid.uuid4()
                    else:
                        uid = uuid.uuid4()
                    mesha.write(delim.join((mh, str(uid)))+'\n')
                elif any('C' in branch for branch in mns):
                    # does UI exist as a Xref in DO?
                    xref = do_data.get_xrefs('MSH:'+ui)
                    if xref:
                        uid = do_eq_dict[xref]
                    else:
                        uid = uuid.uuid4()
                    meshc.write(delim.join((mh, str(uid)))+'\n')
                elif any('G' in branch for branch in mns):
                    # synonyms for MeSH
                    uid = None
                    for syn in synonyms:
                        # root 'G' branch in GOBP
                        for name in gobp_eq_dict:
                            if syn.lower() == name.lower():
#                                ipdb.set_trace()
                                uid = gobp_eq_dict.get(name)
                    if uid is None:
                        uid = uuid.uuid4()
                    meshg.write(delim.join((mh, str(uid)))+'\n')

acc_helper_dict = defaultdict(list)
sp_acc_eq = {}
def build_acc_data(accessions, gene_name):
    with open('sp-acc_eq.beleq', 'w') as fp:
        # turn list into a queue
        q = deque(accessions)
        # primary accession name is first one on the queue
        primary = q.popleft()
        for item in q:
            acc_helper_dict[item].append(gene_name)
        # map every primary one-to-one with SP entry uuid
        uid = sp_eq.get(gene_name)
        fp.write(delim.join((primary, str(uid)))+'\n')
        sp_acc_eq[primary] = uid

# try to factor this out and merge into build_acc_data
def finish():
    with open('sp-acc_eq.beleq', 'a') as fp:
        for sec_acc_id, v in acc_helper_dict.items():
            # only maps to one primary accession, same uuid
            if len(v) == 1:
                uid = sp_eq.get(v[0])
                fp.write(delim.join((sec_acc_id, str(uid)))+'\n')
                sp_acc_eq[sec_acc_id] = uid
            # maps to > 1 primary accession, give it a new uuid.
            else:
                uid = uuid.uuid4()
                fp.write(delim.join((sec_acc_id, str(uid)))+'\n')
                sp_acc_eq[sec_acc_id] = uid

# fills a dict mapping (entrez_gene -> refseq status)
def build_refseq(d):
    for entrez_gene, status, taxid in d.get_eq_values():
        target_pool = ['9606', '10116', '10090']
        valid_status = ['REVIEWED', 'VALIDATED', 'PROVISIONAL', 'PREDICTED',
                        'MODEL', 'INFERRED']

        if taxid in target_pool and status in valid_status:
            refseq[entrez_gene] = status

def to_entrez(gene_id):
    converted_id = entrez_converter.get(gene_id)
    return converted_id
