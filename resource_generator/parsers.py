# coding: utf-8

from common import gzip_to_text
from lxml import etree
import csv
import gzip
import uuid

class Parser(object):
    def __init__(self, file_to_url):
        self.file_to_url = file_to_url

    def parse():
        pass

class EntrezGeneInfoParser(Parser):
    resourceLocation = "http://resource.belframework.org/belframework/1.0/namespace/entrez-gene-ids-hmr.belns"

    def __init__(self, file_to_url):
        super(EntrezGeneInfoParser, self).__init__(file_to_url)
        file_keys = iter(file_to_url.keys())
        self.entrez_gene_info = next(file_keys)
   
    def parse(self):

        # define a csv reader object
        info_csvreader = csv.reader(gzip_to_text(self.entrez_gene_info), delimiter="\t", quotechar="\"")
        self.columns_for_gene_info = ["tax_id", "GeneID", "Symbol", "LocusTag", "Synonyms", "dbXrefs", \
                                      "chromosome", "map_location", "description", "type_of_gene", \
                                      "Symbol_from_nomenclature_authority", \
                                      "Full_name_from_nomenclature_authority", "Nomenclature_status", \
                                      "Other_designations", "Modification_date"]

         # Dictionary for base gene info
        info_dict = {}
        
        for row in info_csvreader:
            if row[0] in ("9606", "10090", "10116"):
                for index, item in enumerate(self.columns_for_gene_info):
                    info_dict[item] = row[index]
                    yield info_dict

    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneInfo_Parser"

class EntrezGeneHistoryParser(Parser):
    resourceLocation = """"http://resource.belframework.org/belframework/1.0/namespace/
                           entrez-gene-ids-hmr.belns"""

    def __init__(self, file_to_url):
        super(EntrezGeneHistoryParser, self).__init__(file_to_url)
        file_keys = iter(file_to_url.keys())
        self.entrez_gene_history = next(file_keys)

    def parse(self):

        # define a csv reader object
        history_csvreader =  csv.reader(gzip_to_text(self.entrez_gene_history), delimiter="\t", 
                                        quotechar="\"")

        self.columns_for_gene_history = ["tax_id", "GeneID", "Discontinued_GeneID", "Discontinued_Symbol", \
                                              "Discontinued_Date"]

         # Dictionary for base gene info
        history_dict = {}
        
        for row in history_csvreader:
            if row[0] in ("9606", "10090", "10116"):
                for index, item in enumerate(self.columns_for_gene_history):
                    history_dict[item] = row[index]
                    yield history_dict
 
    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneHistory_Parser"

class HGNCParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/namespace/
                          hgnc-approved-symbols.belns"""

    def __init__(self, file_to_url):
        super(HGNCParser, self).__init__(file_to_url)
        self.hgnc_file = next(iter(file_to_url.keys()))

    def parse(self):
        # use iso-8859-1 as default encoding.
        with open(self.hgnc_file, "r", encoding="iso-8859-1") as hgncf:
            # open csv file
            hgnc_csvr = csv.reader(hgncf, delimiter="\t", quotechar="\"")

            # columns from the HGNC dataset
            self.hgnc_column_headers = ["HGNC ID", "Approved Symbol", "Approved Name", "Status", \
                               "Locus Type", "Locus Group", "Previous Symbols", "Previous Names", \
                               "Synonyms", "Name Synonyms", "Chromosome", "Date Approved", \
                               "Date Modified", "Date Symbol Changed", "Date Name Changed", \
                               "Accession Numbers", "Enzyme IDs", "Entrez0 Gene ID", "Ensembl Gene ID", \
                               "Mouse Genome Database ID", "Specialist Database Links", \
                               "Specialist Database IDs", "Pubmed IDs", "RefSeq IDs", "Gene Family Tag", \
                               "Gene family description", "Record Type", "Primary IDs", "Secondary IDs", \
                               "CCDS IDs", "VEGA IDs", "Locus Specific Databases", "Entrez1 gene ID", \
                               "OMIM ID", "RefSeq", "UniProtID", "Ensembl ID", "UCSC ID", \
                               "Mouse Genome Database ID", "Rat Genome Database ID"]

            temp_dict = dict()
            for row in hgnc_csvr:
                for index, item in enumerate(self.hgnc_column_headers):
                    temp_dict[item] = row[index]
                    yield temp_dict

    def __str__(self):
        return "HGNC_Parser"

class MGIParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/namespace/
                          mgi-approved-symbols.belns"""

    def __init__(self, file_to_url):
        super(MGIParser, self).__init__(file_to_url)
        self.mgi_file = next(iter(file_to_url.keys()))

    def parse(self):
        with open(self.mgi_file, "r") as mgif:
            # open csv file
            mgi_csvr = csv.reader(mgif, delimiter="\t", quotechar="\"")

           # columns from the MGI dataset
            mgi_column_headers = ["MGI Marker Accession ID", "Chr", "cM Position", \
                                       "genome coordinate start", "genome coordinate end", \
                                       "strand", "Marker Symbol", "Status", "Marker Name", \
                                       "Marker Type", "Feature Type", \
                                       "Marker Synonyms (pipe-separated)"]

            temp_dict = dict()
            for row in mgi_csvr:
                for index, item in enumerate(mgi_column_headers):
                    temp_dict[item] = row[index]
                    yield temp_dict

    def __str__(self):
        return "MGI_Parser"

class RGDParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/namespace/
                          rgd-approved-symbols.belns""" 

    def __init__(self, file_to_url):
        super(RGDParser, self).__init__(file_to_url)
        self.rgd_file = next(iter(file_to_url.keys()))

    def parse(self):
        with open(self.rgd_file, "r") as rgdf:
            # open csv file
            rgd_csvr = csv.reader(rgdf, delimiter="\t", quotechar="\"")

           # columns from the RGD dataset
            rgd_column_headers = ["GENE_RGD_ID", "SYMBOL", "NAME", "GENE_DESC", "CHROMOSOME_CELERA", \
                                  "CHROMOSOME_3.1", "CHROMOSOME_3.4", "FISH_BAND", "START_POS_CELERA", \
                                  "STOP_POS_CELERA", "STRAND_CELERA", "START_POS_3.1", "STOP_POS_3.1", \
                                  "STRAND_3.1", "START_POS_3.4", "STOP_POS_3.4", "STRAND_3.4", \
                                  "CURATED_REF_RGD_ID", "CURATED_REF_PUBMED_ID", "UNCURATED_PUBMED_ID", \
                                  "ENTREZ_GENE", "UNIPROT_ID", "UNUSED", "GENBANK_NUCLEOTIDE", \
                                  "TIGR_ID", "GENBANK_PROTEIN", "UNIGENE_ID", "SSLP_RGD_ID", \
                                  "SSLP_SYMBOL", "OLD_SYMBOL", "OLD_NAME", "QTL_RGD_ID", "QTL_SYMBOL", \
                                  "NOMENCLATURE_STATUS", "SPLICE_RGD_ID", "SPLICE_SYMBOL", "GENE_TYPE", \
                                  "ENSEMBL_ID", "GENE_REFSEQ_STATUS", "UNUSED_OTHER"]

            temp_dict = dict()
            # RGD file contains ~40-50 lines of comments that begin with '#', so skip all of these.
            for row in rgd_csvr:
                if row[0] != '#' and str(row[0]).isdigit():
                    for index, item in enumerate(rgd_column_headers):
                        temp_dict[item] = row[index]
                        yield temp_dict
    
    def __str__(self):
        return "RGD_Parser"

class SwissProtParser(Parser):
    resourceLocation_accession_numbers = "http://resource.belframework.org/belframework/1.0/namespace/swissprot-accession-numbers.belns"
    resourceLocation_entry_names = "http://resource.belframework.org/belframework/1.0/namespace/swissprot-entry-names.belns"

    def __init__(self, file_to_url):
        super(SwissProtParser, self).__init__(file_to_url)
        self.sprot_file = next(iter(file_to_url.keys()))
        self.encoding = "GRP"
        self.entries = {}
        self.accession_numbers = {}
        self.gene_ids = {}
        self.entry_names = set({})

    def parse(self):
        sprot_dict = {}
        with gzip.open(self.sprot_file) as sprotf:
            ctx = etree.iterparse(sprotf, events=('end',), tag='{http://uniprot.org/uniprot}entry')
 
            temp_dict = dict()
            for ev, e in ctx:
                # stop evaluating if this entry is not in the Swiss-Prot dataset
                if e.get("dataset") != "Swiss-Prot":
                    return
                #print ("got here")
                # stop evaluating if this entry is not for human, mouse, or rat
                org = e.find("{http://uniprot.org/uniprot}organism")
                if org is not None:
                    # restrict by NCBI Taxonomy reference
                    dbr = org.find("{http://uniprot.org/uniprot}dbReference")
                   # print("----------------------DEBUG------------------------")
                   # print("----------- NCBI Tax ID :" +dbr.get("id") + " -----")
                   # print("----------------------DEBUG------------------------")
                    if dbr.get("id") not in ("9606", "10090", "10116"):
                        yield temp_dict
                    else:
                        # add NCBI Taxonomy and the id for the entry to the dict
                        temp_dict[dbr.get("type")] = dbr.get("id")
                        
                # get entry name, add it to the dict
                entry_name = e.find("{http://uniprot.org/uniprot}name").text
                temp_dict["name"] = entry_name
                
                # get protein data
                prot = e.find("{http://uniprot.org/uniprot}protein")
                rec_name = prot.find("recommendedName")
                rec_full_name = rec_name.find("fullName").text
                # add recommended name to dict
                temp_dict["recommendedName"] = rec_full_name
                alt_names = []
                # add each alternate name to the list, then put in the dict
                for alternate_name in prot.findall("alternateName"):
                    for full_name in alternate_name:
                        alt_names.append(full_name.text)
                temp_dict["alternateNames"] = alt_names

                # get gene data
                names = []
                gene = e.find("{http://uniprot.org/uniprot}gene")
                for name in gene.find("name"):
                    if name.get("type") == "primary":
                        temp_dict["primary"] = name.text
                    if name.get("type") == "synonym":
                        names.apped(name.text)
                # add gene data to the dict
                temp_dict["synonyms"] = names

                # get all accessions
                entry_accessions = []
                for entry_accession in e.findall("{http://uniprot.org/uniprot}accession"):
                    acc = entry_accession.text
                    entry_accessions.append(acc)
                    if acc in self.accession_numbers:
                        self.accession_numbers[acc] = None
                    else:
                        self.accession_numbers[acc] = 1

                # add the array of accessions to the dict
                temp_dict["accessions"] = entry_accessions
                    
                type_set = ["GeneId", "MGI", "HGNC", "RGD"]
                entry_gene_ids = []
                for dbr in e.findall("{http://uniprot.org/uniprot}dbReference"):
                    if dbr.get("type") in type_set:
                        gene_id = dbr.get("id")
                        entry_gene_ids.append(gene_id)
                        if gene_id in self.gene_ids:
                            self.gene_ids[gene_id] = None
                        else:
                            self.gene_ids[gene_id] = 1
                            # add dbReference type and gene ids to the dict
                            temp_dict["dbReference"] = {dbr.get("type") : entry_gene_ids}
                e.clear()
                while e.getprevious() is not None:
                    del e.getparent()[0]
                yield temp_dict

    def __str__(self):
        return "SwissProt_Parser"

