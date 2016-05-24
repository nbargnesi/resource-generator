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
package org.openbel.reggie.rdf;

import org.apache.jena.query.QuerySolution;
import org.apache.jena.rdf.model.RDFNode;
import org.openbel.reggie.rdf.vocabulary.BEL;

import java.io.File;
import java.util.LinkedList;
import java.util.List;

import static java.lang.System.getenv;

/**
 * A collection of functions for working with BEL RDF data.
 */
public class Functions {

    private static char DOES_NOT_CODE = '\0';

    /**
     * Get the char-encoding of a BEL concept.
     *
     * @param conceptURI BEL concept URI {@link String string}; e.g., {@link
     *                   BEL#ABUNDANCE_CONCEPT_URI}
     * @return char; {@code \0} if the concept URI does not code for a BEL
     * concept
     */
    public static char conceptToEncoding(String conceptURI) {
        if (BEL.ABUNDANCE_CONCEPT_URI.equals(conceptURI)) {
            return 'A';
        } else if (BEL.BIOLOGICAL_PROCESS_CONCEPT_URI.equals(conceptURI)) {
            return 'B';
        } else if (BEL.COMPLEX_CONCEPT_URI.equals(conceptURI)) {
            return 'C';
        } else if (BEL.GENE_CONCEPT_URI.equals(conceptURI)) {
            return 'G';
        } else if (BEL.MICRORNA_CONCEPT_URI.equals(conceptURI)) {
            return 'M';
        } else if (BEL.PATHOLOGY_CONCEPT_URI.equals(conceptURI)) {
            return 'O';
        } else if (BEL.PROTEIN_CONCEPT_URI.equals(conceptURI)) {
            return 'P';
        } else if (BEL.RNA_CONCEPT_URI.equals(conceptURI)) {
            return 'R';
        } else if (BEL.MOLECULAR_ACTIVITY_CONCEPT_URI.equals(conceptURI)) {
            return 'T';
        } else if (BEL.PROTEIN_MODIFICATION_CONCEPT_URI.equals(conceptURI)) {
            return 'E';
        }
        return DOES_NOT_CODE;
    }

    /**
     * Get whether a concept URI {@link String string} codes for a BEL concept.
     * <p>
     * For example, the following URI codes for BEL abundances:
     * <code>
     * assert encodedConcept(BEL.ABUNDANCE_CONCEPT_URI) == true
     * </code>
     * And this concept URI does not:
     * <code>
     * assert encodedConcept(BEL.ANNOTATION_CONCEPT_URI) == false
     * </code>
     * </p>
     *
     * @param conceptURI BEL concept URI {@link String string}; e.g., {@link
     *                   BEL#ABUNDANCE_CONCEPT_URI}
     * @return boolean
     */
    public static boolean encodedConcept(String conceptURI) {
        char e = conceptToEncoding(conceptURI);
        if (e == DOES_NOT_CODE) return false;
        return true;
    }

    /**
     * Get the namespace file templates for a preferred label.
     *
     * @param preferredLabel {@link String}
     * @return File[]
     */
    public static File[] namespaceTemplates(String preferredLabel) {
        final String templateDir = getenv("RG_JAVA_TEMPLATES");
        preferredLabel = preferredLabel.replace(' ', '-');
        preferredLabel = preferredLabel.toLowerCase();
        String belns = preferredLabel + "-belns.st";
        String ids = preferredLabel + "-ids-belns.st";

        List<File> files = new LinkedList<>();
        File template;
        template = new File(templateDir, belns);
        if (template.canRead()) files.add(template);
        template = new File(templateDir, ids);
        if (template.canRead()) files.add(template);
        return files.toArray(new File[0]);
    }

    /**
     * Get the annotation file template for a preferred label.
     *
     * @param preferredLabel {@link String}
     * @return File
     */
    public static File annotationTemplate(String preferredLabel) {
        final String templateDir = getenv("RG_JAVA_TEMPLATES");
        preferredLabel = preferredLabel.replace(' ', '-');
        preferredLabel = preferredLabel.toLowerCase();
        String belanno = preferredLabel + "-belanno.st";

        File template;
        template = new File(templateDir, belanno);
        if (template.canRead()) return template;
        return null;
    }

