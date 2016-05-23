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
package org.openbel.reggie.rdf.generate;

import org.apache.jena.query.ARQ;
import org.apache.jena.query.Dataset;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.tdb.TDBFactory;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.openbel.reggie.rdf.Q;
import org.openbel.reggie.rdf.QuerySolutions;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import static java.lang.System.*;

/**
 * Shows namespaces currently known about.
 */
public class ShowNamespaces {

    private Q q;
    private Logger log;

    private ShowNamespaces(String tdbdata) {
        Dataset dataset = TDBFactory.createDataset(tdbdata);
        q = new Q(dataset);
        log = Logger.getRootLogger();
        String level = getenv("RG_JAVA_LOG_LEVEL");
        if (level != null) {
            log.setLevel(Level.toLevel(level));
        }
    }

    private void run() {
        List<String> NSs = new ArrayList<>();
        try (QuerySolutions QS = q.namespacePrefLabels()) {
            for (QuerySolution nsPL : QS) {
                RDFNode node = nsPL.get("label");
                String nl = node.asLiteral().getString();
                nl = nl.replace(' ', '-');
                nl = nl.toLowerCase();
                NSs.add(nl);
            }
        }
        log.info("Found " + NSs.size() + " namepsaces.");
        for (int i = 0; i < NSs.size(); i++) {
            log.info((i + 1) + ": " + NSs.get(i));
        }
    }

    public static void main(String... args) throws Exception {
        initLogging();
        final String tdbdata = getenv("RG_TDB_DATA");
        if (tdbdata == null) {
            err.println("RG_TDB_DATA is not set");
            exit(1);
        }
        // Apache Jena 3.1 generates a NPE w/out this (2016-05-21)
        ARQ.init();
        ShowNamespaces check = new ShowNamespaces(tdbdata);
        check.run();
    }

    private static void initLogging() {
        ConsoleAppender ca = new ConsoleAppender();
        String PATTERN = "%d [%p|%C] %m%n";
        ca.setLayout(new PatternLayout(PATTERN));
        ca.activateOptions();
        Logger rlog = Logger.getRootLogger();
        rlog.addAppender(ca);
        rlog.setLevel(Level.INFO);
        rlog.log(Level.INFO, "Logging initialized");
    }

}
