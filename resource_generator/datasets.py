# coding: utf-8
#
# datasets.py

# Represent each parsed dataset as an object. This is
# really just a wrapper to the underlying dictionaries.

import ipdb

class DataSet():
    def __init__(self, dictionary):
        self.dict = dictionary

    def get_dictionary(self):
        return self.dict

    def __str__(self):
        return 'DataSet_Object'


class EntrezInfoData(DataSet):

    def __init__(self, dictionary):
        super(EntrezInfoData, self).__init__(dictionary)
        self.entrez_info_dict = dictionary

    def get_dictionary(self):
        return self.entrez_info_dict

    def get_ns_values(self):
        for gene_id in self.entrez_info_dict:
            mapping = self.entrez_info_dict.get(gene_id)
            gene_type = mapping.get('type_of_gene')
            description = mapping.get('description')
            yield gene_id, gene_type, description

    def get_eq_values(self):
        for gene_id in self.entrez_info_dict:
            yield gene_id

    def __str__(self):
        return 'entrez_info'


class EntrezHistoryData(DataSet):

    def __init__(self, dictionary):
        super(EntrezHistoryData, self).__init__(dictionary)
        self.entrez_history_dict = dictionary

    def get_dictionary(self):
        return self.entrez_history_dict

    def get_ns_values(self):
        for gene_id in self.entrez_history_dict:
            mapping = self.entrez_history_dict.get(gene_id)
            gene_type = mapping.get('type_of_gene')
            description = mapping.get('description')
            yield gene_id, gene_type, description

    def __str__(self):
        return 'entrez_history'


class HGNCData(DataSet):

    def __init__(self, dictionary):
        super(HGNCData, self).__init__(dictionary)
        self.hgnc_dict = dictionary

    def get_dictionary(self):
        return self.hgnc_dict

    def get_ns_values(self):
        for symbol in self.hgnc_dict:
            mapping = self.hgnc_dict.get(symbol)
            loc_type = mapping.get('Locus Type')
            hgnc_id = mapping.get('HGNC ID')
            yield symbol, loc_type, hgnc_id

    def get_eq_values(self):
        for approved_symbol in self.hgnc_dict:
            yield approved_symbol

    def __str__(self):
        return 'hgnc'


class MGIData(DataSet):

    def __init__(self, dictionary):
        super(MGIData, self).__init__(dictionary)
        self.mgi_dict = dictionary

    def get_dictionary(self):
        return self.mgi_dict

    def get_ns_values(self):
        for marker_symbol in self.mgi_dict:
            mapping = self.mgi_dict.get(marker_symbol)
            feature_type = mapping.get('Feature Type')
            acc_id = mapping.get('MGI Accession ID')
            marker_type = mapping.get('Marker Type')
            yield marker_symbol, feature_type, acc_id, marker_type

    def get_eq_values(self):
        for marker_symbol in self.mgi_dict:
            yield marker_symbol

    def __str__(self):
        return 'mgi'


class RGDData(DataSet):

    def __init__(self, dictionary):
        super(RGDData, self).__init__(dictionary)
        self.rgd_dict = dictionary

    def get_dictionary(self):
        return self.rgd_dict

    def get_ns_values(self):
        for symbol in self.rgd_dict:
            mapping = self.rgd_dict.get(symbol)
            name = mapping.get('NAME')
            gene_type = mapping.get('GENE_TYPE')
            rgd_id = mapping.get('GENE_RGD_ID')
            yield symbol, gene_type, name, rgd_id

    def get_eq_values(self):
        for symbol in self.rgd_dict:
            yield symbol

    def __str__(self):
        return 'rgd'


class SwissProtData(DataSet):

    def __init__(self, dictionary):
        super(SwissProtData, self).__init__(dictionary)
        self.sp_dict = dictionary

    def get_dictionary(self):
        return self.sp_dict

    def get_ns_values(self):
        for name in self.sp_dict:
            mapping = self.sp_dict.get(name)
            acc = mapping.get('accessions')
            yield name, acc

    def get_eq_values(self):
        for name in self.sp_dict:
            mapping = self.sp_dict.get(name)
            dbrefs = mapping.get('dbreference')
            acc = mapping.get('accessions')
            yield name, dbrefs, acc

    def __str__(self):
        return 'swiss'


