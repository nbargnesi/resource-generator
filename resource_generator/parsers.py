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
        self.gene_info_headers = ["tax_id", "GeneID", "Symbol", "LocusTag", "Synonyms", "dbXrefs", \
                                      "chromosome", "map_location", "description", "type_of_gene", \
                                      "Symbol_from_nomenclature_authority", \
                                      "Full_name_from_nomenclature_authority", "Nomenclature_status", \
                                      "Other_designations", "Modification_date"]

         # Dictionary for base gene info
        temp_dict = dict()
        info_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_info), delimiter='\t', fieldnames=self.gene_info_headers)
        for row in info_csvr:
            if row["tax_id"] in ("9606", "10090", "10116"):
                temp_dict = row
                yield temp_dict
                

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
        # history_csvreader =  csv.reader(gzip_to_text(self.entrez_gene_history), delimiter="\t", 
        #                                quotechar="\"")

        self.gene_history_headers = ["tax_id", "GeneID", "Discontinued_GeneID", "Discontinued_Symbol", \
                                              "Discontinued_Date"]

         # Dictionary for base gene info
        temp_dict = dict()
        history_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_history), delimiter='\t', fieldnames=self.gene_history_headers)
        for row in history_csvr:
            if row["tax_id"] in ("9606", "10090", "10116"):
                temp_dict = row
                yield temp_dict
 
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
            # hgnc_csvr = csv.reader(hgncf, delimiter="\t", quotechar="\"")

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
            hgnc_csvr = csv.DictReader(hgncf, delimiter='\t', fieldnames=self.hgnc_column_headers)
            for row in hgnc_csvr:
                temp_dict = row
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
            # mgi_csvr = csv.reader(mgif, delimiter="\t", quotechar="\"")

           # columns from the MGI dataset
            self.mgi_column_headers = ["MGI Marker Accession ID", "Chr", "cM Position", \
                                       "genome coordinate start", "genome coordinate end", \
                                       "strand", "Marker Symbol", "Status", "Marker Name", \
                                       "Marker Type", "Feature Type", \
                                       "Marker Synonyms (pipe-separated)"]

            temp_dict = dict()
            mgi_csvr = csv.DictReader(mgif, delimiter='\t', fieldnames=self.mgi_column_headers)
            for row in mgi_csvr:
                temp_dict = row
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
            # rgd_csvr = csv.reader(rgdf, delimiter="\t", quotechar="\"")

           # columns from the RGD dataset
            self.rgd_column_headers = ["GENE_RGD_ID", "SYMBOL", "NAME", "GENE_DESC", "CHROMOSOME_CELERA", \
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

            # skip all the comment lines beginning with '#' and also the header.
            rgd_csvr = csv.DictReader(filter(lambda row:  not row[0].startswith('#') and str(row[0]).isdigit(), rgdf), \
                                          delimiter='\t', fieldnames=self.rgd_column_headers)

            for row in rgd_csvr:
                temp_dict = row
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
                    yield temp_dict
     
                # stop evaluating if this entry is not for human, mouse, or rat
                org = e.find("{http://uniprot.org/uniprot}organism")
                if org is not None:
                    # restrict by NCBI Taxonomy reference
                    dbr = org.find("{http://uniprot.org/uniprot}dbReference")
                    if dbr.get("id") not in ("9606", "10090", "10116"):
                        yield temp_dict
                    else:
                        # add NCBI Taxonomy and the id for the entry to the dict
                        temp_dict[dbr.get("type")] = dbr.get("id")
                        
                # get entry name, add it to the dict
                entry_name = e.find("{http://uniprot.org/uniprot}name").text
                temp_dict["name"] = entry_name
                
                # get protein data, add recommended full and short names to the dict
                protein = e.find("{http://uniprot.org/uniprot}protein")
                # print ("--- Getting recommendedNames ---")
                for child in protein.find("{http://uniprot.org/uniprot}recommendedName"):
                    if child.tag == "{http://uniprot.org/uniprot}fullName":
                        temp_dict["recommendedFullName"] = child.text
                    if child.tag == "{http://uniprot.org/uniprot}shortName":
                        temp_dict["recommendedShortName"] = child.text
                        
                alt_shortnames = []
                alt_fullnames = []

                protein = e.find("{http://uniprot.org/uniprot}protein")
                for altName in protein.findall("{http://uniprot.org/uniprot}alternativeName"):
                    #print (str(altName))
                    for child in altName:
                        #print ("The child of altName: ", child.tag)
                        #print ("The text of that child: ", child.text)
                        if child.tag == "{http://uniprot.org/uniprot}fullName":
                           # print("Adding a full name.")
                            alt_fullnames.append(child.text)
                        if child.tag == "{http://uniprot.org/uniprot}shortName":
                            #print ("Adding a short name.")
                            alt_shortnames.append(child.text)

                temp_dict["alternativeFullNames"] = alt_fullnames
                temp_dict["alternativeShortNames"] = alt_shortnames

                # get gene data
                # names = []
                # gene = e.find("{http://uniprot.org/uniprot}gene")
                # for child in gene.find("name"):
                #    if child.get("type") == "primary":
                #        temp_dict["primary"] = name.text
                #    if child.get("type") == "synonym":
                #        names.apped(name.text)
                # add gene data to the dict
                # temp_dict["synonyms"] = names

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

