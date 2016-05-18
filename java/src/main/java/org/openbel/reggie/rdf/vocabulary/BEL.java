// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
package org.openbel.reggie.rdf.vocabulary;

import org.apache.jena.rdf.model.*;

import static org.apache.jena.rdf.model.ModelFactory.*;

/**
 * BEL vocabulary definitions.
 */
public class BEL {

    /** The RDF model that holds the vocabulary terms. */
    private static Model mdl = createDefaultModel();

    /** The namespace of the vocabulary as a string ({@value}). */
    public static final String NS = "http://www.openbel.org/vocabulary/";

    /**
     * The namespace of the vocabulary as a {@link String}.
     *
     * @return {@link String}
     */
    public static String getURI() {
        return NS;
    }

    /**
     * The namespace of the vocabulary as a {@link Resource resource}.
     *
     * @return {@link Resource}
     */
    public static final Resource NAMESPACE = mdl.createResource(NS);

    private static Property createProperty(String base) {
        return mdl.createProperty(NS + base);
    }

    /** BEL abundance concepts. */
    public static final Property ABUNDANCE_CONCEPT;
    public static final String ABUNDANCE_CONCEPT_URI;
    /** BEL anatomy annotation concepts. */
    public static final Property ANATOMY_ANNOTATION_CONCEPT;
    public static final String ANATOMY_ANNOTATION_CONCEPT_URI;
    /** BEL annotation concepts. */
    public static final Property ANNOTATION_CONCEPT;
    public static final String ANNOTATION_CONCEPT_URI;
    /** BEL annotation concept schemes. */
    public static final Property ANNOTATION_CONCEPT_SCHEME;
    public static final String ANNOTATION_CONCEPT_SCHEME_URI;
    /** BEL biological process concepts. */
    public static final Property BIOLOGICAL_PROCESS_CONCEPT;
    public static final String BIOLOGICAL_PROCESS_CONCEPT_URI;
    /** BEL cell annotation concepts. */
    public static final Property CELL_ANNOTATION_CONCEPT;
    public static final String CELL_ANNOTATION_CONCEPT_URI;
    /** BEL cell line annotation concepts. */
    public static final Property CELL_LINE_ANNOTATION_CONCEPT;
    public static final String CELL_LINE_ANNOTATION_CONCEPT_URI;
    /** BEL complex concepts. */
    public static final Property COMPLEX_CONCEPT;
    public static final String COMPLEX_CONCEPT_URI;
    /** BEL disease annotation concepts. */
    public static final Property DISEASE_ANNOTATION_CONCEPT;
    public static final String DISEASE_ANNOTATION_CONCEPT_URI;
    /** BEL domain concepts. */
    public static final Property DOMAIN;
    public static final String DOMAIN_URI;
    /** BEL from-species concepts. */
    public static final Property FROM_SPECIES;
    public static final String FROM_SPECIES_URI;
    /** BEL gene concepts. */
    public static final Property GENE_CONCEPT;
    public static final String GENE_CONCEPT_URI;
    /** BEL location annotation concepts. */
    public static final Property LOCATION_ANNOTATION_CONCEPT;
    public static final String LOCATION_ANNOTATION_CONCEPT_URI;
    /** BEL microRNA concepts. */
    public static final Property MICRORNA_CONCEPT;
    public static final String MICRORNA_CONCEPT_URI;
    /** BEL namespace concepts. */
    public static final Property NAMESPACE_CONCEPT;
    public static final String NAMESPACE_CONCEPT_URI;
    /** BEL namespace concept schemes. */
    public static final Property NAMESPACE_CONCEPT_SCHEME;
    public static final String NAMESPACE_CONCEPT_SCHEME_URI;
    /** BEL orthologous match concepts. */
    public static final Property ORTHOLOGOUS_MATCH;
    public static final String ORTHOLOGOUS_MATCH_URI;
    /** BEL pathology concepts. */
    public static final Property PATHOLOGY_CONCEPT;
    public static final String PATHOLOGY_CONCEPT_URI;
    /** BEL prefix concepts. */
    public static final Property PREFIX;
    public static final String PREFIX_URI;
    /** BEL protein concepts. */
    public static final Property PROTEIN_CONCEPT;
    public static final String PROTEIN_CONCEPT_URI;
    /** BEL RNA concepts. */
    public static final Property RNA_CONCEPT;
    public static final String RNA_CONCEPT_URI;
    /** BEL species annotation concepts. */
    public static final Property SPECIES_ANNOTATION_CONCEPT;
    public static final String SPECIES_ANNOTATION_CONCEPT_URI;
    /** BEL status concepts. */
    public static final Property STATUS;
    public static final String STATUS_URI;

