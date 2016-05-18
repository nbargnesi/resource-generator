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

import static java.util.Arrays.sort;
import java.util.Collection;

/**
 * Represents a BEL RDF namespace concept. Namespace concepts are in the
 * namespace concept scheme.
 * <p>
 * In legacy terms, a namespace concept is a single value from a BEL namespace
 * (i.e., <i>.belns</i> file). The single value is analogous to this class. The
 * enclosing namespace is analogous to the namespace concept scheme.
 * </p>
 */
public class NamespaceConcept {

    private String encoding;
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
     * Create a namespace concept from a collection of triples.
     *
     * @param triples {@link Collection} of {@link RDFNode RDF node}
     * {@link TTriple triples}
     */
    public NamespaceConcept(Collection<TTriple<RDFNode>> triples) {
        TCharSet encodings = new TCharHashSet();
        for (TTriple<RDFNode> triple : triples) {
            RDFNode predicate = triple.getMiddle();
            if (!predicate.isResource()) continue;
            String predicateURI = predicate.asResource().getURI();

            if (predicateURI.equals(RDF_TYPE_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isResource()) continue;
                String conceptURI = object.asResource().getURI();
                if (!encodedConcept(conceptURI)) continue;
                char encoding = conceptToEncoding(conceptURI);
                encodings.add(encoding);
            } else if (predicateURI.equals(DC_IDENTIFIER_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isLiteral()) continue;
                this.identifier = object.asLiteral().getLexicalForm();
            } else if (predicateURI.equals(SKOS_PREF_LABEL_URI)) {
                RDFNode object = triple.getRight();
                if (!object.isLiteral()) continue;
                this.preflabel = object.asLiteral().getLexicalForm();
            }
        }
        if (encodings.size() > 0) {
            setEncoding(encodings);
        }
    }

    /**
     * Get whether this namespace concept encodes for a BEL concept.
     *
     * @return boolean
     */
    public boolean hasEncoding() {
        if (encoding == null) return false;
        return true;
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
     * Get this namespace concept's encoding.
     *
     * @return {@link String}; may be null
     */
    public String getEncoding() {
        return encoding;
    }

    /**
     * Get this namespace concept's identifier.
     *
     * @return {@link String}; may be null
     */
    public String getIdentifier() {
        return identifier;
    }

    private void setEncoding(TCharSet encodings) {
        boolean A, B, C, G, M, O, P, R;
        A = encodings.contains('A');
        B = encodings.contains('B');
        C = encodings.contains('C');
        G = encodings.contains('G');
        M = encodings.contains('M');
        O = encodings.contains('O');
        P = encodings.contains('P');
        R = encodings.contains('R');

        // redundant biological process when pathology
        if (B && O) encodings.remove('B');
        // redundant RNA abundance when micro RNA
        if (R && M) encodings.remove('R');
        // redundant abundance when any other abundance
        if (A && (C || G || M || P || R)) encodings.remove('A');

        char[] carr = new char[encodings.size()];
        TCharIterator chariter = encodings.iterator();
        for (int i = 0; i < carr.length; i++) {
            carr[i] = chariter.next();
        }
        sort(carr);
        this.encoding = new String(carr);
    }
}