# class SwissProtAccData(DataSet):

#     def __init__(self, dictionary):
#         super(SwissProtAccData, self).__init__(dictionary)
#         self.sp_acc_dict = dictionary

#     def get_dictionary(self):
#         return self.sp_acc_dict

#     def get_ns_values(self):
#         for acc_id in self.sp_acc_dict:
#             yield acc_id

#     def __str__(self):
#         return 'swiss'


class AffyData(DataSet):

    def __init__(self, dictionary):
        super(AffyData, self).__init__(dictionary)
        self.affy_dict = dictionary

    def get_dictionary(self):
        return self.affy_dict

    def get_ns_values(self):
        for probe_id in self.affy_dict:
            yield probe_id

    def get_eq_values(self):
        for probe_id in self.affy_dict:
            mapping = self.affy_dict.get(probe_id)
            gene_id  = mapping.get('Entrez Gene')
            yield probe_id, gene_id

    def __str__(self):
        return 'affy'


class CHEBIData(DataSet):

    def __init__(self, dictionary):
        super(CHEBIData, self).__init__(dictionary)
        self.chebi_dict = dictionary

    def get_dictionary(self):
        return self.chebi_dict

    def get_ns_values(self):
        for name in self.chebi_dict:
            mapping = self.chebi_dict.get(name)
            primary_id = mapping.get('primary_id')
            altIds = mapping.get('alt_ids')
            yield name, primary_id, altIds

    def get_names(self):
        for name in self.chebi_dict:
            yield name

    def get_primary_ids(self):
        for name in self.chebi_dict:
            mapping = self.chebi_dict.get(name)
            primary_id = mapping.get('primary_id')
            yield primary_id

    def get_alt_ids(self):
        for name in self.chebi_dict:
            mapping = self.chebi_dict.get(name)
            altIds = mapping.get('alt_ids')
            if altIds is not None:
                for alt in altIds:
                    yield alt

    def alt_to_primary(self, alt):
        for name in self.chebi_dict:
            mapping = self.chebi_dict.get(name)
            altIds = mapping.get('alt_ids')
            if alt in altIds:
                primary_id = mapping.get('primary_id')
                yield primary_id

    def name_to_primary(self, name):
        mapping = self.chebi_dict.get(name)
        primary_id = mapping.get('primary_id')
        yield primary_id

    def __str__(self):
        return 'chebi'


class SCHEMData(DataSet):

    def __init__(self, dictionary):
        super(SCHEMData, self).__init__(dictionary)
        self.schem_dict = dictionary

    def get_dictionary(self):
        return self.schem_dict

    def get_ns_values(self):
        for entry in self.schem_dict:
            yield entry

    def __str__(self):
        return 'schem'


class SCHEMtoCHEBIData(DataSet):

    def __init__(self, dictionary):
        super(SCHEMtoCHEBIData, self).__init__(dictionary)
        self.schem_to_chebi = dictionary

    def get_dictionary(self):
        return self.schem_to_chebi

    def has_equivalence(self, schem_name):
        equiv = False
        for schem_term in self.schem_to_chebi:
            mapping = self.schem_to_chebi.get(schem_term)
            chebi_name = mapping.get('CHEBI_name')
            # if schem_name == '(-)-Catechin':
            #     ipdb.set_trace()
#            ipdb.set_trace()
            if schem_name.lower() == chebi_name.lower():
                equiv = True
        return equiv

    def get_equivalence(self, schem_id):
        mapping = self.schem_to_chebi.get(schem_id)
        chebi_name = mapping.get('CHEBI_name')
        return chebi_name

    def __str__(self):
        return 'schem_to_chebi'


