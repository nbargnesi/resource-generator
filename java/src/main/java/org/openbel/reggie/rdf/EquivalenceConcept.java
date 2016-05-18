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

import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.vocabulary.DCTerms;
import org.apache.jena.vocabulary.SKOS;

import java.util.Collection;

/**
 * Represents a BEL RDF equivalence.
 */
public class EquivalenceConcept {

    private String identifier;
    private String preflabel;
    private final static String SKOS_PREF_LABEL_URI;
    private final static String SKOS_IN_SCHEME_URI;
    private final static String DC_IDENTIFIER_URI;
    private String uuid;

    static {
        SKOS_PREF_LABEL_URI = SKOS.prefLabel.asResource().getURI();
        SKOS_IN_SCHEME_URI = SKOS.inScheme.asResource().getURI();
        DC_IDENTIFIER_URI = DCTerms.identifier.asResource().getURI();
    }

    /**
     * Create an equivalence concept from a collection of triples.
     *
     * @param triples {@link Collection} of {@link RDFNode RDF node}
     * {@link TTriple triples}
     */
    public EquivalenceConcept(Collection<TTriple<RDFNode>> triples) {
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
            } else if (predicateURI.equals(SKOS_IN_SCHEME_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isResource()) continue;
                String uri = object.asResource().getURI();
                if (!uri.contains("uuid")) continue;
                String[] tokens = uri.split("/");
                this.uuid = tokens[tokens.length - 1];
            }
        }
    }

    /**
     * Get this equivalence concept's UUID.
     *
     * @return {@link String}
     */
    public String getUUID() {
        return uuid;
    }

    /**
     * Get whether this namespace concept has an identifier.
     *
     * @return boolean
     */
    public boolean hasIdentifier() {
        if (identifier == null) return false;
        return true;
    }

    /**
     * Get whether this namespace concept has a preferred label.
     *
     * @return boolean
     */
    public boolean hasPreferredLabel() {
        if (preflabel == null) return false;
        return true;
    }

    /**
     * Get this namespace concept's preferred label.
     *
     * @return {@link String}; may be null
     */
    public String getPreferredLabel() {
        return preflabel;
    }

    /**
     * Get this namespace concept's identifier.
     *
     * @return {@link String}; may be null
     */
    public String getIdentifier() {
        return identifier;
    }
}
