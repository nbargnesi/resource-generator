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

import static org.openbel.reggie.rdf.Constants.*;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/**
 * A collection of RDF query functions.
 * <p>
 * An instance of this class can be constructed to simplify method
 * interaction.
 * </p>
 */
public class Q {

    private final Dataset dataset;
    private final StringBuilder bldr;

    private enum SPARQL_Atom {
        // keywords
        BASE, PREFIX, SELECT, CONSTRUCT, DESCRIBE, ASK,
        ORDER_BY, LIMIT, OFFSET, DISTINCT, REDUCED,
        FROM, FROM_NAMED, WHERE,
        GRAPH, OPTIONAL, UNION, FILTER, A,
        STR, LANG, LANGMATCHES, DATATYPE, BOUND, SAMETERM,
        ISURI, ISIRI, ISLITERAL, REGEX, TRUE, FALSE,

        // common syntax
        SUBJECT, PREDICATE, OBJECT,

        // structural elements
        START_GROUP_GRAPH_PATTERN, END_GROUP_GRAPH_PATTERN, DOT,
        START_IRI_REF, END_IRI_REF
    }

    private static final SPARQL_Atom base;
    private static final SPARQL_Atom prefix;
    private static final SPARQL_Atom select;
    private static final SPARQL_Atom construct;
    private static final SPARQL_Atom describe;
    private static final SPARQL_Atom ask;
    private static final SPARQL_Atom order_by;
    private static final SPARQL_Atom limit;
    private static final SPARQL_Atom offset;
    private static final SPARQL_Atom distinct;
    private static final SPARQL_Atom reduced;
    private static final SPARQL_Atom from;
    private static final SPARQL_Atom from_named;
    private static final SPARQL_Atom where;
    private static final SPARQL_Atom graph;
    private static final SPARQL_Atom optional;
    private static final SPARQL_Atom union;
    private static final SPARQL_Atom filter;
    private static final SPARQL_Atom a;
    private static final SPARQL_Atom is_a;
    private static final SPARQL_Atom str;
    private static final SPARQL_Atom lang;
    private static final SPARQL_Atom lang_matches;
    private static final SPARQL_Atom datatype;
    private static final SPARQL_Atom bound;
    private static final SPARQL_Atom sameterm;
    private static final SPARQL_Atom is_uri;
    private static final SPARQL_Atom is_iri;
    private static final SPARQL_Atom is_literal;
    private static final SPARQL_Atom regex;
    private static final SPARQL_Atom subject;
    private static final SPARQL_Atom s;
    private static final SPARQL_Atom predicate;
    private static final SPARQL_Atom p;
    private static final SPARQL_Atom object;
    private static final SPARQL_Atom o;
    private static final SPARQL_Atom lbrace;
    private static final SPARQL_Atom rbrace;
    private static final SPARQL_Atom dot;
    private static final SPARQL_Atom lt;
    private static final SPARQL_Atom gt;

    static {
        base = SPARQL_Atom.BASE;
        select = SPARQL_Atom.SELECT;
        prefix = SPARQL_Atom.PREFIX;
        construct = SPARQL_Atom.CONSTRUCT;
        describe = SPARQL_Atom.DESCRIBE;
        ask = SPARQL_Atom.ASK;
        order_by = SPARQL_Atom.ORDER_BY;
        limit = SPARQL_Atom.LIMIT;
        offset = SPARQL_Atom.OFFSET;
        distinct = SPARQL_Atom.DISTINCT;
        reduced = SPARQL_Atom.REDUCED;
        from = SPARQL_Atom.FROM;
        from_named = SPARQL_Atom.FROM_NAMED;
        where = SPARQL_Atom.WHERE;
        graph = SPARQL_Atom.GRAPH;
        optional = SPARQL_Atom.OPTIONAL;
        union = SPARQL_Atom.UNION;
        filter = SPARQL_Atom.FILTER;
        a = SPARQL_Atom.A;
        is_a = SPARQL_Atom.A;
        str = SPARQL_Atom.STR;
        lang = SPARQL_Atom.LANG;
        lang_matches = SPARQL_Atom.LANGMATCHES;
        datatype = SPARQL_Atom.DATATYPE;
        bound = SPARQL_Atom.BOUND;
        sameterm = SPARQL_Atom.SAMETERM;
        is_uri = SPARQL_Atom.ISURI;
        is_iri = SPARQL_Atom.ISIRI;
        is_literal = SPARQL_Atom.ISLITERAL;
        regex = SPARQL_Atom.REGEX;
        subject = SPARQL_Atom.SUBJECT;
        s = SPARQL_Atom.SUBJECT;
        predicate = SPARQL_Atom.PREDICATE;
        p = SPARQL_Atom.PREDICATE;
        object = SPARQL_Atom.OBJECT;
        o = SPARQL_Atom.OBJECT;
        lbrace = SPARQL_Atom.START_GROUP_GRAPH_PATTERN;
        rbrace = SPARQL_Atom.END_GROUP_GRAPH_PATTERN;
        dot = SPARQL_Atom.DOT;
        lt = SPARQL_Atom.START_IRI_REF;
        gt = SPARQL_Atom.END_IRI_REF;
    }

