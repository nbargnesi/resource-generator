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

import org.apache.jena.riot.Lang;
import org.apache.jena.riot.RDFDataMgr;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.apache.jena.query.*;

import org.apache.jena.tdb.TDBFactory;

import java.io.File;
import java.io.FileOutputStream;

import static java.lang.System.*;

/**
 * Exports a turtle dump.
 */
public class ExportTurtle {
    private Logger log;
    private Dataset dataset;

    ExportTurtle(String tdbdata) {
        log = Logger.getRootLogger();
        String level = getenv("RG_JAVA_LOG_LEVEL");
        if (level != null) {
            log.setLevel(Level.toLevel(level));
        }
        this.dataset = TDBFactory.createDataset(tdbdata);
    }

    void run() throws Exception {
        String outputFile = "resource-generator-turtle-export.ttl";
        File file = new File(outputFile);
        FileOutputStream fos = new FileOutputStream(file);
        log.info("Writing " + file.getName());
        RDFDataMgr.write(fos, dataset.getDefaultModel(), Lang.TURTLE);
        log.info("Finished writing to " + file.getAbsolutePath());
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
        ExportTurtle export = new ExportTurtle(tdbdata);
        export.run();
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
