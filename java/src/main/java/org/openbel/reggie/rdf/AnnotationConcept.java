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

import gnu.trove.iterator.TCharIterator;
import gnu.trove.set.TCharSet;
import gnu.trove.set.hash.TCharHashSet;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.SKOS;

import static org.openbel.reggie.rdf.Functions.*;

import java.util.Collection;

/**
 * Represents a BEL RDF annotation concept. Annotation concepts are in the
 * annotation concept scheme.
 * <p>
 * In legacy terms, an annotation concept is a single value from a BEL annotation
 * (i.e., <i>.belanno</i> file). The single value is analogous to this class. The
 * enclosing annotation is analogous to the annotation concept scheme.
 * </p>
 */
public class AnnotationConcept {

    private String identifier;
    private String preflabel;
    private final static String RDF_TYPE_URI;
    private final static String SKOS_PREF_LABEL_URI;
    private final static String DC_IDENTIFIER_URI;

    static {
        RDF_TYPE_URI = RDF.type.asResource().getURI();
        SKOS_PREF_LABEL_URI = SKOS.prefLabel.asResource().getURI();
        DC_IDENTIFIER_URI = DCTerms.identifier.asResource().getURI();
    }

    /**
     * Create a annotation concept from a collection of triples.
     *
     * @param triples {@link Collection} of {@link RDFNode RDF node}
     * {@link TTriple triples}
     */
    public AnnotationConcept(Collection<TTriple<RDFNode>> triples) {
        for (TTriple<RDFNode> triple : triples) {
            RDFNode predicate = triple.getMiddle();
            if (!predicate.isResource()) continue;
            String predicateURI = predicate.asResource().getURI();

            if (predicateURI.equals(DC_IDENTIFIER_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isLiteral()) continue;
                this.identifier = object.asLiteral().getLexicalForm();
            } else if (predicateURI.equals(SKOS_PREF_LABEL_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isLiteral()) continue;
                this.preflabel = object.asLiteral().getLexicalForm();
            }
        }
    }

    /**
     * Get whether this annotation concept has an identifier.
     *
     * @return boolean
     */
    public boolean hasIdentifier() {
        if (identifier == null) return false;
        return true;
    }

    /**
     * Get whether this annotation concept has a preferred label.
     *
     * @return boolean
     */
    public boolean hasPreferredLabel() {
        if (preflabel == null) return false;
        return true;
    }

    /**
     * Get this annotation concept's preferred label.
     *
     * @return {@link String}; may be null
     */
    public String getPreferredLabel() {
        return preflabel;
    }

    /**
     * Get this annotation concept's identifier.
     *
     * @return {@link String}; may be null
     */
    public String getIdentifier() {
        return identifier;
    }

}