    /**
     * New Q.
     *
     * @param dataset {@link Dataset}
     */
    public Q(Dataset dataset) {
        this.dataset = dataset;
        this.bldr = new StringBuilder();
    }

    /**
     * Get subjects of type <i>type</i>.
     *
     * @param type {@link String}
     * @return {@link QuerySolutions}
     */
    public QuerySolutions subjectIsA(String type) {
        QueryStr qs = qs();
        qs.add(select, s, where, lbrace, s, is_a);
        qs.add(type);
        qs.add(rbrace);
        return q(qs);
    }

    /**
     * Get subjects where {@code ?subject <predicate> <object>}.
     *
     * @param predicate {@link String}
     * @param object    {@link String}
     * @return {@link QuerySolutions}
     */
    public QuerySolutions subject(String predicate, String object) {
        QueryStr qs = qs();
        qs.add(select, s, where, lbrace, s);
        qs.add(predicate, object);
        qs.add(rbrace);
        return q(qs);
    }

    /**
     * Get subjects where {@code ?subject skos:inScheme <concept>}.}
     *
     * @param concept {@link String}
     * @return {@link QuerySolutions}
     */
    public QuerySolutions subjectInScheme(String concept) {
        String predicate = Constants.SKOS_IN_SCHEME;
        return subject(predicate, concept);
    }

    /**
     * Get predicate and objects where {@code <concept> ?p ?o}, binding
     * {@code "predicate"} and {@code "object"}.
     *
     * @param concept {@link String}
     * @return {@link QuerySolutions}
     */
    public QuerySolutions subjectIsConcept(String concept) {
        QueryStr qs = qs();
        // select ?p ?o where {
        qs.add(select, p, o, where, lbrace);
        // <concept> ?p ?o }
        qs.addi(concept).add(p, o, rbrace);
        return q(qs);
    }

