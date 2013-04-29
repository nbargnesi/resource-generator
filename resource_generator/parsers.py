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
                #    print("Index = ", index)
                #    print("Item = ", item)
                    try:
                        row[index]
                    except IndexError:
                        print("Line number: ", info_csvreader.line_num)
                        print("Row: ", row)
                    info_dict[item] = row[index]
                    yield info_dict

   #     with open('entrez_info.csv', 'w', newline='') as f:
   #         writer = csv.DictWriter(f, info_dict.keys())
   #         writer.writeheader()
   #         writer.writerow(info_dict)

   #     yield info_dict
    

    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneInfo Parser for dataset: %s" %(self.file_to_url)

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
            
       #  print("# of key-value pairs in history_dict: ", len(history_dict))
       # with open('entrez_history.csv', 'w', newline='') as f:
       #     writer = csv.DictWriter(f, history_dict.keys())
       #     writer.writeheader()
       #     writer.writerow(history_dict)

       # yield history_dict
    

    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneHistory Parser for dataset: %s" %(self.file_to_url)

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

            with open('hgnc.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, temp_dict.keys())
                writer.writeheader()
                writer.writerow(temp_dict)
         
        return (temp_dict)

    def __str__(self):
        return "HGNC Parser for dataset: %s" %(self.file_to_url)

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
            mgi_column_headers = ["MGI Marker Accession ID", "Chromosome", "cM Position", \
                                       "Genome Coordinate Start", "Genome Coordinate End", \
                                       "Genome Strand", "Marker Symbol", "Status", "Marker Name", \
                                       "Marker Type", "Feature types (|-delimited)", \
                                       "Marker Synonyms (|-delimited)"]

            temp_dict = dict()
            for row in mgi_csvr:
                for index, item in enumerate(mgi_column_headers):
                    temp_dict[item] = row[index]

            with open('mgi.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, temp_dict.keys())
                writer.writeheader()
                writer.writerow(temp_dict)
    
        return (temp_dict)

    def __str__(self):
        return "MGI Parser for dataset: %s" %(self.file_to_url)

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

            with open('hgnc.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, temp_dict.keys())
                writer.writeheader()
                writer.writerow(temp_dict)
    
        return (temp_dict)
    
    def __str__(self):
        return "RGD Parser for dataset: %s" %(self.file_to_url)

class SwissProtParser(Parser):
    resourceLocation_accession_numbers = "http://resource.belframework.org/belframework/1.0/namespace/swissprot-accession-numbers.belns"
    resourceLocation_entry_names = "http://resource.belframework.org/belframework/1.0/namespace/swissprot-entry-names.belns"

    def __init__(self, gene_dict, history_dict, file_to_url):
        super(SwissProtParser, self).__init__(file_to_url)
        self.gene_dict = gene_dict
        self.history_dict = history_dict
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
            self.__fast_iter__(ctx, self.__eval_entry__)

            for entry_name in sorted(self.entry_names):
                val = self.entries[entry_name]
                entry_accessions = val[0]
                entry_gene_ids = val[1]

                # one protein to many genes, so we cannot equivalence
                if len(entry_gene_ids) > 1:
                    entry_uuid = uuid.uuid4()
                elif len(entry_gene_ids) == 0:
                    #print("No GeneId for entry name: %s" %(entry_name))
                    entry_uuid = uuid.uuid4()
                else:
                    # one gene exists so find entrez gene uuid
                    gene_id = entry_gene_ids[0]
                    if gene_id in self.history_dict:
                        gene_id = self.history_dict[gene_id]
                    entry_uuid = self.gene_dict[(EntrezGeneParser.resourceLocation, gene_id)]

                # add entry name namespace / equivalence entry
                sprot_dict.update({(SwissProtParser.resourceLocation_entry_names, entry_name) : (self.encoding, entry_uuid)})

                # add entry accession numbers where each one represents only one swiss prot entry
                for entry_accession in entry_accessions:
                    state = self.accession_numbers[entry_accession]
                    if state is None:
                        # accession number is one to many, create separate uuid
                        # not equivalenced with either entry name or entrez gene id
                        sprot_dict.update({(SwissProtParser.resourceLocation_accession_numbers, entry_accession) : (self.encoding, uuid.uuid4())})
                    else:
                        # accession number is unique to this protein entry, so equivalence
                        # to entry name and entrez gene id
                        sprot_dict.update({(SwissProtParser.resourceLocation_accession_numbers, entry_accession) : (self.encoding, entry_uuid)})
            return sprot_dict 

            #print("swiss prot saved items: %d" %(len(self.entries)))
            #print("Number of unique accession numbers: " + str(sum(val == 1 for acc, val in self.accession_numbers.items())))
            #print("Number of duplicate accession numbers: " + str(sum(val == None for acc, val in self.accession_numbers.items())))
            #print("Number of unique gene ids: " + str(sum(val == 1 for gene_id, val in self.gene_ids.items())))
            #print("Number of duplicate gene ids: " + str(sum(val == None for gene_id, val in self.gene_ids.items())))

            #for k, v in self.gene_dict.items():
            #    print("sprot ns/eq: (%s) : (%s)" %(k, v))

    def __eval_entry__(self, e):
        # stop evaluating if this entry is not in the Swiss-Prot dataset
        if e.get("dataset") != "Swiss-Prot":
            return

        # stop evaluating if this entry is not for human, mouse, or rat
        org = e.find("{http://uniprot.org/uniprot}organism")
        if org is not None:
            # restrict by NCBI Taxonomy reference
            dbr = org.find("{http://uniprot.org/uniprot}dbReference")
            if dbr.get("id") not in ("9606", "10090", "10116"):
                return

        # get entry name
        entry_name = e.find("{http://uniprot.org/uniprot}name").text
        self.entry_names.add(entry_name)

        # get all accessions
        entry_accessions = []
        for entry_accession in e.findall("{http://uniprot.org/uniprot}accession"):
            acc = entry_accession.text
            entry_accessions.append(acc)
            if acc in self.accession_numbers:
                self.accession_numbers[acc] = None
            else:
                self.accession_numbers[acc] = 1

        entry_gene_ids = []
        for dbr in e.findall("{http://uniprot.org/uniprot}dbReference"):
            if dbr.get("type") == "GeneId":
                gene_id = dbr.get("id")
                entry_gene_ids.append(gene_id)
                if gene_id in self.gene_ids:
                    self.gene_ids[gene_id] = None
                else:
                    self.gene_ids[gene_id] = 1

        self.entries.update({entry_name : (entry_accessions, entry_gene_ids)})

    def __fast_iter__(self, ctx, fun):
        for ev, e in ctx:
            fun(e)
            e.clear()
            while e.getprevious() is not None:
                del e.getparent()[0]
        del ctx

    def __str__(self):
        return "SwissProt Parser for dataset: %s" %(self.file_to_url)

