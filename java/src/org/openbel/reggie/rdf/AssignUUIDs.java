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

import org.apache.jena.query.*;

import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.vocabulary.RDF;
import org.apache.jena.vocabulary.RDFS;
import org.apache.jena.vocabulary.SKOS;
import org.apache.log4j.*;

import java.io.File;
import java.io.FileWriter;
import java.util.UUID;

import static java.lang.System.*;

/**
 * Assigns UUIDs to BEL namespace concepts.
 */
public class AssignUUIDs {

    private Logger log;
    private I i;
    private Q q;
    private Dataset dataset;
    private final static String BEL_UUID_CONCEPT_SCHEME;
    private final static String BEL_UUID_CONCEPT;
    private File output;
    private FileWriter writer;
    static {
        BEL_UUID_CONCEPT_SCHEME = "<http://www.openbel.org/vocabulary/UUIDConceptScheme>";
        BEL_UUID_CONCEPT = "<http://www.openbel.org/vocabulary/UUIDConcept>";
    }

    /**
     * @param dataset {@link Dataset}
     */
    public AssignUUIDs(Dataset dataset) throws Exception {
        log = Logger.getRootLogger();
        this.dataset = dataset;
        i = new I(dataset);
        q = new Q(dataset);
        String outputDir = getenv("RG_JAVA_OUTPUT");
        output = new File(outputDir, "uuids.nt");
        writer = new FileWriter(output, false);
    }

    String uuidIRI(String uuid) {
        return "<http://www.openbel.org/bel/uuid/".concat(uuid).concat(">");
    }

    String belNamespace(String path) {
        return "<http://www.openbel.org/bel/namespace/".concat(path).concat(">");
    }

    String rdfs(String path) {
        return "<http://www.w3.org/2000/01/rdf-schema#".concat(path).concat(">");
    }

    String skos(String path) {
        return "<http://www.w3.org/2004/02/skos/core#".concat(path).concat(">");
    }

    void assign() throws Exception {
        log.info("Started Generating UUID Assignments");
        log.info("Writing triples to: " + output.getAbsolutePath());
        StringBuilder bldr = new StringBuilder();
        bldr.append(BEL_UUID_CONCEPT_SCHEME + " ");
        bldr.append("<" + RDF.type.getURI() + "> ");
        bldr.append("<" + RDFS.Class.getURI() + "> .\n");
        bldr.append(BEL_UUID_CONCEPT_SCHEME + " ");
        bldr.append("<" + RDF.type.getURI() + "> ");
        bldr.append("<" + RDFS.Resource.getURI() + "> .\n");
        bldr.append(BEL_UUID_CONCEPT_SCHEME + " ");
        bldr.append("<" + RDFS.subClassOf.getURI() + "> ");
        bldr.append(BEL_UUID_CONCEPT_SCHEME + " .\n");
        bldr.append(BEL_UUID_CONCEPT_SCHEME + " ");
        bldr.append("<" + RDFS.subClassOf.getURI() + "> ");
        bldr.append("<" + SKOS.ConceptScheme.getURI() + "> .\n");
        writer.write(bldr.toString());

        QuerySolutions nsConceptIter = q.namespaceValues();
        for (QuerySolution nsConcept : nsConceptIter) {
            RDFNode subject = nsConcept.get("subject");
            String conceptIRI = subject.asResource().getURI();
            QuerySolutions eqConceptIter = q.equivalentConcepts(conceptIRI);

            String uuid = UUID.randomUUID().toString();
            String uuidIRI = uuidIRI(uuid);
            bldr.setLength(0);
            bldr.append(uuidIRI);
            bldr.append(" <" + RDF.type.getURI() + "> " + BEL_UUID_CONCEPT_SCHEME + " .\n");
            bldr.append(uuidIRI);
            bldr.append(" <" + RDF.type.getURI() + "> <" + SKOS.ConceptScheme.getURI() + "> .\n");
            writer.write(bldr.toString());

            for (QuerySolution eqConcept : eqConceptIter) {
                RDFNode eq = eqConcept.get("eq");
                String eqConceptIRI = eq.asResource().getURI();
                bldr.setLength(0);
                bldr.append("<".concat(eqConceptIRI).concat("> "));
                bldr.append(" <" + SKOS.inScheme.getURI() + "> " + uuidIRI + " .\n");
                bldr.append("<".concat(eqConceptIRI).concat("> "));
                bldr.append(" <" + RDF.type.getURI() + "> " + BEL_UUID_CONCEPT + " .\n");
                writer.write(bldr.toString());
            }

        }

        log.info("Completed Generating UUID Assignments");
        writer.close();
        exit(0);
    }

    public static void main(String... args) throws Exception {
        initLogging();
        final String tdbdata = getenv("RG_TDB_DATA");
        if (tdbdata == null) {
            err.println("RG_TDB_DATA is not set");
            exit(1);
        }
        final String env = getenv("RG_JAVA_OUTPUT");
        if (env == null) {
            err.println("RG_JAVA_OUTPUT is not set");
            exit(1);
        }

        Dataset dataset = TDBFactory.createDataset(tdbdata);
        AssignUUIDs au = new AssignUUIDs(dataset);
        au.assign();
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
