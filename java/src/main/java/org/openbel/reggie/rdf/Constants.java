package org.openbel.reggie.rdf;

/**
 * RDF constants specific to BEL resources.
 */
public class Constants {

    static {
        RDF_PROLOGUE =
            "PREFIX belv: <http://www.openbel.org/vocabulary/>\n" +
            "PREFIX dcterms: <http://purl.org/dc/terms/>\n" +
            "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\n" +
            "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n" +
            "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n" +
            "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n";

        BELV_ABUNDANCE_CONCEPT = "belv:AbundanceConcept";
        BELV_ANATOMY_ANNOTATION_CONCEPT = "belv:AnatomyAnnotationConcept";
        BELV_ANNOTATION_CONCEPT = "belv:AnnotationConcept";
        BELV_ANNOTATION_CONCEPT_SCHEME = "belv:AnnotationConceptScheme";
        BELV_BIOLOGICAL_PROCESS_CONCEPT = "belv:BiologicalProcessConcept";
        BELV_CELL_ANNOTATION_CONCEPT = "belv:CelllAnnotationConcept";
        BELV_CELL_LINE_ANNOTATION_CONCEPT = "belv:CellLineAnnotationConcept";
        BELV_COMPLEX_CONCEPT = "belv:ComplexConcept";
        BELV_DISEASE_ANNOTATION_CONCEPT = "belv:DiseaseAnnotationConcept";
        BELV_DOMAIN = "belv:domain";
        BELV_FROM_SPECIES = "belv:fromSpecies";
        BELV_GENE_CONCEPT = "belv:GeneConcept";
        BELV_LOCATION_ANNOTATION_CONCEPT = "belv:LocationAnnotationConcept";
        BELV_MICRO_RNA_CONCEPT = "belv:MicroRNAConcept";
        BELV_NAMESPACE_CONCEPT = "belv:NamespaceConcept";
        BELV_NAMESPACE_CONCEPT_SCHEME = "belv:NamespaceConceptScheme";
        BELV_ORTHOLOGOUS_MATCH = "belv:OrthologousMatch";
        BELV_PATHOLOGY_CONCEPT = "belv:PathologyConcept";
        BELV_PREFIX = "belv:prefix";
        BELV_PROTEIN_CONCEPT = "belv:ProteinConcept";
        BELV_RNA_CONCEPT = "belv:RNAConcept";
        BELV_SPECIES_ANNOTATION_CONCEPT = "belv:SpeciesAnnotationConcept";
        BELV_STATUS = "belv:status";
        BELV_UUID_CONCEPT = "belv:UUIDConcept";
        BELV_UUID_CONCEPT_SCHEME = "belv:UUIDConceptScheme";

        SKOS_IN_SCHEME = "skos:inScheme";
        SKOS_EXACT_MATCH = "skos:exactMatch";
        SKOS_PREF_LABEL = "skos:prefLabel";
    }

    /**
     * RDF prologue. Contains prefixes for the BEL vocabulary (belv),
     * Dublin Core (dcterms), RDF (rdf), RDF schema (rdfs), Simple Knowledge
     * Organization System (skos), and XML schema definition (xsd).
     */
    public static final String RDF_PROLOGUE;

    /**
     * The concept of an abundance in the BEL vocabulary.
     */
    public static final String BELV_ABUNDANCE_CONCEPT;

    /**
     * The concept of a anatomy annotation in the BEL vocabulary.
     */
    public static final String BELV_ANATOMY_ANNOTATION_CONCEPT;

    /**
     * The concept of an annotation in the BEL vocabulary.
     */
    public static final String BELV_ANNOTATION_CONCEPT;

    /**
     * The scheme encompassing all annotation concepts in the BEL vocabulary.
     */
    public static final String BELV_ANNOTATION_CONCEPT_SCHEME;

    /**
     * The concept of a biological process in the BEL vocabulary.
     */
    public static final String BELV_BIOLOGICAL_PROCESS_CONCEPT;

    /**
     * The concept of a cell annotation in the BEL vocabulary.
     */
    public static final String BELV_CELL_ANNOTATION_CONCEPT;

    /**
     * The concept of a cell line annotation in the BEL vocabulary.
     */
    public static final String BELV_CELL_LINE_ANNOTATION_CONCEPT;

    /**
     * The concept of a complex in the BEL vocabulary.
     *
     */
    public static final String BELV_COMPLEX_CONCEPT;

    /**
     * The concept of a disease annotation in the BEL vocabulary.
     */
    public static final String BELV_DISEASE_ANNOTATION_CONCEPT;

    /**
     * The concept of a gene in the BEL vocabulary.
     */
    public static final String BELV_GENE_CONCEPT;

    /**
     * The concept of a location annotation in the BEL vocabulary.
     */
    public static final String BELV_LOCATION_ANNOTATION_CONCEPT;

    /**
     * The concept of a microRNA in the BEL vocabulary.
     */
    public static final String BELV_MICRO_RNA_CONCEPT;

    /**
     * The concept of a namespace in the BEL vocabulary.
     */
    public static final String BELV_NAMESPACE_CONCEPT;

    /**
     * The scheme encompassing all namespace concepts in the BEL vocabulary.
     */
    public static final String BELV_NAMESPACE_CONCEPT_SCHEME;

    /**
     * The concept of a pathology in the BEL vocabulary.
     */
    public static final String BELV_PATHOLOGY_CONCEPT;

    /**
     * The concept of a protein in the BEL vocabulary.
     */
    public static final String BELV_PROTEIN_CONCEPT;

    /**
     * The concept of an RNA in the BEL vocabulary.
     */
    public static final String BELV_RNA_CONCEPT;

    /**
     * The concept of a species annotation in the BEL vocabulary.
     */
    public static final String BELV_SPECIES_ANNOTATION_CONCEPT;

    /**
     * The concept of a domain in the BEL vocabulary.
     */
    public static final String BELV_DOMAIN;

    /**
     * The concept of species in the BEL vocabulary.
     */
    public static final String BELV_FROM_SPECIES;

    /**
     * The concept of an orthologous match in the BEL vocabulary.
     */
    public static final String BELV_ORTHOLOGOUS_MATCH;

    /**
     * The concept of a prefix in the BEL vocabulary.
     */
    public static final String BELV_PREFIX;

    /**
     * The concept of status in the BEL vocabulary.
     */
    public static final String BELV_STATUS;

    /**
     * The concept of UUID in the BEL vocabulary.
     */
    public static final String BELV_UUID_CONCEPT;

    /**
     * The scheme encompassing all UUID concepts in the BEL vocabulary.
     */
    public static final String BELV_UUID_CONCEPT_SCHEME;

    /**
     * Transitive property indicating two concepts are linked interchangeably.
     */
    public static final String SKOS_EXACT_MATCH;

    /**
     * Indicates a concept exists in an aggregation of one or more concepts.
     */
    public static final String SKOS_IN_SCHEME;

    /**
     * Preferred label.
     */
    public static final String SKOS_PREF_LABEL;


}

