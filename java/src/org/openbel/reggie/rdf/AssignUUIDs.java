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
import org.apache.log4j.*;

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

    /**
     * @param dataset {@link Dataset}
     */
    public AssignUUIDs(Dataset dataset) {
        log = Logger.getRootLogger();
        this.dataset = dataset;
        i = new I(dataset);
        q = new Q(dataset);
    }

    String uuidIRI(String uuid) {
        return "<http://www.openbel.org/bel/uuid/".concat(uuid).concat(">");
    }

    void assign() {
        log.info("Started");
        StringBuilder bldr = new StringBuilder();
        bldr.append("belv:UUIDConceptScheme a rdfs:Class . ");
        bldr.append("belv:UUIDConceptScheme a rdfs:Resource . ");
        bldr.append("belv:UUIDConceptScheme rdfs:subClassOf belv:UUIDConceptScheme . ");
        bldr.append("belv:UUIDConceptScheme rdfs:subClassOf skos:ConceptScheme . ");
        i.insert(bldr.toString());

        QuerySolutions nsConceptIter = q.namespaceValues();
        for (QuerySolution nsConcept : nsConceptIter) {
            RDFNode subject = nsConcept.get("subject");
            String conceptIRI = subject.asResource().getURI();
            QuerySolutions eqConceptIter = q.equivalentConcepts(conceptIRI);

            dataset.begin(ReadWrite.WRITE);

            String uuid = UUID.randomUUID().toString();
            String uuidIRI = uuidIRI(uuid);
            bldr.setLength(0);
            bldr.append(uuidIRI);
            bldr.append(" a belv:UUIDConceptScheme . ");
            bldr.append(uuidIRI);
            bldr.append(" a skos:ConceptScheme . ");
            i.insert(bldr.toString());

            for (QuerySolution eqConcept : eqConceptIter) {
                RDFNode eq = eqConcept.get("eq");
                String eqConceptIRI = eq.asResource().getURI();
                bldr.setLength(0);
                bldr.append("<".concat(eqConceptIRI).concat(">"));
                bldr.append(" skos:inScheme ");
                bldr.append(uuidIRI);
                bldr.append(" . ");
                i.insert(bldr.toString());
            }

            dataset.end();
        }

        log.info("Completed");
        exit(0);
    }

    public static void main(String... args) throws Exception {
        initLogging();
        final String tdbdata = getenv("RG_TDB_DATA");
        if (tdbdata == null) {
            err.println("RG_TDB_DATA is not set");
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
