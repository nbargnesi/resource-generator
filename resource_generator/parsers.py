# coding: utf-8
#
# parsers.py

from common import gzip_to_text
from lxml import etree
from collections import defaultdict
import csv
import gzip
import urllib.request
import zipfile
import io
import ipdb

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

        # columns for an Entrez gene info dataset.
        entrez_info_headers = ["tax_id", "GeneID", "Symbol", "LocusTag",
                               "Synonyms", "dbXrefs", "chromosome",
                               "map_location", "description",
                               "type_of_gene",
                               "Symbol_from_nomenclature_authority",
                               "Full_name_from_nomenclature_authority",
                               "Nomenclature_status",
                               "Other_designations", "Modification_date"]

      # dictionary for base gene info
        info_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_info),
                                   delimiter='\t',
                                   fieldnames=entrez_info_headers)

        for row in info_csvr:
            if row['tax_id'] in ('9606', '10090', '10116'):
                yield row

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

        entrez_history_headers = ["tax_id", "GeneID", "Discontinued_GeneID",
                                  "Discontinued_Symbol", "Discontinued_Date"]

         # dictionary for base gene info
        history_csvr = csv.DictReader(gzip_to_text(self.entrez_gene_history),
                                      delimiter='\t',
                                      fieldnames=entrez_history_headers)

        for row in history_csvr:
            if row['tax_id'] in ("9606", "10090", "10116"):
                yield row

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

            # Note that HGNC uses TWO columns named the same thing for Entrez
            # Gene ID. Currently we are not using these columns and it is not a
            # big deal, but in the future we could account for this by using
            # custom headers (like EntrezGeneInfo_Parser), or resolving to the
            # SECOND of the Entrez Gene ID columns.
            hgnc_csvr = csv.DictReader(hgncf, delimiter='\t')

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
            mgi_csvr = csv.DictReader(mgif, delimiter='\t')

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
            # skip all the comment lines beginning with '#' and also the header.
            rgd_csvr = csv.DictReader(filter(lambda row:
                                                 not row[0].startswith('#'), rgdf),
                                      delimiter='\t')

            for row in rgd_csvr:
                yield row

    def __str__(self):
        return "RGD_Parser"


# This class exists mainly as a way to break the iteration loop during parsing
# of the SwissProt dataset if needed.
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

        with gzip.open(self.sprot_file) as sprotf:
            ctx = etree.iterparse(sprotf, tag=self.entry)

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
                for dbr in e.findall(self.db_ref):
                    if dbr.get('type') in type_set:
                        gene_id = dbr.get('id')
                        if dbr.get('type') not in n_dict:
                            n_dict[dbr.get('type')] = [gene_id]
                        else:
                            n_dict[dbr.get('type')].append(gene_id)
                temp_dict['dbReference'] = n_dict

                # clear the tree before next iteration
                e.clear()
                while e.getprevious() is not None:
                    del e.getparent()[0]

                yield temp_dict

    def __str__(self):
        return 'SwissProt_Parser'


# Helper function for AffyParser. This will save each of the downloaded
# URLs and return the file pointer.
def get_data(url):
    # from url, download and save file
    REQ = urllib.request.urlopen(url)
    file_name = url.split('/')[-1]
    with open(file_name,'b+w') as f:
        f.write(REQ.read())
    return file_name

def filter_plus_print(row):
    return not row.startswith('#')


class AffyParser(Parser):

    def __init__(self, file_to_url):
        super(AffyParser, self).__init__(file_to_url)
        self.affy_file = next(iter(file_to_url.keys()))

    # Here maybe take the downloading and exctracting the files out of
    # parser() and call only once from __init__. As it is, the data
    # is being re-downloaded and parsed every time.
    def parse(self):

        # the arrays we are concerned with
        array_names = ['HG-U133A', 'HG-U133B', 'HG-U133_Plus_2', 'HG_U95Av2',
                       'MG_U74A', 'MG_U74B', 'MG_U74C', 'MOE430A', 'MOE430B',
                       'Mouse430A_2', 'Mouse430_2', 'RAE230A', 'RAE230B',
                       'Rat230_2']

        urls = []
        with open(self.affy_file, 'rb') as affyf:
            ctx = etree.iterparse(affyf, events=('start', 'end'))

            # This is certainly not the best way to traverse this tree. Look at
            # the lxml.etree API more closely for possible implementations when
            # refactoring
            # NOTES - put some debugging in here to see how this is parsing,
            # may be a better way to parse (like using diff events).
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
                    # wrap in a TextIOWrapper. otherwise it returns bytes.
                    affy_reader = csv.DictReader(filter(lambda x:
                                                        not x.startswith('#'),
                                                        io.TextIOWrapper(z.open(name))),
                                                        delimiter=',')

                    for x in affy_reader:
                        yield x

    def __str__(self):
        return 'Affy_Parser'