    static {
        ABUNDANCE_CONCEPT = createProperty("AbundanceConcept");
        ANATOMY_ANNOTATION_CONCEPT = createProperty("AnatomyAnnotationConcept");
        ANNOTATION_CONCEPT = createProperty("AnnotationConcept");
        ANNOTATION_CONCEPT_SCHEME = createProperty("AnnotationConceptScheme");
        BIOLOGICAL_PROCESS_CONCEPT = createProperty("BiologicalProcessConcept");
        CELL_ANNOTATION_CONCEPT = createProperty("CellAnnotationConcept");
        CELL_LINE_ANNOTATION_CONCEPT = createProperty("CellLineAnnotationConcept");
        COMPLEX_CONCEPT = createProperty("ComplexConcept");
        DISEASE_ANNOTATION_CONCEPT = createProperty("DiseaseAnnotationConcept");
        DOMAIN = createProperty("domain");
        FROM_SPECIES = createProperty("fromSpecies");
        GENE_CONCEPT = createProperty("GeneConcept");
        LOCATION_ANNOTATION_CONCEPT = createProperty("LocationAnnotationConcept");
        MICRORNA_CONCEPT = createProperty("MicroRNAConcept");
        NAMESPACE_CONCEPT = createProperty("NamespaceConcept");
        NAMESPACE_CONCEPT_SCHEME = createProperty("NamespaceConceptScheme");
        ORTHOLOGOUS_MATCH = createProperty("orthologousMatch");
        PATHOLOGY_CONCEPT = createProperty("PathologyConcept");
        PREFIX = createProperty("prefix");
        PROTEIN_CONCEPT = createProperty("ProteinConcept");
        RNA_CONCEPT = createProperty("RNAConcept");
        SPECIES_ANNOTATION_CONCEPT = createProperty("SpeciesAnnotationConcept");
        STATUS = createProperty("status");

        ABUNDANCE_CONCEPT_URI = ABUNDANCE_CONCEPT.getURI();
        ANATOMY_ANNOTATION_CONCEPT_URI = ANATOMY_ANNOTATION_CONCEPT.getURI();
        ANNOTATION_CONCEPT_URI = ANNOTATION_CONCEPT.getURI();
        ANNOTATION_CONCEPT_SCHEME_URI = ANNOTATION_CONCEPT_SCHEME.getURI();
        BIOLOGICAL_PROCESS_CONCEPT_URI = BIOLOGICAL_PROCESS_CONCEPT.getURI();
        CELL_ANNOTATION_CONCEPT_URI = CELL_ANNOTATION_CONCEPT.getURI();
        CELL_LINE_ANNOTATION_CONCEPT_URI = CELL_LINE_ANNOTATION_CONCEPT.getURI();
        COMPLEX_CONCEPT_URI = COMPLEX_CONCEPT.getURI();
        DISEASE_ANNOTATION_CONCEPT_URI = DISEASE_ANNOTATION_CONCEPT.getURI();
        DOMAIN_URI = DOMAIN.getURI();
        FROM_SPECIES_URI = FROM_SPECIES.getURI();
        GENE_CONCEPT_URI = GENE_CONCEPT.getURI();
        LOCATION_ANNOTATION_CONCEPT_URI = LOCATION_ANNOTATION_CONCEPT.getURI();
        MICRORNA_CONCEPT_URI = MICRORNA_CONCEPT.getURI();
        NAMESPACE_CONCEPT_URI = NAMESPACE_CONCEPT.getURI();
        NAMESPACE_CONCEPT_SCHEME_URI = NAMESPACE_CONCEPT_SCHEME.getURI();
        ORTHOLOGOUS_MATCH_URI = ORTHOLOGOUS_MATCH.getURI();
        PATHOLOGY_CONCEPT_URI = PATHOLOGY_CONCEPT.getURI();
        PREFIX_URI = PREFIX.getURI();
        PROTEIN_CONCEPT_URI = PROTEIN_CONCEPT.getURI();
        RNA_CONCEPT_URI = RNA_CONCEPT.getURI();
        SPECIES_ANNOTATION_CONCEPT_URI = SPECIES_ANNOTATION_CONCEPT.getURI();
        STATUS_URI = STATUS.getURI();
    }
}
