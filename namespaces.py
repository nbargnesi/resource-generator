# coding: utf-8

'''
 namespace.py

 Construct each of the .belns files, given a particular dataset.
 This involves gathering all the terms and determining their
 proper encoding.

'''

import parsed

# namespace dictionaries
entrez_ns = set()
hgnc_ns = set()
mgi_ns  = set()
rgd_ns = set()
sp_ns = set()
sp_acc_ns = set()
affy_ns = set()
chebi_name_ns = set()
chebi_id_ns = set()
pub_ns = set()
do_ns = set()

# miscRNA should not be used here, as it will be handled in a special case.
# For completion sake it is included.
entrez_encoding = {'protein-coding' : 'GRP', 'miscRNA' : 'GR', 'ncRNA' : 'GR',
                   'snoRNA' : 'GR', 'snRNA' : 'GR', 'tRNA' : 'GR',
                   'scRNA' : 'GR', 'other' : 'G', 'pseudo' : 'GR',
                   'unknown' : 'GRP', 'rRNA' : 'GR'}

hgnc_encoding = {'gene with protein product' : 'GRP', 'RNA, cluster' : 'GR',
                 'RNA, long non-coding' : 'GR', 'RNA, micro' : 'GRM',
                 'RNA, ribosomal' : 'GR', 'RNA, small cytoplasmic' : 'GR',
                 'RNA, small misc' : 'GR', 'RNA, small nuclear' : 'GR',
                 'RNA, small nucleolar' : 'GR', 'RNA, transfer' : 'GR',
                 'phenotype only' : 'G', 'RNA, pseudogene' : 'GR',
                 'T cell receptor pseudogene' : 'GR',
                 'immunoglobulin pseudogene' : 'GR', 'pseudogene' : 'GR',
                 'T cell receptor gene' : 'GRP',
                 'complex locus constituent' : 'GRP',
                 'endogenous retrovirus' : 'G', 'fragile site' : 'G',
                 'immunoglobulin gene' : 'GRP', 'protocadherin' : 'GRP',
                 'readthrough' : 'GR', 'region' : 'G',
                 'transposable element' : 'G', 'unknown' : 'GRP',
                 'virus integration site' : 'G', 'RNA, micro' : 'GRM',
                 'RNA, misc' : 'GR', 'RNA, Y' : 'GR', 'RNA, vault' : 'GR',
                 }

mgi_encoding = {'gene' : 'GRP', 'protein coding gene' : 'GRP',
                'non-coding RNA gene' : 'GR', 'rRNA gene' : 'GR',
                'tRNA gene' : 'GR', 'snRNA gene' : 'GR', 'snoRNA gene' : 'GR',
                'miRNA gene' : 'GRM', 'scRNA gene' : 'GR',
                'lincRNA gene' : 'GR', 'RNase P RNA gene' : 'GR',
                'RNase MRP RNA gene' : 'GR', 'telomerase RNA gene' : 'GR',
                'unclassified non-coding RNA gene' : 'GR',
                'heritable phenotypic marker' : 'G', 'gene segment' : 'G',
                'unclassified gene' : 'GRP', 'other feature types' : 'G',
                'pseudogene' : 'GR', 'transgene' : 'G',
                'other genome feature' : 'G', 'pseudogenic region' : 'GR',
                'polymorphic pseudogene' : 'GRP',
                'pseudogenic gene segment' : 'GR', 'SRP RNA gene' : 'GR'}

rgd_encoding = {'gene' : 'GRP', 'miscrna' : 'GR', 'predicted-high' : 'GRP',
                'predicted-low' : 'GRP', 'predicted-moderate' : 'GRP',
                'protein-coding' : 'GRP', 'pseudo' : 'GR', 'snrna' : 'GR',
                'trna' : 'GR', 'rrna' : 'GR'}

