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
package org.openbel.reggie.rdf.generate.namespaces;

import org.apache.jena.query.*;
import org.apache.jena.rdf.model.*;
import org.apache.jena.reasoner.Reasoner;

import static org.apache.jena.rdf.model.ModelFactory.*;

import org.apache.jena.reasoner.rulesys.GenericRuleReasoner;
import org.apache.jena.reasoner.rulesys.Rule;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.vocabulary.OWL;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.SKOS;
import org.apache.log4j.*;
import static org.openbel.reggie.rdf.Constants.*;
import org.openbel.reggie.rdf.Q;
import org.openbel.reggie.rdf.QuerySolutions;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Stream;

import static java.util.stream.StreamSupport.*;

import static java.util.Spliterators.*;

import static java.lang.System.*;

/**
 * Generates BEL namespaces from the RDF.
 */
public class Main {

    private Dataset dataset;
    private final File templateDir;
    private final File outputDir;
    private Logger log;
    private Q q;

    public Main(Dataset dataset, File templateDir, File outputDir) {
        // connect to the existing data
        this.dataset = dataset;
        // where the templates are located
        this.templateDir = templateDir;
        // where the generated output goes
        this.outputDir = outputDir;
        q = new Q(this.dataset);
    }

    /**
     * Get namespace concepts.
     * <p>
     *     Queries subjects where {@code s} is a
     *     {@code belv:NamespaceConceptScheme}.
     * </p>
     *
     * @return {@link List} of {@link String strings}
     */
    List<String> getNamespaces() {
        List<String> ret = new ArrayList<>();
        try (QuerySolutions QS = q.namespaces()) {
            for (QuerySolution ns : QS) {
                RDFNode subject = ns.get("subject");
                String uri = subject.asResource().getURI();
                ret.add(uri);
            }
        }
        return ret;
    }

    /**
     * Map namespace concept URLs to their prefixes.
     * <p>
     *     For each namespace, query objects where the namespace {@code ns},
     *     {@code belv:prefix ?object}.
     * </p>
     *
     * @return {@link List} of {@link String strings}
     */
    Map<String, String> mapNamespaces(List<String> nsURLs) {
        RDFNode node;
        // start a read transaction
        dataset.begin(ReadWrite.READ);

        Map<String, String> map = new HashMap<>();
        String q1 = RDF_QUERY_PROLOGUE;
        q1 += "select ?object where { <";
        String q2 = "> belv:prefix ?object }";

        for (String nsURL : nsURLs) {
            String q = q1 + nsURL + q2;
            QueryExecution qe = QueryExecutionFactory.create(q, dataset);
            ResultSet rs = qe.execSelect();
            List<QuerySolution> solutions = consume(rs);
            assert solutions.size() == 1;
            node = solutions.get(0).get("object");
            Literal literal = node.asLiteral();
            String prefix = literal.getString();
            map.put(nsURL, prefix);
        }

        // end the read transaction
        dataset.end();
        return map;
    }

