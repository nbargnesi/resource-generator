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
import static org.apache.jena.update.UpdateExecutionFactory.*;
import static org.apache.jena.update.UpdateFactory.*;
import org.apache.jena.update.UpdateProcessor;
import org.apache.jena.update.UpdateRequest;

import static org.openbel.reggie.rdf.Constants.*;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/**
 * A collection of RDF insert functions.
 * <p>
 * An instance of this class can be constructed to simplify method
 * interaction.
 * </p>
 */
public class I {

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
        INSERT,

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
    private static final SPARQL_Atom insert;

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
        insert = SPARQL_Atom.INSERT;
    }

    /**
     * New I.
     *
     * @param dataset {@link Dataset}
     */
    public I(Dataset dataset) {
        this.dataset = dataset;
        this.bldr = new StringBuilder();
    }

    /**
     * Insert by insert clause..
     *
     * @param insert {@link String}
     */
    public void insert(String insert) {
        InsertStr is = new InsertStr();
        is.add(I.insert, lbrace);
        is.add(insert);
        is.add(rbrace);
        is.add(where, lbrace,rbrace);
        i(is.render());
    }

    private void i(String insert) {
        insert = Constants.RDF_PROLOGUE + insert;
        UpdateRequest ur = create(insert);
        UpdateProcessor proc = create(ur, this.dataset);
        proc.execute();
    }

    private void i(InsertStr insert) {
        i(insert.render());
    }

    private InsertStr is() {
        return new InsertStr();
    }

    /**
     * Internal class for making insert writing a bit more expressive.
     */
    final class InsertStr {

        /**
         * New query string.
         */
        public InsertStr() {
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
         * Add {@code insert}.
         */
        public InsertStr insert() {
            return add(insert);
        }

        /**
         * Add {@code where}.
         *
         * @return this
         */
        public InsertStr where() {
            return add(where, lbrace);
        }

        /**
         * Add one or more atoms.
         *
         * @param atoms {@link SPARQL_Atom}
         * @return this
         */
        public InsertStr add(SPARQL_Atom... atoms) {
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
        public InsertStr add(String... s) {
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
        public InsertStr addi(String... s) {
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
        public InsertStr s() {
            return add(s);
        }

        /**
         * Add {@code "?subject"};
         *
         * @return this
         */
        public InsertStr subject() {
            return add(subject);
        }

        /**
         * Add {@code "?predicate"};
         *
         * @return this
         */
        public InsertStr p() {
            return add(p);
        }

        /**
         * Add {@code "?predicate"};
         *
         * @return this
         */
        public InsertStr predicate() {
            return add(predicate);
        }

        /**
         * Add {@code "?object"};
         *
         * @return this
         */
        public InsertStr o() {
            return add(o);
        }

        /**
         * Add {@code "?object"};
         *
         * @return this
         */
        public InsertStr object() {
            return add(object);
        }

        /**
         * Add {@code "a"};
         *
         * @return this
         */
        public InsertStr a() {
            return add(a);
        }

        /**
         * Add {@code "a"};
         *
         * @return this
         */
        public InsertStr is_a() {
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
            case INSERT:
                return "insert";

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