class PubNamespaceData(DataSet):

    def __init__(self, dictionary):
        super(PubNamespaceData, self).__init__(dictionary)
        self.pub_dict = dictionary

    def get_dictionary(self):
        return self.pub_dict

    def get_ns_values(self):
        for pid in self.pub_dict:
            yield pid

    def __str__(self):
        return 'pubchem_namespace'


class PubEquivData(DataSet):

    def __init__(self, dictionary):
        super(PubEquivData, self).__init__(dictionary)
        self.pub_eq_dict = dictionary

    def get_dictionary(self):
        return self.pub_eq_dict

    def get_eq_values(self):
        for sid in self.pub_eq_dict:
            mapping = self.pub_eq_dict.get(sid)
            source = mapping.get('Source')
            cid = mapping.get('PubChem CID')

            yield sid, source, cid

    def __str__(self):
        return 'pubchem_equiv'


class Gene2AccData(DataSet):

    def __init__(self, dictionary):
        super(Gene2AccData, self).__init__(dictionary)
        self.g2a_dict = dictionary

    def get_dictionary(self):
        return self.g2a_dict

    def get_eq_values(self):
        for entrez_gene in self.g2a_dict:
            mapping = self.g2a_dict.get(entrez_gene)
            status = mapping.get('status')
            taxid = mapping.get('tax_id')
            yield entrez_gene, status, taxid

    def __str__(self):
        return 'gene2acc'


class GOBPData(DataSet):

    def __init__(self, dictionary):
        super(GOBPData, self).__init__(dictionary)
        self.gobp_dict = dictionary

    def get_dictionary(self):
        return self.gobp_dict

    def get_ns_values(self):
        for termid in self.gobp_dict:
            mapping = self.gobp_dict.get(termid)
            termname = mapping.get('termname')
            altids = mapping.get('altids')

            yield termid, termname, altids

    def get_eq_values(self):
        for termid in self.gobp_dict:
            mapping = self.gobp_dict.get(termid)
            termname = mapping.get('termname')

            yield termid, termname

    def __str__(self):
        return 'gobp'


class GOCCData(DataSet):

    def __init__(self, dictionary):
        super(GOCCData, self).__init__(dictionary)
        self.gocc_dict = dictionary

    def get_dictionary(self):
        return self.gocc_dict

    def get_ns_values(self):
        for termid in self.gocc_dict:
            mapping = self.gocc_dict.get(termid)
            termname = mapping.get('termname')
            complex = mapping.get('complex')
            altids = mapping.get('altids')

            yield termid, termname, altids, complex

    def get_eq_values(self):
        for termid in self.gocc_dict:
            mapping = self.gocc_dict.get(termid)
            termname = mapping.get('termname')

            yield termid, termname

    def __str__(self):
        return 'gocc'


class MESHData(DataSet):

    def __init__(self, dictionary):
        super(MESHData, self).__init__(dictionary)
        self.mesh_dict = dictionary

    def get_dictionary(self):
        return self.mesh_dict

    def get_ns_values(self):
        for ui in self.mesh_dict:
            mapping = self.mesh_dict.get(ui)
            mh = mapping.get('mesh_header')
            mns = mapping.get('mns')
            sts = mapping.get('sts')

            yield ui, mh, mns, sts

    def get_eq_values(self):
        for ui in self.mesh_dict:
            mapping = self.mesh_dict.get(ui)
            mh = mapping.get('mesh_header')
            mns = mapping.get('mns')
            synonyms = mapping.get('synonyms')

            yield ui, mh, mns, synonyms

    def __str__(self):
        return 'mesh'


class SwissWithdrawnData(DataSet):

    def __init__(self, dictionary):
        super(SwissWithdrawnData, self).__init__(dictionary)
        self.s_dict = dictionary

    def get_dictionary(self):
        return self.s_dict

    def get_withdrawn_accessions(self):
        accessions = self.s_dict.get('accessions')
        return accessions
        # for acc in accessions:
        #     yield acc

    def __str__(self):
        return 'swiss-withdrawn'
