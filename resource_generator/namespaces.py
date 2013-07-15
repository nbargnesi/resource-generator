# coding: utf-8
#
# namespaces.py

import equiv

# namespace dictionaries
entrez_ns_dict = {}
hgnc_ns_dict = {}
mgi_ns_dict = {}
rgd_ns_dict = {}
sp_ns_dict = {}
sp_acc_ns_dict = {}
affy_ns_dict = {}

# miscRNA should not be used here, as it will be handled in a special case.
# For completion sake it is included.
entrez_encoding = {"protein-coding" : "GRP", "miscRNA" : "GR", "ncRNA" : "GR",
                   "snoRNA" : "GR", "snRNA" : "GR", "tRNA" : "GR",
                   "scRNA" : "GR", "other" : "G", "pseudo" : "GR",
                   "unknown" : "GRP", "rRNA" : "GR"}

hgnc_encoding = {"gene with protein product" : "GRP", "RNA, cluster" : "GR",
                 "RNA, long non-coding" : "GR", "RNA, micro" : "GRM",
                 "RNA, ribosomal" : "GR", "RNA, small cytoplasmic" : "GR",
                 "RNA, small misc" : "GR", "RNA, small nuclear" : "GR",
                 "RNA, small nucleolar" : "GR", "RNA, transfer" : "GR",
                 "phenotype only" : "G", "RNA, pseudogene" : "GR",
                 "T cell receptor pseudogene" : "GR",
                 "immunoglobulin pseudogene" : "GR", "pseudogene" : "GR",
                 "T cell receptor gene" : "GRP",
                 "complex locus constituent" : "GRP",
                 "endogenous retrovirus" : "G", "fragile site" : "G",
                 "immunoglobulin gene" : "GRP", "protocadherin" : "GRP",
                 "readthrough" : "GR", "region" : "G",
                 "transposable element" : "G", "unknown" : "GRP",
                 "virus integration site" : "G", "RNA, micro" : "GRM",
                 "RNA, misc" : "GR", "RNA, Y" : "GR", "RNA, vault" : "GR",
                 }

mgi_encoding = {"gene" : "GRP", "protein coding gene" : "GRP",
                "non-coding RNA gene" : "GR", "rRNA gene" : "GR",
                "tRNA gene" : "GR", "snRNA gene" : "GR", "snoRNA gene" : "GR",
                "miRNA gene" : "GRM", "scRNA gene" : "GR",
                "lincRNA gene" : "GR", "RNase P RNA gene" : "GR",
                "RNase MRP RNA gene" : "GR", "telomerase RNA gene" : "GR",
                "unclassified non-coding RNA gene" : "GR",
                "heritable phenotypic marker" : "G", "gene segment" : "G",
                "unclassified gene" : "GRP", "other feature types" : "G",
                "pseudogene" : "GR", "transgene" : "G",
                "other genome feature" : "G", "pseudogenic region" : "GR",
                "polymorphic pseudogene" : "GRP",
                "pseudogenic gene segment" : "GR", "SRP RNA gene" : "GR"}

rgd_encoding = {"gene" : "GRP", "miscrna" : "GR", "predicted-high" : "GRP",
                "predicted-low" : "GRP", "predicted-moderate" : "GRP",
                "protein-coding" : "GRP", "pseudo" : "GR", "snrna" : "GR",
                "trna" : "GR", "rrna" : "GR"}

hgnc_map = {}
mgi_map = {}
rgd_map = {}
def make_namespace(row, parser):

    # build the namespace values (to be refactored later)

    if str(parser) == 'EntrezGeneInfo_Parser':
        gene_id = row.get('GeneID')
        gene_type = row.get('type_of_gene')
        if gene_type == 'miscRNA':
            desc = row.get('description')
            if 'microRNA' in desc:
                entrez_ns_dict[gene_id] = 'GRM'
            else:
                entrez_ns_dict[gene_id] = 'GR'
        else:
            entrez_ns_dict[gene_id] = entrez_encoding[gene_type]

    if str(parser) == 'HGNC_Parser':
        gene_id = row.get('Approved Symbol')
        locus_type = row.get('Locus Type')
        # withdrawn genes not included in this namespace
        if locus_type is not 'withdrawn' and 'withdrawn' not in gene_id:
            hgnc_ns_dict[gene_id] = hgnc_encoding[locus_type]
        hgnc_map[row.get('HGNC ID')] = row.get('Approved Symbol')

    if str(parser) == 'MGI_Parser':
        feature_type = row.get('Feature Type')
        symbol = row.get('Marker Symbol')
        flag = row.get('Marker Type')
        if flag == 'Gene' or flag == 'Pseudogene':
            mgi_ns_dict[symbol] = mgi_encoding[feature_type]
        mgi_map[row.get('MGI Accession ID')] = row.get('Marker Symbol')

    # withdrawn genes are NOT included in this namespace
    if str(parser) == 'RGD_Parser':
        g_type = row.get('GENE_TYPE')
        name = row.get('NAME')
        symbol = row.get('SYMBOL')
        if g_type == 'miscrna' and 'microRNA' in name:
            rgd_ns_dict[symbol] = 'GRM'
        elif g_type == 'miscrna' and 'microRNA' not in name:
            rgd_ns_dict[symbol] = 'GR'
        else:
            if g_type is not '':
                rgd_ns_dict[symbol] = rgd_encoding[g_type]
        rgd_map[row.get('GENE_RGD_ID')] = row.get('SYMBOL')

    if str(parser) == 'SwissProt_Parser':
        gene_name = row.get('name')
        sp_ns_dict[gene_name] = 'GRP'
        accessions = row.get('accessions')
        # build equivalency for SwissProt here, because we have access to the
        # entry from the file being parsed. Maybe move during refactoring.
        equiv.build_sp_eq(row)
        # equivalency for accessions
        equiv.build_acc_data(accessions, gene_name)
        for acc in accessions:
            sp_acc_ns_dict[acc] = 'GRP'

    if str(parser) == 'Affy_Parser':
        # affy equivalence does not need the namespace necessarily, so its ok
        # to compute this now, before namespace is complete.
        equiv.affys(row)
        probe_set_id = row.get('Probe Set ID')
        if probe_set_id not in affy_ns_dict:
            affy_ns_dict[probe_set_id] = 'R'
