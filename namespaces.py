# coding: utf-8

'''
 namespace.py

 Construct each of the .belns files, given a particular dataset.
 This involves gathering all the terms and determining their
 proper encoding.

'''

import parsed

# Encoding dictionaries
# For Entrez and RGD, miscRNA (RNA, small misc) is evaluated together with other
# information to determine 'M' (microRNA) encodings

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

# takes a dataset 'Object' and build namespace
def make_namespace(d, verbose):

    # build and write out the namespace values for each dataset
    ns_dict = {}
    ns_id_dict = {}
    if str(d) == 'entrez_info':
        ns = 'entrez-gene-ids'
        for gene_id, gene_type, description in d.get_ns_values():
            encoding = entrez_encoding.get(gene_type, 'G')
            if gene_type == 'miscRNA' and 'microRNA' in description:
                encoding = 'GRM'
            if gene_type not in entrez_encoding:
                print('WARNING ' + gene_type + ' not defined for Entrez. G assigned as default encoding.')
            ns_dict[gene_id] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'hgnc':
        ns = 'hgnc-approved-symbols'
        for symbol, locus_type, hgnc_id in d.get_ns_values():
            encoding = hgnc_encoding.get(locus_type, 'G')
            if locus_type not in hgnc_encoding:
                print('WARNING ' + locus_type + ' not defined for HGNC. G assigned as default encoding.')
            ns_dict[symbol] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'mgi':
        ns = 'mgi-approved-symbols'
        for marker_symbol, feature_type, acc_id in d.get_ns_values():
            encoding = mgi_encoding.get(feature_type, 'G')
            if feature_type not in mgi_encoding:
                print('WARNING ' + feature_type + ' not defined for MGI. G assigned as default encoding.')
            ns_dict[marker_symbol] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'rgd':
        ns = 'rgd-approved-symbols'
        for symbol, gene_type, name, rgd_id in d.get_ns_values():
            encoding = rgd_encoding.get(gene_type, 'G')
            if gene_type == 'miscrna' and 'microRNA' in name:
                encoding = 'GRM'
            if gene_type not in rgd_encoding:
                print('WARNING ' + gene_type + ' not defined for RGD. G assigned as default encoding.')
            ns_dict[symbol] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'swiss':
        ns = 'swissprot-entry-names'
        ns_id = 'swissprot-accession-numbers'
        encoding = 'GRP'
        for gene_name, accessions in d.get_ns_values():
            ns_dict[gene_name] = encoding
            for acc in accessions:
                ns_id_dict[acc] = encoding
        write_belns(ns_dict, ns)
        write_belns(ns_id_dict, ns_id)

    elif str(d) == 'affy':
        ns = 'affy-probeset-ids'
        encoding = 'R'
        for pid in d.get_ns_values():
            ns_dict[pid] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'chebi':
        ns = 'chebi-names'
        ns_id = 'chebi-ids'
        encoding = 'A'
        for name, primary_id, altids in d.get_ns_values():
            ns_dict[name] = encoding
            ns_id_dict[primary_id] = encoding
            for i in altids:
                ns_id_dict[i] = encoding
        write_belns(ns_dict, ns)
        write_belns(ns_id_dict, ns_id)

    elif str(d) == 'pubchem_namespace':
        ns_id = 'pubchem'
        encoding = 'A'
        for pid in d.get_ns_values():
            ns_id_dict[pid] = encoding
        write_belns(ns_id_dict, ns_id)

    elif str(d) == 'gobp':
        ns = 'go-biological-processes-names'
        ns_id = 'go-biological-processes-ids'
        encoding = 'B'
        for termid, termname, altids in d.get_ns_values():
            ns_dict[termname] = encoding
            ns_id_dict[termid] = encoding
            if altids is not None:
                for i in altids:
                    ns_id_dict[i] = encoding
        write_belns(ns_dict, ns)
        write_belns(ns_id_dict, ns_id)

    elif str(d) == 'gocc':
        ns = 'go-cellular-component-names'
        ns_id = 'go-cellular-component-ids'
        for termid, termname, altids, complex in d.get_ns_values():
            if complex:
                encoding = 'C'
            else:
                encoding = 'A'
            ns_dict[termname] = encoding
            ns_id_dict[termid] = encoding
            if altids is not None:
                for i in altids:
                    ns_id_dict[i] = encoding
        write_belns(ns_dict, ns)
        write_belns(ns_id_dict, ns_id)

    elif str(d) == 'schem':
        ns = 'selventa-legacy-chemical-names'
        encoding = 'A'
        for entry in d.get_ns_values():
            ns_dict[entry] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'sdis':
        ns = 'selventa-legacy-diseases'
        encoding = 'O'
        for entry in d.get_ns_values():
            ns_dict[entry] = encoding
        write_belns(ns_dict, ns)

    elif str(d) == 'mesh':
        ns = 'mesh-cellular-locations'
        ns2 = 'mesh-diseases'
        ns2_dict = {}
        ns3 = 'mesh-biological-processes'
        ns3_dict = {}
        for ui, mh, mns, sts in d.get_ns_values():
            if any(branch.startswith('A11.284') for branch in mns):
                # MeSH Cellular Locations; encoding = 'A'
                ns_dict[mh] = 'A'
            if any(branch.startswith('C') for branch in mns):
                # MeSH Diseases; encoding = 'O'
                ns2_dict[mh] = 'O'
            if any(branch.startswith('G') for branch in mns):
                # MeSH Phenomena and Processes; encoding = 'B'
                excluded = ('G01', 'G02', 'G15', 'G17')
                if not all(branch.startswith(excluded) for branch in mns):
                    ns3_dict[mh] = 'B'
        write_belns(ns_dict, ns)
        write_belns(ns2_dict, ns2)
        write_belns(ns3_dict, ns3)

    elif str(d) == 'do':
        ns = 'disease-ontology-names'
        ns_id = 'disease-ontology-ids'
        encoding = 'O'
        for name, id in d.get_ns_values():
            ns_dict[name] = encoding
            ns_id_dict[id] = encoding
        write_belns(ns_dict, ns)
        write_belns(ns_id_dict, ns_id)

def write_belns(ns_dict, filename):
    """ Writes values and encodings from namespace dict to .belns file. """
    fullname = '.'.join((filename, 'belns'))
    with open(fullname, 'w') as f:
        for name, encoding in sorted(ns_dict.items()):
            f.write('|'.join((name, encoding)) + '\n')