    void values(List<String> nsURLs) {
        String q;
        long t0 = currentTimeMillis();

        // start a read transaction
        dataset.begin(ReadWrite.READ);

        Map<String, String> map = new HashMap<>();
        String prologue = RDF_QUERY_PROLOGUE;

        // query for all values in a namespace
        String valuesQueryQ1 = prologue;
        valuesQueryQ1 += "select ?subject where { ?subject skos:inScheme <";
        String valuesQueryQ3 = "> }";

        // query for a specific value
        String valueQueryQ1 = prologue;
        valueQueryQ1 += "select ?predicate ?object where { <";
        String valueQueryQ3 = "> ?predicate ?object }";

        int queries = 0;
        int vqueries = 0;
        Set<Integer> hashes = new HashSet<>();

        for (String nsURL : nsURLs) {
            String valuesQueryQ2 = nsURL;
            q = valuesQueryQ1 + valuesQueryQ2 + valuesQueryQ3;
            QueryExecution qe = QueryExecutionFactory.create(q, dataset);
            ResultSet rs = qe.execSelect();
            queries += 1;
            while (rs.hasNext()) {
                QuerySolution valuesSolution = rs.next();
                RDFNode subject = valuesSolution.get("subject");
                Resource resource = subject.asResource();
                String nsval = resource.getURI();
                String valueQueryQ2 = nsval;
                hashes.add(nsval.hashCode());
                q = valueQueryQ1 + valueQueryQ2 + valueQueryQ3;
                qe = QueryExecutionFactory.create(q, dataset);
                ResultSet rs2 = qe.execSelect();
                vqueries += 1;
                if (hashes.size() != vqueries) {
                    out.println(hashes.size());
                    out.println(vqueries);
                }
                queries += 1;
                if (queries % 10000 == 0) {
                    out.println(queries);
                }
                while (rs2.hasNext()) {
                    QuerySolution valueSolution = rs2.next();
                }
            }
        }

        // end the read transaction
        dataset.end();

        long t1 = currentTimeMillis();
        out.println(queries + " in " + (t1 - t0) + " milliseconds");
    }

    public static void main(String... args) throws Exception {
        initLogging();
        final String tdbdata = getenv("RG_TDB_DATA");
        if (tdbdata == null) {
            err.println("RG_TDB_DATA is not set");
            exit(1);
        }

        final String templateDir = getenv("RG_JAVA_TEMPLATES");
        if (templateDir == null) {
            err.println("RG_JAVA_TEMPLATES is not set");
            exit(1);
        }

        final String outputDir = getenv("RG_JAVA_OUTPUT");
        if (outputDir == null) {
            err.println("RG_JAVA_TEMPLATES is not set");
            exit(1);
        }

        File templateDirFile = new File(templateDir);
        File outputDirFile = new File(outputDir);

        Dataset dataset = TDBFactory.createDataset(tdbdata);
        Main m = new Main(dataset, templateDirFile, outputDirFile);
    }

    private void tryReasoning() throws IOException {
        Model defaultModel = this.dataset.getDefaultModel();
        String SKOSEM = SKOS.exactMatch.getURI();
        String transitiveEM = "[TEM: (?a " + SKOSEM + " ?b) (?b " + SKOSEM + " ?c) -> (?a " + SKOSEM + " ?c)]";
        Rule rule = Rule.parseRule(transitiveEM);
        List<Rule> rules = Arrays.asList(new Rule[] { rule });
        Reasoner r = new GenericRuleReasoner(rules);

        defaultModel.add(SKOS.exactMatch, RDF.type, OWL.TransitiveProperty);
        //Reasoner OR = getOWLReasoner();
        InfModel inferredModel = createInfModel(r, defaultModel);

        /*
        String truleSrc = "[rule1: (?a eg:p ?b) (?b eg:p ?c) -> (?a eg:p ?c)]";
        List rules = Rule.parseRules(ruleSrc);
        Reasoner reasoner = new GenericRuleReasoner(rules);
        */


        out.println("Inferred model statement count:");
        out.println(count(inferredModel.listStatements()));
        out.println("Default model statement count:");
        out.println(count(defaultModel.listStatements()));

        //out.println("writing");
        //inferredModel.write(new FileWriter("somefile.ttl"), "TURTLE");
        //out.println("written");

        /*
        QueryExecution qe = QueryExecutionFactory.create("select ?s ?p ?o where { <http://www.openbel.org/bel/namespace/entrez-gene/24086> ?p ?o }", inferredModel);
        ResultSet resultSet = qe.execSelect();
        while (resultSet.hasNext()) {
            i += 1;
            out.println(i);
        }
        out.println(i);
        */

        /*
        stream(iterable(defaultModel.listStatements()).spliterator(), false).count();
        iterable(defaultModel.listStatements()).spliterator().

        for (Statement stmt : iterable(inferredmdl.listStatements())) {
            Resource subject = stmt.getSubject();
            Property predicate = stmt.getPredicate();
            RDFNode object = stmt.getObject();
            out.print(subject);
            out.print("\t");
            out.print(predicate);
            out.print("\t");
            out.print(object);
            out.println();
        }
        */
    }