    /**
     * BEL namespaces bound to {@code "subject"}.
     * <p>
     * <code>
     * try (QuerySolutions QS = namespaces()) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode s = qs.get("subject");
     *     }
     * }
     * </code>
     * </p>
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions namespaces() {
        return subjectIsA(BELV_NAMESPACE_CONCEPT_SCHEME);
    }

    /**
     * BEL namespace pref labels bound to {@code "label"}.
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions namespacePrefLabels() {
        QueryStr qs = qs();
        // select ?label where {
        qs.add(select).add("?label").add(where, lbrace);
        // ?s a belv:NamespaceConceptScheme .
        qs.add(s, is_a).add(BELV_NAMESPACE_CONCEPT_SCHEME).add(dot);
        // ?s
        qs.add(s);
        // skos:prefLabel
        qs.add(Constants.SKOS_PREF_LABEL);
        // ?label
        qs.add("?label");
        // . }
        qs.add(dot, rbrace);
        return q(qs);
    }

    /**
     * Get the preferred label of a concept bound to {@code "label"}.
     *
     * @param concept {@link String}
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions preferredLabel(String concept) {
        QueryStr qs = qs();
        // select ?label where {
        qs.add(select).add("?label").add(where, lbrace);
        // <concept> skos:prefLabel ?label
        qs.addi(concept).add(Constants.SKOS_PREF_LABEL).add("?label");
        // . }
        qs.add(dot, rbrace);
        return q(qs);
    }

    /**
     * BEL namespace values bound to {@code "subject"}.
     * <p>
     * <code>
     * try (QuerySolutions QS = namespacesValues()) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode s = qs.get("subject");
     *     }
     * }
     * </code>
     * </p>
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions namespaceValues() {
        return subjectIsA(BELV_NAMESPACE_CONCEPT);
    }

    /**
     * BEL namespace values bound to {@code "value"} and constrained to
     * <i>concept</i> (i.e., <i>skos:inScheme</i> of <i>concept</i>).
     * @param concept {@link String}
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions namespaceValues(String concept) {
        QueryStr qs = qs();
        // select ?value where {
        qs.add(select).add("?value").add(where, lbrace);
        // ?s skos:inScheme
        qs.add("?value").add(Constants.SKOS_IN_SCHEME);
        // <concept> . }
        qs.addi(concept).add(dot, rbrace);
        return q(qs);
    }

    /**
     * BEL annotations bound to {@code "subject"}.
     * <p>
     * <code>
     * try (QuerySolutions QS = annotations()) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode s = qs.get("subject");
     *     }
     * }
     * </code>
     * </p>
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions annotations() {
        return subjectIsA(BELV_ANNOTATION_CONCEPT_SCHEME);
    }

    /**
     * BEL annotation values bound to {@code "subject"}.
     * <p>
     * <code>
     * try (QuerySolutions QS = annotationValues()) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode s = qs.get("subject");
     *     }
     * }
     * </code>
     * </p>
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions annotationValues() {
        return subjectIsA(BELV_ANNOTATION_CONCEPT);
    }

    /**
     * BEL annotation values bound to {@code "value"} and constrained to
     * <i>concept</i> (i.e., <i>skos:inScheme</i> of <i>concept</i>).
     * @param concept {@link String}
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions annotationValues(String concept) {
        QueryStr qs = qs();
        // select ?value where {
        qs.add(select).add("?value").add(where, lbrace);
        // ?s skos:inScheme
        qs.add("?value").add(Constants.SKOS_IN_SCHEME);
        // <concept> . }
        qs.addi(concept).add(dot, rbrace);
        return q(qs);
    }

    /**
     * BEL annotation pref labels bound to {@code "label"}.
     *
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public QuerySolutions annotationPrefLabels() {
        QueryStr qs = qs();
        // select ?label where {
        qs.add(select).add("?label").add(where, lbrace);
        // ?s a belv:NamespaceConceptScheme .
        qs.add(s, is_a).add(BELV_ANNOTATION_CONCEPT_SCHEME).add(dot);
        // ?s
        qs.add(s);
        // skos:prefLabel
        qs.add(Constants.SKOS_PREF_LABEL);
        // ?label
        qs.add("?label");
        // . }
        qs.add(dot, rbrace);
        return q(qs);
    }

    /**
     * Get subjects in <i>concept</i>.
     * <p>
     * The iterable returned will bind {@code subject} variables.
     * For example,
     * <code>
     * try (QuerySolutions QS = subjectsInScheme(ds, concept)) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode subject = qs.get("subject");
     *     }
     * }
     * </code>
     * </p>
     *
     * @param ds     {@link Dataset}
     * @param concept SKOS concept
     * @return {@link QuerySolutions} Iterable query solutions
     */
    public static QuerySolutions subjectsInScheme(Dataset ds, String concept) {
        StringBuilder bldr = new StringBuilder();
        bldr.append(RDF_QUERY_PROLOGUE);
        bldr.append("select ?subject where { ?subject skos:inScheme <");
        bldr.append(concept);
        bldr.append("> }");
        String q = bldr.toString();
        return new QuerySolutions(ds, q);
    }

    /**
     * Get all solutions for <i>subject</i>.
     * <p>
     * The iterable returned will bind {@code predicate} and {@code object}
     * variables. For example,
     * <code>
     * try (QuerySolutions QS = forSubject(ds, subject)) {
     *     for (QuerySolution qs : QS) {
     *         RDFNode predicate = qs.get("predicate");
     *         RDFNode object = qs.get("object");
     *     }
     * }
     * </code>
     * </p>
     *
     * @param ds      {@link Dataset}
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
     * The iterable returned will bind {@code object} variables. For
     * example,
     * <code>
     * try (QuerySolutions QS = forSubject(ds, subject, predicate)) {
     * for (QuerySolution qs : QS) {
     * RDFNode object = qs.get("object");
     * }
     * }
     * </code>
     * </p>
     *
     * @param ds        {@link Dataset}
     * @param subject   Subject
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

    /**
     * Select-where query.
     *
     * @param select {@link String}
     * @param where  {@link String}
     * @return {@link QuerySolutions}
     */
    public QuerySolutions selectWhere(String select, String where) {
        QueryStr qs = new QueryStr();
        qs.add(Q.select);
        qs.add(select);
        qs.add(Q.where, lbrace);
        qs.add(where);
        qs.add(rbrace);
        return q(qs.render());
    }

    private QuerySolutions q(String query) {
        query = Constants.RDF_QUERY_PROLOGUE + query;
        return new QuerySolutions(this.dataset, query);
    }

    private QuerySolutions q(QueryStr query) {
        return q(query.render());
    }

    private QueryStr qs() {
        return new QueryStr();
    }

    /**
     * Internal class for making query writing a bit more expressive.
     * <p>
     * <code>
     * QueryStr qs = new QueryStr();
     * qs.add(select, s, p, o, where, lbrace, s, p, o, rbrace);
     * String query = qs.render();
     * </code>
     * </p>
     */
    final class QueryStr {

        /**
         * New query string.
         */
        public QueryStr() {
            reset();
        }

        void reset() {
            bldr.setLength(0);
        }