    /**
     * Get the equivalence file templates for a preferred label.
     *
     * @param preferredLabel {@link String}
     * @return File[]
     */
    public static File[] equivalenceTemplate(String preferredLabel) {
        final String templateDir = getenv("RG_JAVA_TEMPLATES");
        preferredLabel = preferredLabel.replace(' ', '-');
        preferredLabel = preferredLabel.toLowerCase();
        String beleq = preferredLabel + "-beleq.st";
        String ids = preferredLabel + "-ids-beleq.st";

        List<File> files = new LinkedList<>();
        File template;
        template = new File(templateDir, beleq);
        if (template.canRead()) files.add(template);
        template = new File(templateDir, ids);
        if (template.canRead()) files.add(template);
        return files.toArray(new File[0]);
    }

    /**
     * Consume all {@link QuerySolution query solutions} from the solutions and
     * return it in its entirety.
     * <p>
     *     This method should only be used when the number of potential query
     *     solutions is very low. Otherwise, stick with the iterator.
     * </p>
     * @param solutions {@link QuerySolutions}
     * @return {@link List} of {@link QuerySolution}
     */
    public static List<QuerySolution> consume(QuerySolutions solutions) {
        List<QuerySolution> x = new LinkedList<>();
        solutions.forEach((y) -> { x.add(y); });
        return x;
    }

    /**
     * Consume all {@link QuerySolution query solutions} binding <i>binding</i>
     * from the solutions and return them all.
     * <p>
     *     This method should only be used when the number of potential query
     *     solutions is very low. Otherwise, stick with the iterator.
     * </p>
     * @param solutions {@link QuerySolutions}
     * @return {@link List} of {@link RDFNode}
     */
    public static List<RDFNode> consume(QuerySolutions solutions, String binding) {
        List<RDFNode> x = new LinkedList<>();
        solutions.forEach((y) -> { x.add(y.get(binding)); });
        return x;
    }

    /**
     * Consume all {@link QuerySolution query solutions} binding <i>subject</i>
     * from the solutions and return them all.
     * <p>
     *     This method should only be used when the number of potential query
     *     solutions is very low. Otherwise, stick with the iterator.
     * </p>
     * @param solutions {@link QuerySolutions}
     * @return {@link List} of {@link RDFNode}
     */
    public static List<RDFNode> consumeSubject(QuerySolutions solutions) {
        List<RDFNode> x = new LinkedList<>();
        solutions.forEach((y) -> { x.add(y.get("subject")); });
        return x;
    }

    /**
     * Consume all {@link QuerySolution query solutions} binding
     * <i>predicate</i>from the solutions and return them all.
     * <p>
     *     This method should only be used when the number of potential query
     *     solutions is very low. Otherwise, stick with the iterator.
     * </p>
     * @param solutions {@link QuerySolutions}
     * @return {@link List} of {@link RDFNode}
     */
    public static List<RDFNode> consumePredicate(QuerySolutions solutions) {
        List<RDFNode> x = new LinkedList<>();
        solutions.forEach((y) -> { x.add(y.get("predicate")); });
        return x;
    }

    /**
     * Consume all {@link QuerySolution query solutions} binding <i>object</i>
     * from the solutions and and return them all.
     * <p>
     *     This method should only be used when the number of potential query
     *     solutions is very low. Otherwise, stick with the iterator.
     * </p>
     * @param solutions {@link QuerySolutions}
     * @return {@link List} of {@link RDFNode}
     */
    public static List<RDFNode> consumeObject(QuerySolutions solutions) {
        List<RDFNode> x = new LinkedList<>();
        solutions.forEach((y) -> { x.add(y.get("object")); });
        return x;
    }

    /**
     * Get the first element of a {@link List list}.
     * @param list {@link List}
     * @param <T> Formal type parameter list element
     * @return {@link List} element {@code T}
     */
    public static <T> T first(List<T> list) {
        return list.get(0);
    }

}
