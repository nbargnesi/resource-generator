# coding: utf-8
#
# datasets.py

# Represent each parsed dataset as an object. This is
# really just a wrapper to the underlying dictionaries.

import ipdb

class DataSet(object):
    def __init__(self, dictionary):
        self.dict = dictionary

    def get_dictionary(self):
        pass

    def __str__(self):
        return 'DataSet_Object'


class EntrezData(DataSet):

    def __init__(self, dictionary):
        super(EntrezData, self).__init__(dictionary)
        self.entrez_dict = dictionary

    def get_dictionary(self):
        return self.entrez_dict

    def get_ns_values(self):
        for gene_id in self.entrez_dict:
            mapping = self.entrez_dict.get(gene_id)
            gene_type = mapping.get('type_of_gene')
            description = mapping.get('description')
            yield gene_id, gene_type, description

    def __str__(self):
        return 'entrez_info'


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

    def __str__(self):
        return 'chebi'


class PUBCHEMData(DataSet):

    def __init__(self, dictionary):
        super(PUBCHEMData, self).__init__(dictionary)
        self.pub_dict = dictionary

    def get_dictionary(self):
        return self.pub_dict

    def get_ns_values(self):
        for pid in self.pub_dict:
            yield pid

    def __str__(self):
        return 'pubchem'
