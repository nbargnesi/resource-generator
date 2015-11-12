affy-probeset-ids-beleq(version, createdDateTime) ::= <<
[Equivalence]
NameString=Affymetrix Probe Set Identifier Equivalences
DescriptionString=Affymetrix probe set identifier equivalences were derived from mappings to Entrez Gene IDs from NetAffx. For probe sets annotated to multiple Entrez Gene IDs, a single ID was selected as follows: the Entrez Gene ID with the highest priority RefSeq status was selected (from high to low priority - Reviewed, Validated, Provisional, Predicted, Model, Inferred, none). Gene IDs with the RefSeq status 'suppressed' were not used. When multiple Entrez Gene IDs shared the highest priority RefSeq status, the lowest numbered ID was selected. 
VersionString=<version>
CreatedDateTime=<createdDateTime>

[NamespaceReference]
NameString=Affymetrix Probe Set Identifiers
VersionString=<version>

[Author]
NameString=OpenBEL
CopyrightString=Copyright (c) 2015, OpenBEL Project. This work is licensed under a Creative Commons Attribution 3.0 Unported License.
ContactInfoString=info@openbel.org

[Citation]
NameString=Affymetrix, Santa Clara, California, USA; NCBI Entrez Gene
DescriptionString=NetAffx annotation files for Affymetrix 3'IVT expression arrays.; RefSeq status was obtained from NCBI gene2accession file.
PublishedVersionString=na35
PublishedDate=2015-04-16
ReferenceURL=http://www.affymetrix.com/analysis; http://www.ncbi.nlm.nih.gov/gene

[Processing]
CaseSensistiveFlag=yes
DelimiterString=|
CacheableFlag=yes

[Values]

>>
