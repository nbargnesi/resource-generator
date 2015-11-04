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

import org.apache.jena.query.Dataset;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.rdf.model.RDFNode;
import static org.openbel.reggie.rdf.Constants.*;

import java.util.ArrayList;
import java.util.List;
import static java.lang.String.format;

/**
 * A collection of RDF query functions.
 */
public class Q {

    /**
     * Get the {@link RDFNode RDF nodes} that are BEL namespaces.
     * @param ds {@link Dataset}
     * @return {@link List} of {@link RDFNode RDF nodes}
     */
    public static List<RDFNode> getNamespaces(Dataset ds) {
        StringBuilder bldr = new StringBuilder();
        bldr.append(RDF_QUERY_PROLOGUE);
        bldr.append("select ?s where { ?s a ");
        bldr.append(BELV_NAMESPACE_CONCEPT_SCHEME);
        bldr.append(" }");
        String q = bldr.toString();

        List<RDFNode> ret = new ArrayList<>();
        try (QuerySolutions qs = new QuerySolutions(ds, q)) {
            for (QuerySolution solution : qs) {
                ret.add(solution.get("s"));
            }
        }
        return ret;
    }

    /**
     * Get subjects in <i>scheme</i>.
     * <p>
     *     The iterable returned will bind {@code subject} variables.
     *     For example,
     *     <code>
     *         try (QuerySolutions QS = subjectsInScheme(ds, scheme)) {
     *             for (QuerySolution qs : QS) {
     *                 RDFNode subject = qs.get("subject");
     *             }
     *         }
     *     </code>
     * </p>
     * @param ds {@link Dataset}
     * @param scheme SKOS scheme
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public static QuerySolutions subjectsInScheme(Dataset ds, String scheme) {
        StringBuilder bldr = new StringBuilder();
        bldr.append(RDF_QUERY_PROLOGUE);
        bldr.append("select ?subject where { ?subject skos:inScheme <");
        bldr.append(scheme);
        bldr.append("> }");
        String q = bldr.toString();
        return new QuerySolutions(ds, q);
    }

    /**
     * Get all solutions for <i>subject</i>.
     * <p>
     *     The iterable returned will bind {@code predicate} and {@code object}
     *     variables. For example,
     *     <code>
     *         try (QuerySolutions QS = forSubject(ds, subject)) {
     *             for (QuerySolution qs : QS) {
     *                 RDFNode predicate = qs.get("predicate");
     *                 RDFNode object = qs.get("object");
     *             }
     *         }
     *     </code>
     * </p>
     * @param ds {@link Dataset}
     * @param subject Subject
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public static QuerySolutions forSubject(Dataset ds, String subject) {
        StringBuilder bldr = new StringBuilder();
        bldr.append(RDF_QUERY_PROLOGUE);
        bldr.append("select ?predicate ?object where { <");
        bldr.append(subject);
        bldr.append("> ?predicate ?object }");
        String q = bldr.toString();
        return new QuerySolutions(ds, q);
    }

    /**
     * Get all objects for <i>subject</i> and <i>predicate</i>.
     * <p>
     *     The iterable returned will bind {@code object} variables. For
     *     example,
     *     <code>
     *         try (QuerySolutions QS = forSubject(ds, subject, predicate)) {
     *             for (QuerySolution qs : QS) {
     *                 RDFNode object = qs.get("object");
     *             }
     *         }
     *     </code>
     * </p>
     * @param ds {@link Dataset}
     * @param subject Subject
     * @param predicate Predicate
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public static QuerySolutions objects(Dataset ds, String subject,
                                         String predicate) {
        StringBuilder bldr = new StringBuilder();
        bldr.append(RDF_QUERY_PROLOGUE);
        bldr.append("select ?object where { <");
        bldr.append(subject);
        bldr.append("> <");
        bldr.append(predicate);
        bldr.append("> ?object }");
        String q = bldr.toString();
        return new QuerySolutions(ds, q);
    }

}