    private void run() {
        Set<String> preds = new HashSet<>();
        List<String> namespaces = getNamespaces();
        Map<Integer, Map<Integer, Integer>> hashes = new HashMap<>();
        for (String ns : namespaces) {
            try (QuerySolutions subjects = Q.subjectsInScheme(dataset, ns)) {
                for (QuerySolution qs : subjects) {
                    RDFNode node = qs.get("subject");
                    String subject = node.asResource().getURI();

                    int sh = subject.hashCode();
                    if (!hashes.containsKey(sh)) {
                        hashes.put(sh, new HashMap<>());
                    }
                    Map<Integer, Integer> smap = hashes.get(sh);

                    try (QuerySolutions EMs = Q.objects(dataset, subject, SKOS_EXACT_MATCH)) {
                        for (QuerySolution em : EMs) {
                            node = em.get("predicate");
                            String predicate = node.asResource().getURI();
                            int ph = predicate.hashCode();
                            smap.put(ph, 1);

                            if (!hashes.containsKey(ph)) {
                                hashes.put(ph, new HashMap<>());
                            }
                            Map<Integer, Integer> pmap = hashes.get(ph);
                            pmap.put(sh, 0);
                        }
                    }


                    /*
                    try (QuerySolutions forsub = Q.forSubject(dataset, subject)) {
                        for (QuerySolution sN : forsub) {
                            RDFNode predicate = sN.get("predicate");
                            int cur = preds.size();
                            preds.add(predicate.toString());
                            int now = preds.size();
                            if (now != cur) {
                                out.println(preds);
                            }
                        }
                    }
                    */
                }
            }
        }

        out.println("checking keys");
        Set<Map.Entry<Integer, Map<Integer, Integer>>> entries = hashes.entrySet();
        for (Map.Entry<Integer, Map<Integer, Integer>> entry : entries) {
            int prikey = entry.getKey();
            Map<Integer, Integer> maps = entry.getValue();
            for (Map.Entry<Integer, Integer> entry2 : maps.entrySet()) {
                int seckey = entry2.getKey();
                int val = entry2.getValue();
                if (val == 0) {
                    out.println("val 0 for prikey " + prikey + " and seckey " + seckey);
                }
            }
        }
        out.println("done checking keys");

        //mapNamespaces(namespaces);
        //values(namespaces);
    }

    static <T> Iterable<T> iterable(Iterator<T> iter) {
        return new Iterable<T>() {
            @Override
            public Iterator<T> iterator() {
                return iter;
            }
        };
    }

    static <T> long count(Iterator<T> iter) {
        return stream(iterable(iter).spliterator(), false).count();
    }

    static <T> Stream<T> asDistinctStream(Iterator<T> iter) {
        int characteristic = Spliterator.DISTINCT;
        Spliterator<T> siter = spliteratorUnknownSize(iter, characteristic);
        Stream<T> strm = stream(siter, false); // false: sequential stream
        return strm;
    }

    static List<QuerySolution> consume(ResultSet results) {
        List<QuerySolution> ret = new ArrayList<>();
        while (results.hasNext()) {
            ret.add(results.next());
        }
        return ret;
    }

    static void initLogging() {
        ConsoleAppender ca = new ConsoleAppender();
        String PATTERN = "%d [%p|%C] %m%n";
        ca.setLayout(new PatternLayout(PATTERN));
        ca.setThreshold(Level.INFO);
        ca.activateOptions();
        Logger rlog = Logger.getRootLogger();
        rlog.addAppender(ca);
        rlog.setLevel(Level.INFO);
        rlog.log(Level.INFO, "Logging initialized");
    }
}