hgnc_map = {}
mgi_map = {}
rgd_map = {}
# takes a dataset 'Object' and build namespace
def make_namespace(d, verbose):

    # build and write out the namespace values for each dataset

    delim = '|'
    if str(d) == 'entrez_info':
        with open('entrez-gene-ids.belns', 'w') as fp:
            # tuple of (gene_id, gene_type, description)
            for vals in d.get_ns_values():
                gene_id, gene_type, description = vals
                if gene_type == 'miscRNA':
                    if 'microRNA' in description:
                        fp.write(delim.join((gene_id, 'GRM'))+'\n')
                        entrez_ns.add(gene_id)
                    else:
                        fp.write(delim.join((gene_id, 'GR'))+'\n')
                        entrez_ns.add(gene_id)
                else:
                    fp.write(delim.join((gene_id, entrez_encoding[gene_type]))+'\n')
                    entrez_ns.add(gene_id)

    elif str(d) == 'hgnc':
        with open('hgnc-approved-symbols.belns', 'w') as fp:
            for vals in d.get_ns_values():
                approved_symb, locus_type, hgnc_id = vals
                # withdrawn genes NOT included in this namespace
                if locus_type is not 'withdrawn' and 'withdrawn' not in approved_symb:
                    fp.write(delim.join((approved_symb, hgnc_encoding[locus_type]))+'\n')
                    hgnc_ns.add(approved_symb)
                hgnc_map[hgnc_id] = approved_symb

    elif str(d) == 'mgi':
        with open('mgi-approved-symbols.belns', 'w') as fp:
            for vals in d.get_ns_values():
                marker_symbol, feature_type, acc_id, marker_type = vals
                if marker_type == 'Gene' or marker_type == 'Pseudogene':
                    fp.write(delim.join((marker_symbol, mgi_encoding[feature_type]))+'\n')
                    mgi_ns.add(marker_symbol)
                mgi_map[acc_id] = marker_symbol

    # withdrawn genes are NOT included in this namespace
    elif str(d) == 'rgd':
        with open('rgd-approved-symbols.belns', 'w') as fp:
            for vals in d.get_ns_values():
                symbol, gene_type, name, rgd_id = vals
                if gene_type == 'miscrna' and 'microRNA' in name:
                    fp.write(delim.join((symbol, 'GRM'))+'\n')
                    rgd_ns.add(symbol)
                elif gene_type == 'miscrna' and 'microRNA' not in name:
                    fp.write(delim.join((symbol, 'GR'))+'\n')
                    rgd_ns.add(symbol)
                else:
                    if gene_type is not '':
                        fp.write(delim.join((symbol, rgd_encoding[gene_type]))+'\n')
                        rgd_ns.add(symbol)
                rgd_map[rgd_id] = symbol

    elif str(d) == 'swiss':
        with open('swissprot-entry-names.belns', 'w') as fp, \
                open('swissprot-accession-numbers.belns', 'w') as f:
            for vals in d.get_ns_values():
                gene_name, accessions = vals
                fp.write(delim.join((gene_name, 'GRP'))+'\n')
                sp_ns.add(gene_name)
                for acc in accessions:
                    f.write(delim.join((acc, 'GRP'))+'\n')
                    sp_acc_ns.add(acc)

    elif str(d) == 'affy':
        with open('affy-probeset-ids.belns', 'w') as fp:
            for vals in d.get_ns_values():
                pid = vals
                fp.write(delim.join((pid, 'R'))+'\n')
