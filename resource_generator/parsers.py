# coding: utf-8

from common import gzip_to_text
from lxml import etree
import csv
import gzip
import uuid
import urllib
import zipfile
import io

class Parser(object):
    def __init__(self, file_to_url):
        self.file_to_url = file_to_url

    def parse():
        pass


class EntrezGeneInfoParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/
                          namespace/entrez-gene-ids-hmr.belns"""

    def __init__(self, file_to_url):
        super(EntrezGeneInfoParser, self).__init__(file_to_url)
        file_keys = iter(file_to_url.keys())
        self.entrez_gene_info = next(file_keys)

    def parse(self):
        gene_dict = {}
        # define a csv reader object
        info_csvreader = csv.reader(gzip_to_text(self.entrez_gene_info),
                                    delimiter="\t", quotechar="\"")

        # columns for an Entrez gene info dataset.
        self.gene_info_headers = ["tax_id", "GeneID", "Symbol", "LocusTag",
                                  "Synonyms", "dbXrefs", "chromosome",
                                  "map_location", "description",
                                  "type_of_gene",
                                  "Symbol_from_nomenclature_authority",
                                  "Full_name_from_nomenclature_authority",
                                  "Nomenclature_status",
                                  "Other_designations", "Modification_date"]

        # Dictionary for base gene info
        temp_dict = {}
        info_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_info),
                                   delimiter='\t',
                                   fieldnames=self.gene_info_headers)
        for row in info_csvr:
            if row['tax_id'] in ('9606', '10090', '10116'):
                yield row

    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneInfo_Parser"


class EntrezGeneHistoryParser(Parser):
    resourceLocation = """"http://resource.belframework.org/belframework/1.0/
                           namespace/entrez-gene-ids-hmr.belns"""

    def __init__(self, file_to_url):
        super(EntrezGeneHistoryParser, self).__init__(file_to_url)
        file_keys = iter(file_to_url.keys())
        self.entrez_gene_history = next(file_keys)

    def parse(self):
        # columns from the Entrez history dataset
        self.gene_history_headers = ["tax_id", "GeneID", "Discontinued_GeneID",
                                     "Discontinued_Symbol", "Discontinued_Date"]

         # Dictionary for base gene info
        temp_dict = {}
        history_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_history),
                                      delimiter='\t',
                                      fieldnames=self.gene_history_headers)

        for row in history_csvr:
            if row["tax_id"] in ("9606", "10090", "10116"):
                yield row

    def __walk__(self, history_dict, val):
        while val in history_dict:
            val = history_dict[val]
        return None if val == '-' else val

    def __str__(self):
        return "EntrezGeneHistory_Parser"


class HGNCParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/
                          namespace/hgnc-approved-symbols.belns"""

    def __init__(self, file_to_url):
        super(HGNCParser, self).__init__(file_to_url)
        self.hgnc_file = next(iter(file_to_url.keys()))

    def parse(self):
        # use iso-8859-1 as default encoding.
        with open(self.hgnc_file, "r", encoding="iso-8859-1") as hgncf:

            # columns from the HGNC dataset
            self.hgnc_column_headers = ["HGNC ID", "Approved Symbol",
                                        "Approved Name", "Status",
                                        "Locus Type", "Locus Group",
                                        "Previous Symbols", "Previous Names",
                                        "Synonyms", "Name Synonyms",
                                        "Chromosome", "Date Approved",
                                        "Date Modified", "Date Symbol Changed",
                                        "Date Name Changed",
                                        "Accession Numbers", "Enzyme IDs",
                                        "Entrez0 Gene ID", "Ensembl Gene ID",
                                        "Mouse Genome Database ID",
                                        "Specialist Database Links",
                                        "Specialist Database IDs",
                                        "Pubmed IDs", "RefSeq IDs",
                                        "Gene Family Tag",
                                        "Gene family description",
                                        "Record Type", "Primary IDs",
                                        "Secondary IDs",
                                        "CCDS IDs", "VEGA IDs",
                                        "Locus Specific Databases",
                                        "Entrez1 Gene ID", "OMIM ID", "RefSeq",
                                        "UniProtID", "Ensembl ID", "UCSC ID",
                                        "Mouse Genome Database ID",
                                        "Rat Genome Database ID"]

            hgnc_csvr = csv.DictReader(hgncf, delimiter='\t',
                                       fieldnames=self.hgnc_column_headers)

            # skip the first header row
            next(hgnc_csvr)

            for row in hgnc_csvr:
                yield row

    def __str__(self):
        return "HGNC_Parser"


class MGIParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/
                          namespace/mgi-approved-symbols.belns"""

    def __init__(self, file_to_url):
        super(MGIParser, self).__init__(file_to_url)
        self.mgi_file = next(iter(file_to_url.keys()))

    def parse(self):
        with open(self.mgi_file, "r") as mgif:

           # columns from the MGI dataset
            self.mgi_column_headers = ["MGI Marker Accession ID", "Chr",
                                       "cM Position", "genome coordinate start",
                                       "genome coordinate end", "strand",
                                       "Marker Symbol", "Status", "Marker Name",
                                       "Marker Type", "Feature Type",
                                       "Marker Synonyms (pipe-separated)"]

            mgi_csvr = csv.DictReader(mgif, delimiter='\t',
                                      fieldnames=self.mgi_column_headers)

            # skip the first header row
            next(mgi_csvr)
            for row in mgi_csvr:
                yield row

    def __str__(self):
        return "MGI_Parser"


class RGDParser(Parser):
    resourceLocation = """http://resource.belframework.org/belframework/1.0/
                          namespace/rgd-approved-symbols.belns"""

    def __init__(self, file_to_url):
        super(RGDParser, self).__init__(file_to_url)
        self.rgd_file = next(iter(file_to_url.keys()))

    def parse(self):
        with open(self.rgd_file, "r") as rgdf:

            # columns from the RGD dataset
            self.rgd_column_headers = ["GENE_RGD_ID", "SYMBOL", "NAME",
                                       "GENE_DESC", "CHROMOSOME_CELERA",
                                       "CHROMOSOME_3.1", "CHROMOSOME_3.4",
                                       "FISH_BAND", "START_POS_CELERA",
                                       "STOP_POS_CELERA", "STRAND_CELERA",
                                       "START_POS_3.1", "STOP_POS_3.1",
                                       "STRAND_3.1", "START_POS_3.4",
                                       "STOP_POS_3.4", "STRAND_3.4",
                                       "CURATED_REF_RGD_ID",
                                       "CURATED_REF_PUBMED_ID",
                                       "UNCURATED_PUBMED_ID", "ENTREZ_GENE",
                                       "UNIPROT_ID", "UNUSED",
                                       "GENBANK_NUCLEOTIDE", "TIGR_ID",
                                       "GENBANK_PROTEIN", "UNIGENE_ID",
                                       "SSLP_RGD_ID", "SSLP_SYMBOL",
                                       "OLD_SYMBOL", "OLD_NAME", "QTL_RGD_ID",
                                       "QTL_SYMBOL", "NOMENCLATURE_STATUS",
                                       "SPLICE_RGD_ID", "SPLICE_SYMBOL",
                                       "GENE_TYPE", "ENSEMBL_ID",
                                       "GENE_REFSEQ_STATUS", "UNUSED_OTHER"]

            # skip all the comment lines beginning with '#' and also the header.
            rgd_csvr = csv.DictReader(filter(lambda row:
                                                 not row[0].startswith('#') and
                                             str(row[0]).isdigit(), rgdf),
                                      delimiter='\t',
                                      fieldnames=self.rgd_column_headers)

            for row in rgd_csvr:
                yield row

    def __str__(self):
        return "RGD_Parser"


# this exists mainly as a way to break the iteration loop if needed during
# parsing process.
class GeneTypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class SwissProtParser(Parser):
    resourceLocation_accession_numbers = """http://resource.belframework.org/
                belframework/1.0/namespace/swissprot-accession-numbers.belns"""
    resourceLocation_entry_names = """http://resource.belframework.org/
                      belframework/1.0/namespace/swissprot-entry-names.belns"""

    def __init__(self, file_to_url):
        super(SwissProtParser, self).__init__(file_to_url)
        self.sprot_file = next(iter(file_to_url.keys()))
        self.entries = {}
        self.accession_numbers = {}
        self.gene_ids = {}
        self.tax_ids = {'9606', '10090', '10116'}
        self.pro = '{http://uniprot.org/uniprot}protein'
        self.rec_name = '{http://uniprot.org/uniprot}recommendedName'
        self.full_name = '{http://uniprot.org/uniprot}fullName'
        self.short_name = '{http://uniprot.org/uniprot}shortName'
        self.alt_name = '{http://uniprot.org/uniprot}alternativeName'
        self.db_ref = '{http://uniprot.org/uniprot}dbReference'
        self.organism = '{http://uniprot.org/uniprot}organism'
        self.entry = '{http://uniprot.org/uniprot}entry'
        self.accession = '{http://uniprot.org/uniprot}accession'
        self.name = '{http://uniprot.org/uniprot}name'

    def parse(self):
        sprot_dict = {}

        with gzip.open(self.sprot_file) as sprotf:
            ctx = etree.iterparse(sprotf, events=('end',),
                                  tag=self.entry)

            for ev, e in ctx:
                temp_dict = {}
                n_dict = {}
                # stop evaluating if this entry is not in the Swiss-Prot dataset
                if e.get('dataset') != 'Swiss-Prot':
                    e.clear()
                    continue

                # stop evaluating if this entry is not for human, mouse, or rat
                org = e.find(self.organism)

                # use a custom exception to break to next iteration (e)
                # if tax ref is not found.
                try:
                    for org_child in org:
                        if org_child.tag == self.db_ref:
                            # restrict by NCBI Taxonomy reference
                            if org_child.get('id') not in self.tax_ids:
                                e.clear()
                                raise GeneTypeError(org_child.get('id'))
                            else:
                                # add NCBI Taxonomy and the id for the entry
                                # to the dict
                                temp_dict[org_child.get('type')] = \
                                    org_child.get('id')
                except GeneTypeError:
                    continue

                # get entry name, add it to the dict
                entry_name = e.find(self.name).text
                temp_dict['name'] = entry_name

                # get protein data, add recommended full and short names to dict
                protein = e.find(self.pro)

                for child in protein.find(self.rec_name):
                    if child.tag == self.full_name:
                        temp_dict['recommendedFullName'] = child.text
                    if child.tag == self.short_name:
                        temp_dict['recommendedShortName'] = child.text
                alt_shortnames = []
                alt_fullnames = []

                protein = e.find(self.pro)
                for altName in protein.findall(self.alt_name):
                    for child in altName:
                        if child.tag == self.full_name:
                            alt_fullnames.append(child.text)
                        if child.tag == self.short_name:
                            alt_shortnames.append(child.text)

                temp_dict['alternativeFullNames'] = alt_fullnames
                temp_dict['alternativeShortNames'] = alt_shortnames

                # get all accessions
                entry_accessions = []
                for entry_accession in e.findall(self.accession):
                    acc = entry_accession.text
                    entry_accessions.append(acc)
                    if acc in self.accession_numbers:
                        self.accession_numbers[acc] = None
                    else:
                        self.accession_numbers[acc] = 1

                # add the array of accessions to the dict
                temp_dict["accessions"] = entry_accessions

                # add dbReference type (human, rat, and mouse) and gene ids to
                # the dict
                type_set = ['GeneId', 'MGI', 'HGNC', 'RGD']
                entry_gene_ids = []
                for dbr in e.findall(self.db_ref):
                    if dbr.get('type') in type_set:
                        gene_id = dbr.get('id')
                        n_dict[dbr.get('type')] = dbr.get('id')
                temp_dict['dbReference'] = n_dict

                # clear the tree before next iteration
                e.clear()
                while e.getprevious() is not None:
                    del e.getparent()[0]

                yield temp_dict

    def __str__(self):
        return 'SwissProt_Parser'


def get_data(url):
    # from url, download and save file
    REQ = urllib.request.urlopen(url)
    file_name = url.split('/')[-1]
    with open(file_name,'b+w') as f:
        f.write(REQ.read())
    return file_name

def filter_plus_print(row):
    #print('Row -- ' +str(row))
    #print('Row Type -- ' +str(type(row)))
    return not row.startswith('#')
    #print("Keeping:" if result else "Removing:", row)
    #return result

class AffyParser(Parser):

    def __init__(self, file_to_url):
        super(AffyParser, self).__init__(file_to_url)
        self.affy_file = next(iter(file_to_url.keys()))

    # here maybe take the downloading and exctracting the files out of
    # parser() and call only once from __init__. As it is, the data
    # is being re-downloaded and parsed every time.
    def parse(self):

        # the arrays we are concerned with
        array_names = ['HG-U133A', 'HG-U133B', 'HG-U133_Plus_2', 'HG_U95Av2',
                       'MG_U74A', 'MG_U74B', 'MG_U74C', 'MOE430A', 'MOE430B',
                       'Mouse430A_2', 'Mouse430_2', 'RAE230A', 'RAE230B',
                       'Rat230_2']
        affy_column_headers = ['Probe Set ID', 'GeneChip Array',
                               'Species Scientific Name', 'Annotation Date',
                               'Sequence Type', 'Sequence Source',
                               'Transcript ID(Array Design)',
                               'Target Description',
                               'Representative Public ID',
                               'Archival UniGene Cluster', 'UniGene ID',
                               'Genome Version', 'Alignments', 'Gene Title',
                               'Gene Symbol', 'Chromosomal Location',
                               'Unigene Cluster Type', 'Ensembl',
                               'Entrez Gene', 'SwissProt', 'EC', 'OMIM',
                               'RefSeq Protein ID', 'RefSeq Transcript ID',
                               'FlyBase', 'AGI', 'WormBase', 'MGI Name',
                               'RGD Name', 'SGD accession number',
                               'Gene Ontology Biological Process',
                               'Gene Ontology Cellular Component',
                               'Gene Ontology Molecular Function', 'Pathway',
                               'InterPro', 'Trans Membrane', 'QTL',
                               'Annotation Description',
                               'Annotation Transcript Cluster',
                               'Transcript Assignments', 'Annotation Notes']
        urls = []
        with open(self.affy_file, 'rb') as affyf:
            ctx = etree.iterparse(affyf, events=('start', 'end'))

            # This is certainly not the best way to traverse this tree. Look at
            # the lxml.etree API more closely for possible implementations when
            # refactoring
            for ev, e in ctx:
                # iterate the Array elements
                for n in e.findall('Array'):
                    name = n.get('name')
                    if name in array_names:
                        # iterate Annotation elements
                        for child in n:
                            if child.get('type') == 'Annot CSV':
                                # iterate File elements
                                for g_child in child:
                                    # get the URL and add to the list
                                    for gg_child in g_child:
                                        urls.append(gg_child.text)

        # iterate over the list of URLs returned from the Affy XML feed
        for link in urls:
            affy_reader = {}

            # get_data() downloads the file, saves it as a .csv.zip, and
            # returns a pointer to the file.
            n = get_data(link)
            z = zipfile.ZipFile(n, 'r')

            # only want the .csv from the archive (also contains a .txt)
            for name in z.namelist():
                if '.csv' in name:
                    print('Extracting - ' +name)
                    affy_reader = csv.DictReader(filter(filter_plus_print,
                                                        io.TextIOWrapper(z.open(name))),
                                                        delimiter=',')
                    for x in affy_reader:
                        yield x

    def __str__(self):
        return 'Affy_Parser'
