# coding: utf-8

'''
 equiv.py

 Construct each of the .beleq files, given a particular dataset.
 This involves gathering all the terms and determining whether
 or not there are existing terms that refer to the same thing.
 Terms are either then equivalenced to something else, or given
 a new uuid.

'''

import uuid
import csv
import parsed
import os
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
chebi_id_eq = {}
chebi_name_eq = {}
pub_eq_dict = {}
gobp_eq_dict = {}
gobp_id_eq = {}
gocc_eq_dict = {}
gocc_names_eq = {}
do_eq_dict = {}
do_id_eq = {}
schem_eq = {}
sdis_eq = {}
mesh_cs_eq = {}
mesh_d_eq = {}
mesh_pp_eq = {}

# ID to symbol mapping data used for SwissProt equivalences
hgnc_map = parsed.load_data('hgnc').get_map()
mgi_map = parsed.load_data('mgi').get_map()
rgd_map = parsed.load_data('rgd').get_map()

ref_status = {'REVIEWED' : 0,
              'VALIDATED' : 1,
              'PROVISIONAL' : 2,
              'PREDICTED' : 3,
              'MODEL' : 4,
              'INFERRED' : 5,
              '-' : 6}

delim = '|'

# create a reference, used in MeSH equivalencing
curdir = os.getcwd()
mesh_to_gocc = curdir+'/datasets/meshcs_to_gocc.csv'
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
def equiv(d, verbose):
    if str(d) == 'entrez_info':
        for gene_id in d.get_eq_values():
            uid = uuid.uuid4()
            entrez_eq[gene_id] = uid
        write_beleq(entrez_eq, 'entrez-gene-ids')
        make_eq_dict(d)

    elif str(d) == 'hgnc':
        for approved_symbol in d.get_eq_values():
            if '~withdrawn' in approved_symbol:
                continue
            new_id = to_entrez('HGNC:'+approved_symbol)
            if new_id is None:
                # keep track of which hgnc genes need new uuids (dont map to entrez)
                hgnc_list.append(approved_symbol)
                # generate new uuid
                uid = uuid.uuid4()
            else:
                # use the entrez uuid
                uid = entrez_eq.get(new_id)
            hgnc_eq[approved_symbol] = uid
        write_beleq(hgnc_eq, 'hgnc-approved-symbols')

    elif str(d) == 'mgi':
        for marker_symbol in d.get_eq_values():
            new_id = to_entrez('MGI:'+marker_symbol)
            if new_id is None:
                # keep track of which genes need new uuids (dont map to entrez)
                mgi_list.append(marker_symbol)
                # generate new uuid
                uid = uuid.uuid4()
            else:
                # use the entrez uuid
                uid = entrez_eq.get(new_id)
            mgi_eq[marker_symbol] = uid
        write_beleq(mgi_eq, 'mgi-approved-symbols')    

    elif str(d) == 'rgd':
        for symbol in d.get_eq_values():
            new_id = to_entrez('RGD:'+symbol)
            if new_id is None:
                # keep track of which genes need new uuids (dont map to entrez)
                rgd_list.append(symbol)
                # generate new uuid
                uid = uuid.uuid4()
            else:
                # use the entrez uuid
                uid = entrez_eq.get(new_id)
            rgd_eq[symbol] = uid
        write_beleq(rgd_eq, 'rgd-approved-symbols')	    

    elif str(d) == 'swiss':
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
                uid = entrez_eq.get(gene_ids[0])
            elif len(gene_ids) == 0:
                # if no gene ids, try HGNC, MGI or RGD refs
                if len(alt_ids) == 0:
                    uid = uuid.uuid4()
                    sp_list.append(name)
                elif len(alt_ids) == 1:
                    a_id = alt_ids[0]
                    if 'HGNC' in a_id:
                        hgnc_key = hgnc_map.get(a_id)
                        uid = hgnc_eq.get(hgnc_key)
                    elif 'MGI' in a_id:
                        mgi_key = mgi_map.get(a_id)
                        uid = mgi_eq.get(mgi_key)
                    else:
                        # note 'RGD' not in id string for RGD dbrefs
                        rgd_key = rgd_map.get(a_id)
                        uid = rgd_eq.get(rgd_key)
                elif len(alt_ids) >1:
                    uid = uuid.uuid4()
            # > 1 entrez id than generate a new uuid
            elif len(gene_ids) >1:
                uid = uuid.uuid4()
            if uid is None:
                uid = uuid.uuid4()
            sp_eq[name] = uid
      
            # finally, generate .beleq for accession data also
            # add primary accessions to equivalence dict
            build_acc_data(accessions, name)
	# add secondary accessions to equivalence dict
        swiss_accessions_eq()
        write_beleq(sp_eq, 'swissprot-entry-names')
        write_beleq(sp_acc_eq, 'swissprot-accession-numbers')
    
    elif str(d) == 'affy':
        refseq = build_refseq(parsed.load_data('gene2acc'))
        for probe_id, gene_id in d.get_eq_values():

            if gene_id is not None and '---' not in gene_id:

                # need the space before and after '///' because that is how it is parsed.
                entrez_ids = gene_id.split(' /// ')

                # for 1 entrez mapping, use the entez uuid
                if len(entrez_ids) == 1:
                    uid = entrez_eq.get(entrez_ids[0])
                    if uid is None:
                        uid = uuid.uuid4()

                # if > 1 entrez mapping, resolve to one.
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
            # no entrez mapping, create a new uuid
            else:
                uid = uuid.uuid4()
            affy_eq[probe_id] = uid
        write_beleq(affy_eq, 'affy-probeset-ids') 

    # equiv for alt ids and names relies on the equivalence for
    # primary ids being completely generated.
    elif str(d) == 'chebi':
        for primary_id in d.get_primary_ids():
            uid = uuid.uuid4()
            chebi_id_eq[primary_id] = uid
        for alt_id in d.get_alt_ids():
            if alt_id not in chebi_id_eq:
                # get its primary equivalent and use its uuid
                primary = d.alt_to_primary(alt_id)
                uid = chebi_id_eq[primary]
                chebi_id_eq[alt_id] = uid
        for name in d.get_names():
            primary = d.name_to_primary(name)
            uid = chebi_id_eq.get(primary)
            chebi_name_eq[name] = uid
        write_beleq(chebi_name_eq, 'chebi-names')
        write_beleq(chebi_id_eq, 'chebi-ids')

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
        for termid, termname, altids in d.get_eq_values():
            uid = uuid.uuid4()
            gobp_eq_dict[termname] = uid
            gobp_id_eq[termid] = uid
            if altids:
                for i in altids:
                    gobp_id_eq[i] = uid
        write_beleq(gobp_eq_dict, 'go-biological-processes-names')
        write_beleq(gobp_id_eq, 'go-biological-processes-ids')
    # GO is the baseline for processes, so new uuids.

    elif str(d) == 'gocc':
        for termid, termname, altids in d.get_eq_values():
            uid = uuid.uuid4()
            gocc_eq_dict[termid] = uid 
            gocc_names_eq[termname] = uid
            if altids:
                for i in altids:
                    gocc_eq_dict[i] = uid
        write_beleq(gocc_eq_dict, 'go-cellular-component-ids')
        write_beleq(gocc_names_eq, 'go-cellular-component-names')

    elif str(d) == 'do':
        # assign DO a new uuid and use as the primary for diseases
        for vals in d.get_eq_values():
            name, id = vals
            uid = uuid.uuid4()
            do_eq_dict[name] = uid
            do_id_eq[id] = uid
        write_beleq(do_eq_dict, 'disease-ontology-names')
        write_beleq(do_id_eq, 'disease-ontology-ids')

    elif str(d) == 'sdis_to_do':
        # try to resolve sdis terms to DO. If there is not one,
        # assign a new uuid.
        count = 0
        sdis = parsed.load_data('sdis')
        for entry in sdis.get_eq_values():
            #uid = None
            do_id = d.get_equivalence(entry)
            #sdis_term = vals
            #if d.has_equivalence(sdis_term):
            if do_id:
                count = count + 1
                uid = do_id_eq.get(do_id)
               
               # do_term = d.get_equivalence(sdis_term)
               # if do_term in do_eq_dict:
               #     uid = do_eq_dict[do_term]
               # else:
               #     uid = do_eq_dict[do_term.lower()]
            else:
                uid = uuid.uuid4()
            sdis_eq[entry] = uid
        write_beleq(sdis_eq, 'selventa-legacy-diseases')
        if verbose:
            print('Able to resolve ' +str(count)+ ' legacy disease terms to DO.')

    elif str(d) == 'schem_to_chebi':
        # try to resolve schem terms to CHEBI. If there is not one,
        # assign a new uuid.
        count = 0
        schem = parsed.load_data('schem')
        for schem_term in schem.get_eq_values():
            #uid = None
            #schem_term = vals
            #if d.has_equivalence(schem_term):
            #    count = count + 1
            chebi_id = d.get_equivalence(schem_term)
            if chebi_id:
                count = count + 1
                uid = chebi_id_eq.get(chebi_id)
                if uid is None:
                    uid = uuid.uuid4()
               #if chebi_term in chebi_name_eq:
                    #uid = chebi_name_eq[chebi_term]
                #elif chebi_term.lower() in chebi_name_eq:
                 #   uid = chebi_name_eq[chebi_term.lower()]
            else:
                uid = uuid.uuid4()
            schem_eq[schem_term] = uid
        write_beleq(schem_eq, 'selventa-legacy-chemical-names')
        if verbose:
            print('Able to resolve ' +str(count)+ ' legacy chemical terms to CHEBI.')

    elif str(d) == 'mesh':

        do_data = parsed.load_data('do')
        for vals in d.get_eq_values():
            ui, mh, mns, synonyms = vals
            # MeSH Cellular Structures equivalences to GO Cellular Components
            if any('A11.284' in branch for branch in mns):
                # get GO equiv if there is one in meshcs_to_gocc.csv
                uid = None
                go_id = mg_eq.get(mh)
                if go_id:
                    go_id = go_id.replace('GO:','')
                # meshcs_to_gocc contains OBSOLETE GO terms at the moment.
                # It is possible this lookup will return None, in that
                # case generate a new uuid.
                if go_id is not None:
                    uid = gocc_eq_dict.get(go_id)
                    if uid is None:
                        if verbose:
                            print('Lookup failed for: '+str(go_id))
                        uid = uuid.uuid4()
                else:
                    uid = uuid.uuid4()
                mesh_cs_eq[mh] = uid
            # MeSH Diseases equivalences to Disease Ontology (DO) 
            if any('C' in branch for branch in mns):
                # does UI exist as a Xref in DO?
                xref = do_data.get_xrefs('MSH:'+ui)
                if xref:
                    uid = do_eq_dict[xref]
                else:
                    uid = uuid.uuid4()
                mesh_d_eq[mh] = uid
            # MeSH Phenomena and Processes
            if any('G' in branch for branch in mns):
                excluded = ('G01', 'G02', 'G15', 'G17')
                if all(branch.startswith(excluded) for branch in mns):
                     continue
                # synonyms for MeSH
                uid = None
                for syn in synonyms:
                    # root 'G' branch in GOBP
                    for name in gobp_eq_dict:
                        if syn.casefold() == name.casefold() or mh.casefold() == name.casefold():
                            uid = gobp_eq_dict.get(name)
                if uid is None:
                    uid = uuid.uuid4()
                mesh_pp_eq[mh] = uid
        write_beleq(mesh_cs_eq, 'mesh-cellular-locations')
        write_beleq(mesh_d_eq, 'mesh-diseases')
        write_beleq(mesh_pp_eq, 'mesh-biological-processes')