class Gene2AccParser(Parser):

    def __init__(self, file_to_url):
       super(Gene2AccParser, self).__init__(file_to_url)
       self.gene2acc_file = next(iter(file_to_url.keys()))

    def parse(self):

        # would like to have DictReader handle this, but need a way to
        # deal with the special case of the first value beginning with
        # a hashtag. i.e. #Format: <-- is NOT a column header.
        column_headers = ['tax_id', 'GeneID', 'status',
                          'RNA nucleotide accession.version',
                          'RNA nucleotide gi', 'protein accession.version',
                          'protein gi', 'genomic nucleotide accession.version',
                          'genomic nucleotide gi',
                          'start position on the genomic accession',
                          'end position on the genomic accession',
                          'orientation', 'assembly',
                          'mature peptide accession.version',
                          'mature peptide gi', 'Symbol']

        g2a_reader = csv.DictReader(gzip_to_text(self.gene2acc_file), delimiter='\t',
                                    fieldnames=column_headers)
        for row in g2a_reader:
            yield row

    def __str__(self):
        return 'Gene2Acc_Parser'

class BELNamespaceParser(Parser):

    def __init__(self):
        self.old_files = 'http://resource.belframework.org./belframework/1.0/index.xml'
        self.anno_def = '{http://www.belscript.org/schema/annotationdefinitions}annotationdefinitions'
        self.namespace = '{http://www.belscript.org/schema/namespace}namespace'
        self.namespaces = '{http://www.belscript.org/schema/namespaces}namespaces'

    def parse(self):

        tree = etree.parse(self.old_files)

        # xpath will return all elements under this namespace (list of bel namespace urls)
        urls = tree.xpath('//*[local-name()="namespace"]/@idx:resourceLocation',
                          namespaces={'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                      'idx' : 'http://www.belscript.org/schema/index'})

        for u in urls:
            yield u

    def __str__(self):
        return 'BELNamespace_Parser'


class CHEBIParser(Parser):

    def __init__(self, file_to_url):
        super(CHEBIParser, self).__init__(file_to_url)
        self.chebi_file = '/home/jhourani/openbel-contributions/resource_generator/base/datasets/chebi.owl'
        self.classy = '{http://www.w3.org/2002/07/owl#}Class'
        self.label = '{http://www.w3.org/2000/01/rdf-schema#}label'
        self.altId = '{http://purl.obolibrary.org/obo#}altId'

    def parse(self):

        chebi_dict = defaultdict(list)
        with open(self.chebi_file, 'rb') as cf:
            tree = etree.iterparse(cf, tag=self.classy)
            for event, elem in tree:
                if len(elem.values()) != 0:
                    vals = elem.values()
                    chebi_dict['primary_id'] = vals[0].split('CHEBI_')[1]
                    children = elem.getchildren()
                    for child in children:
                        if child.tag == self.label:
                            chebi_dict['name'] = child.text
                        if child.tag == self.altId:
                            chebi_dict['alt_ids'].append(child.text.split(':')[1])
                    #ipdb.set_trace()
                    yield chebi_dict

    def __str__(self):
        return 'CHEBI_Parser'


# class CHEBIParser(Parser):

#     def __init__(self, file_to_url):
#         super(CHEBIParser, self).__init__(file_to_url)
#         self.chebi_file = file_to_url.get('datasets/chebi.owl')

#     def parse(self):

#         namespace = {
#             'base' : 'ftp://ftp.ebi.ac.uk/pub/databases/chebi/ontology/chebi.owl',
#             'obo' : 'http://purl.obolibrary.org/obo/',
#             'xsd' : 'http://www.w3.org/2001/XMLSchema#',
#             'obo2' : 'http://purl.obolibrary.org/obo#',
#             'dc' : 'http://purl.org/dc/elements/1.1/',
#             'rdfs' : 'http://www.w3.org/2000/01/rdf-schema#',
#             'rdf' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
#             'owl' : 'http://www.w3.org/2002/07/owl#' }

#         tree = etree.parse(self.chebi_file)

#         name_resources = tree.xpath('//owl:Class/*[local-name()="label"]', namespaces=namespace)
#         id_resources = tree.xpath('//owl:Class/@rdf:about', namespaces=namespace)
#         altId_resources = tree.xpath('//owl:Class/*[local-name()="altId"]', namespaces=namespace)

#         names = [x.text for x in name_resources]
#         ids = [x.split('CHEBI_')[1] for x in id_resources]
#         alt_ids = [x.text.split(':')[1] for x in altId_resources]

#         resource_dict = {
#             'name' : names[0],
#             'primary_id' : ids[0],
#             'alt_ids' : alt_ids }

#         yield resource_dict

#     def __str__(self):
#         return 'CHEBI_Parser'

# class CHEBICompoundParser(Parser):

#     def __init__(self, file_to_url):
#         super(CHEBICompoundParser, self).__init__(file_to_url)
#         self.chebi_comp_file = file_to_url.get('datasets/chebi.owl')

#     def parse(self):
#         with open(self.chebi_comp_file, 'r') as cf:
#             chebi_comp_csvr = csv.DictReader(cf, delimiter='\t')

#             for row in chebi_comp_csvr:
#                 yield row

#     def __str__(self):
#         return 'CHEBI_Compound_Parser'


class PUBCHEMParser(Parser):

    def __init__(self, file_to_url):
       super(PUBCHEMParser, self).__init__(file_to_url)
       self.pub_file = next(iter(file_to_url.keys()))

    def parse(self):

        column_headers = ['pubchem_id', 'synonym']
        pub_reader = csv.DictReader(gzip_to_text(self.pub_file), delimiter='\t',
                                    fieldnames=column_headers)
        for row in pub_reader:
            yield row

    def __str__(self):
        return 'PUBCHEM_Parser'