        /**
         * Build a query and render it.
         *
         * @param atoms One or more {@link SPARQL_Atom atoms}
         * @return {@link String}
         * @see #add(SPARQL_Atom...)
         */
        public String make(SPARQL_Atom... atoms) {
            return add(atoms).render();
        }

        /**
         * Add {@code select}.
         */
        public QueryStr select() {
            return add(select);
        }

        /**
         * Add {@code where}.
         *
         * @return this
         */
        public QueryStr where() {
            return add(where, lbrace);
        }

        /**
         * Add one or more atoms.
         *
         * @param atoms {@link SPARQL_Atom}
         * @return this
         */
        public QueryStr add(SPARQL_Atom... atoms) {
            Stream<SPARQL_Atom> astream = Stream.of(atoms);
            List<String> strings = new ArrayList<>(atoms.length);
            astream.forEach((x) -> {
                strings.add(str(x));
            });
            return add(strings.toArray(new String[0]));
        }

        /**
         * Add one or more strings.
         *
         * @param s {@link String strings}
         * @return this
         */
        public QueryStr add(String... s) {
            if (s == null) throw new IllegalArgumentException();
            Stream<String> sstream = Stream.of(s);
            sstream.forEach((x) -> {
                bldr.append(x);
                bldr.append(" ");
            });
            return this;
        }

        /**
         * Add one or more IRI ref strings.
         *
         * @param s {@link String strings}
         * @return this
         */
        public QueryStr addi(String... s) {
            if (s == null) throw new IllegalArgumentException();
            Stream<String> sstream = Stream.of(s);
            sstream.forEach((x) -> {
                bldr.append(str(lt));
                bldr.append(x);
                bldr.append(str(gt));
                bldr.append(" ");
            });
            return this;
        }

        /**
         * Add {@code "?subject"};
         *
         * @return this
         */
        public QueryStr s() {
            return add(s);
        }

        /**
         * Add {@code "?subject"};
         *
         * @return this
         */
        public QueryStr subject() {
            return add(subject);
        }

        /**
         * Add {@code "?predicate"};
         *
         * @return this
         */
        public QueryStr p() {
            return add(p);
        }

        /**
         * Add {@code "?predicate"};
         *
         * @return this
         */
        public QueryStr predicate() {
            return add(predicate);
        }

        /**
         * Add {@code "?object"};
         *
         * @return this
         */
        public QueryStr o() {
            return add(o);
        }

        /**
         * Add {@code "?object"};
         *
         * @return this
         */
        public QueryStr object() {
            return add(object);
        }

        /**
         * Add {@code "a"};
         *
         * @return this
         */
        public QueryStr a() {
            return add(a);
        }

        /**
         * Add {@code "a"};
         *
         * @return this
         */
        public QueryStr is_a() {
            return add(is_a);
        }

        /**
         * Render the query string.
         *
         * @return {@link String}
         */
        public String render() {
            return bldr.toString();
        }

    }

    private static String str(SPARQL_Atom atom) {
        switch (atom) {
            // keywords
            case BASE:
                return "BASE";
            case PREFIX:
                return "PREFIX";
            case SELECT:
                return "SELECT";
            case CONSTRUCT:
                return "CONSTRUCT";
            case DESCRIBE:
                return "DESCRIBE";
            case ASK:
                return "ASK";
            case ORDER_BY:
                return "ORDER BY";
            case LIMIT:
                return "LIMIT";
            case OFFSET:
                return "OFFSET";
            case DISTINCT:
                return "DISTINCT";
            case REDUCED:
                return "REDUCED";
            case FROM:
                return "FROM";
            case FROM_NAMED:
                return "FROM NAMED";
            case WHERE:
                return "WHERE";
            case GRAPH:
                return "GRAPH";
            case OPTIONAL:
                return "OPTIONAL";
            case UNION:
                return "UNION";
            case FILTER:
                return "FILTER";
            case A:
                return "a";
            case STR:
                return "str";
            case LANG:
                return "lang";
            case LANGMATCHES:
                return "langMatches";
            case DATATYPE:
                return "datatype";
            case BOUND:
                return "bound";
            case SAMETERM:
                return "sameTerm";
            case ISURI:
                return "isURI";
            case ISIRI:
                return "isIRI";
            case ISLITERAL:
                return "isLITERAL";
            case REGEX:
                return "REGEX";
            case TRUE:
                return "true";
            case FALSE:
                return "false";

            // common syntax
            case SUBJECT:
                return "?subject";
            case PREDICATE:
                return "?predicate";
            case OBJECT:
                return "?object";

            // structural elements
            case START_GROUP_GRAPH_PATTERN:
                return "{";
            case END_GROUP_GRAPH_PATTERN:
                return "}";
            case DOT:
                return ".";
            case START_IRI_REF:
                return "<";
            case END_IRI_REF:
                return ">";
        }
        throw new UnsupportedOperationException();
    }

}