#                    if pid not in affy_ns_dict:
#                        affy_ns_dict[pid] = 'R'

    elif str(d) == 'chebi':
        with open('chebi-names.belns', 'w') as fp, \
                open('chebi-ids.belns', 'w') as f:
            for vals in d.get_ns_values():
                name, primary_id, altIds = vals
                fp.write(delim.join((name, 'A'))+'\n')
                chebi_name_ns.add(name)
                f.write(delim.join((primary_id, 'A'))+'\n')
                chebi_id_ns.add(name)
                if altIds:
                    for i in altIds:
                        if i not in chebi_id_ns:
                            f.write(delim.join((i, 'A'))+'\n')
                        chebi_id_ns.add(i)

    elif str(d) == 'pubchem_namespace':
        with open('pubchem-ids.belns', 'w') as fp:
            for vals in d.get_ns_values():
                pid = vals
                fp.write(delim.join((pid, 'A'))+'\n')
                pub_ns.add(pid)

    elif str(d) == 'gobp':
        with open('go-biological-processes-names.belns', 'w') as gobp, \
                open('go-biological-processes-accession-numbers.belns', 'w') \
                as gobp_id:
            for vals in d.get_ns_values():
                termid, termname, altids = vals
                gobp.write(delim.join((termname, 'B'))+'\n')
                gobp_id.write(delim.join((termid, 'B'))+'\n')
                if altids is not None:
                    for alt in altids:
                        gobp_id.write(delim.join((alt, 'B'))+'\n')

    elif str(d) == 'gocc':

        with open('go-cellular-component-terms.belns', 'w') as gocc, \
                open('go-cellular-component-accession-numbers.belns', 'w') \
                as gocc_id:
            for vals in d.get_ns_values():
                termid, termname, altids, complex = vals
                if complex:
                    gocc.write(delim.join((termname, 'C'))+'\n')
                    gocc_id.write(delim.join((termid, 'C'))+'\n')
                    for alt in altids:
                        gocc_id.write(delim.join((alt, 'C'))+'\n')
                else:
                    gocc.write(delim.join((termname, 'A'))+'\n')
                    gocc_id.write(delim.join((termid, 'A'))+'\n')
                    if altids is not None:
                        for alt in altids:
                            gocc_id.write(delim.join((alt, 'A'))+'\n')

    elif str(d) == 'schem':
        schem_to_chebi = parsed.load_data('schem_to_chebi')
        count = 0
        with open('selventa-legacy-chemical-names.belns', 'w') as f:
            for entry in d.get_ns_values():
                # try to get a chebi equivalent, if there is one do not
                # write this value to the new namespace
                if schem_to_chebi.has_equivalence(entry):
                    count = count + 1
                    continue
                else:
                    f.write(delim.join((entry, 'A'))+'\n')
        if verbose:
            print('Able to resolve ' +str(count)+ ' SCHEM names to CHEBI.')

    elif str(d) == 'sdis':
        sdis_to_do = parsed.load_data('sdis_to_do')
        count = 0
        with open('selventa-legacy-diseases.belns', 'w') as f:
            for entry in d.get_ns_values():
                # try to get a do equivalent, if there is one do not
                # write this value to the new namespace
                if sdis_to_do.has_equivalence(entry):
                    count = count + 1
                    continue
                else:
                    f.write(delim.join((entry, 'O'))+'\n')
        if verbose:
            print('Able to resolve ' +str(count)+ ' SDIS names to DO.')

    elif str(d) == 'mesh':

        with open('mesh-cellular-locations.belns', 'w') as meshf, \
                open('mesh-diseases.belns', 'w') as meshd, \
                open('mesh-biological-processes.belns', 'w') as meshb:
            for vals in d.get_ns_values():
                ui, mh, mns, sts = vals
                # all entries from A11.284 branch (abundances)
                if any('A11.284' in branch for branch in mns):
                    meshf.write(delim.join((mh, 'A'))+'\n')
                # all entries from the C branch (pathology)
                elif any('C' in branch for branch in mns):
                    meshd.write(delim.join((mh, 'O'))+'\n')
                # G branch (bio process) - exclude G01 G02 G15 G17 branches
                elif any('G' in branch for branch in mns):
                    excluded = False
                    for branch in mns:
                        if branch.startswith('MN = G01') \
                                or branch.startswith('MN = G02') \
                                or branch.startswith('MN = G15') \
                                or branch.startswith('MN = G17'):
                            excluded = True
                    if not excluded:
                        meshb.write(delim.join((mh, 'B'))+'\n')

    elif str(d) == 'do':

        with open('disease-ontology-names.belns', 'w') as dn, \
                open('disease-ontology-ids.belns', 'w') as di:
            for vals in d.get_ns_values():
                name, id = vals
                dn.write(delim.join((name, 'O'))+'\n')
                di.write(delim.join((id, 'O'))+'\n')
