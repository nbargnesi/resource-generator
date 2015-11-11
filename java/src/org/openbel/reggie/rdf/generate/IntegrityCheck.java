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

import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.*;

import org.apache.jena.tdb.TDBFactory;
import org.openbel.reggie.rdf.Q;
import org.openbel.reggie.rdf.QuerySolutions;

import java.io.File;

import static java.lang.System.*;

/**
 * Checks the integrity of the RDF data and templates.
 */
public class IntegrityCheck {

    private String templateDir;
    private Q q;
    private Logger log;

    IntegrityCheck(String tdbdata, String templateDir) {
        Dataset dataset = TDBFactory.createDataset(tdbdata);
        this.templateDir = templateDir;
        q = new Q(dataset);
        log = Logger.getRootLogger();
        String level = getenv("RG_JAVA_LOG_LEVEL");
        if (level != null) {
            log.setLevel(Level.toLevel(level));
        }
    }

    void run() {
        boolean missing = false;
        try (QuerySolutions QS = q.namespacePrefLabels()) {
            for (QuerySolution nsPL : QS) {
                RDFNode node = nsPL.get("label");
                String pl = node.asLiteral().getString();
                pl = pl.replace(' ', '-');
                pl = pl.toLowerCase();
                boolean haveOne = haveNSTemplate(pl);
                if (!haveOne) missing = true;

            }
        }
        try (QuerySolutions QS = q.annotationPrefLabels()) {
            for (QuerySolution annoPL : QS) {
                RDFNode node = annoPL.get("label");
                String pl = node.asLiteral().getString();
                pl = pl.replace(' ', '-');
                pl = pl.toLowerCase();
                boolean have = haveAnnoTemplate(pl);
                if (!have) missing = true;
            }
        }
        if (missing) log.warn("WARNING: Missing templates reported!");
        else log.info("SUCCESS: Templates exist for all resources.");
    }

    boolean haveNSTemplate(String nslabel) {
        String belns = nslabel + "-belns.st";
        File template1 = new File(templateDir, belns);
        boolean t1 = template1.canRead();
        String ids = nslabel + "-ids-belns.st";
        File template2 = new File(templateDir, ids);
        boolean t2 = template2.canRead();

        String p1 = template1.getAbsolutePath();
        String p2 = template2.getAbsolutePath();

        if (!t1 && !t2) {
            log.warn("Missing templates for namespace: " + nslabel);
            log.warn("missing template: " + p1);
            log.warn("missing template: " + p2);
            return false;
        }
        if (!t1) {
            log.debug("Missing name template for namespace: " + nslabel);
            log.debug("missing template: " + p1);
        }
        if (!t2) {
            log.debug("Missing id template for namespace: " + nslabel);
            log.debug("missing template: " + p2);
        }
        return true;
    }

    boolean haveAnnoTemplate(String annolabel) {
        String belanno = annolabel + "-belanno.st";
        File template = new File(templateDir, belanno);
        boolean t = template.canRead();
        String p = template.getAbsolutePath();

        if (!t) {
            log.warn("Missing template for annotation: " + annolabel);
            log.warn("missing template: " + p);
            return false;
        }
        return true;
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
        IntegrityCheck check = new IntegrityCheck(tdbdata, templateDir);
        check.run();
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
    }

}
