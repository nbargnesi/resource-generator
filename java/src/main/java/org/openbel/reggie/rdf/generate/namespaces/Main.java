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

import org.apache.jena.tdb.TDBFactory;
import org.apache.log4j.*;

import static org.openbel.reggie.rdf.Functions.*;

import org.openbel.reggie.rdf.*;

import java.io.File;
import java.util.*;

import static java.lang.System.*;

/**
 * Generates BEL namespaces from the RDF.
 */
public class Main {

    private Logger log;
    private Q q;

    /**
     * @param dataset {@link Dataset}
     */
    public Main(Dataset dataset) {
        log = Logger.getRootLogger();
        q = new Q(dataset);
    }

    public void generate() {
        log.info("Started Generating Namespaces");
        QuerySolutions nsSchemeIter = q.namespaces();
        generate(nsSchemeIter);
        log.info("Completed Generating Namespaces");
    }

    void generate(QuerySolutions nsSchemeIter) {
        for (QuerySolution nsScheme : nsSchemeIter) {
            RDFNode subject = nsScheme.get("subject");
            String nsConceptScheme = subject.asResource().getURI();
            QuerySolutions nsConceptIter = q.namespaceValues(nsConceptScheme);

            QuerySolutions qs = q.preferredLabel(nsConceptScheme);
            RDFNode node = first(consume(qs, "label"));
            String nsPrefLabel = node.asLiteral().getLexicalForm();

            File[] templates = namespaceTemplates(nsPrefLabel);

            generate(nsConceptIter, templates);
        }
    }

    void generate(QuerySolutions nsConceptIter, File[] templates) {
        for (File FT : templates) {
            try (NamespaceTemplate NST = new NamespaceTemplate(FT)) {
                generate(nsConceptIter, NST);
            }
        }
    }

    void generate(QuerySolutions nsConceptIter, NamespaceTemplate template) {
        if (!nsConceptIter.more()) return;
        template.open();
        template.writeHeader();

        for (QuerySolution nsConcept : nsConceptIter) {
            RDFNode node = nsConcept.get("value");
            String valueConcept = node.asResource().getURI();

            List<TTriple<RDFNode>> triples = new LinkedList<>();
            for (QuerySolution valueQuery : q.subjectIsConcept(valueConcept)) {
                RDFNode predicate = valueQuery.get("predicate");
                RDFNode object = valueQuery.get("object");
                TTriple<RDFNode> triple = new TTriple<>();
                triple.setLeft(null);
                triple.setMiddle(predicate);
                triple.setRight(object);
                triples.add(triple);
            }

            NamespaceConcept concept = new NamespaceConcept(triples);
            template.writeValue(concept);
        }
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
            err.println("RG_JAVA_OUTPUT is not set");
            exit(1);
        }
        String env = getenv("RG_NS_OUTPUT");
        if (env == null) {
            err.println("RG_NS_OUTPUT is not set");
            exit(1);
        }
        File f = new File(env);
        if (!f.exists()) {
            boolean rslt = f.mkdirs();
            if (!rslt && !f.exists()) {
                err.println("error creating namespace output path " + env);
                exit(1);
            }
        }

        env = getenv("RG_RESOURCE_VERSION");
        if (env == null) {
            err.println("RG_RESOURCE_VERSION is not set");
            exit(1);
        }
        env = getenv("RG_RESOURCE_DT");
        if (env == null) {
            err.println("RG_RESOURCE_DT is not set");
            exit(1);
        }

        Dataset dataset = TDBFactory.createDataset(tdbdata);
        Main m = new Main(dataset);
        m.generate();
        exit(0);
    }

    static void initLogging() {
        ConsoleAppender ca = new ConsoleAppender();
        String PATTERN = "%d [%p|%C] %m%n";
        ca.setLayout(new PatternLayout(PATTERN));
        ca.activateOptions();
        Logger rlog = Logger.getRootLogger();
        rlog.addAppender(ca);
        rlog.setLevel(Level.INFO);
        rlog.log(Level.INFO, "Logging initialized");
        String level = getenv("RG_JAVA_LOG_LEVEL");
        if (level != null) {
            rlog.setLevel(Level.toLevel(level));
        }
    }
}