acc_helper_dict = defaultdict(list)
sp_acc_eq = {}
def build_acc_data(accessions, gene_name):
    """ For a list of accessions associated with a SwissProt entry name, 
    adds primary accession and uuid to equivalence dictionary. Builds acc_helper_dict to 
    map each accession to entry name(s). """
    # turn list into a queue
    q = deque(accessions)
    # primary accession name is first one on the queue
    primary = q.popleft()
    for item in q:
        acc_helper_dict[item].append(gene_name)
    # map every primary one-to-one with SP entry uuid
    uid = sp_eq.get(gene_name)
    sp_acc_eq[primary] = uid

# try to factor this out and merge into build_acc_data
def swiss_accessions_eq():
    """ Adds SwissProt seconday accessions and uuids to equivalence dict,
    assigning new uuid if accession is associated with more than one entry name. """
    for sec_acc_id, v in acc_helper_dict.items():
        # only maps to one primary accession, same uuid
        if len(v) == 1:
            uid = sp_eq.get(v[0])
        # maps to > 1 primary accession, give it a new uuid.
        else:
            uid = uuid.uuid4()
        sp_acc_eq[sec_acc_id] = uid

def build_refseq(d):
    """ Uses parsed gene2acc file to build dict mapping (entrez_gene -> refseq status). """
    refseq = {}
    for entrez_gene, status, taxid in d.get_eq_values():
        target_pool = ['9606', '10116', '10090']
        valid_status = ['REVIEWED', 'VALIDATED', 'PROVISIONAL', 'PREDICTED',
                        'MODEL', 'INFERRED']

        if taxid in target_pool and status in valid_status:
            refseq[entrez_gene] = status
    return refseq

def to_entrez(gene_id):
    converted_id = entrez_converter.get(gene_id)
    return converted_id

def write_beleq(eq_dict, filename):
    """ Writes values and uuids from equivalence dictionary to .beleq file. """
    fullname = '.'.join((filename, 'beleq'))
    if len(eq_dict) == 0:
        print('    WARNING: skipping writing ' + fullname + '; no equivalence data found.')
    else:
        with open(fullname, 'w') as f:
            for name, uid in sorted(eq_dict.items()):
                f.write('|'.join((name,str(uid))) + '\n')

