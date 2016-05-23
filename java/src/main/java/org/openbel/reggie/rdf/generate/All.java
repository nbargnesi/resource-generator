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

import static java.lang.System.*;

import org.apache.jena.ext.com.google.common.collect.LinkedListMultimap;
import org.apache.jena.query.ARQ;
import org.apache.jena.query.Dataset;
import org.apache.jena.tdb.TDBFactory;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.openbel.reggie.rdf.generate.annotations.Main;

import java.io.File;
import java.util.LinkedList;
import java.util.List;

/**
 * Generates all BEL resources from the RDF.
 */
public class All {

    private Logger log;
    private Dataset dataset;

    /**
     * @param dataset {@link Dataset}
     */
    public All(Dataset dataset) {
        log = Logger.getRootLogger();
        this.dataset = dataset;
    }

    void generate() {
        log.info("Started Generating All Resources");

        // annotations
        org.openbel.reggie.rdf.generate.annotations.Main AM;
        AM = new Main(dataset);
        AM.generate();

        // namespaces
        org.openbel.reggie.rdf.generate.namespaces.Main NM;
        NM = new org.openbel.reggie.rdf.generate.namespaces.Main(dataset);
        NM.generate();

        // equivalences
        org.openbel.reggie.rdf.generate.equivalences.Main EM;
        EM = new org.openbel.reggie.rdf.generate.equivalences.Main(dataset);
        EM.generate();

        log.info("Completed Generating All Resources");
        exit(0);
    }

    private static String assertOrExit(String env) {
        String var = getenv(env);
        if (var != null) return var;
        err.println(env + " is not set");
        exit(1);
        return null; // dead code
    }

    private static void createOrExit(File path) {
        boolean mkdirs = path.mkdirs();
        if (mkdirs || path.isDirectory()) return;
        err.println("error creating path " + path.getAbsolutePath());
        exit(1);
    }

    private static void assertDir(String path) {
        File fpath = new File(path);
        if (fpath.isDirectory()) return;
        createOrExit(fpath);
    }

    public static void main(String... args) throws Exception {
        initLogging();

        // Santity check the environment
        final String tdbdata = assertOrExit("RG_TDB_DATA");
        assertOrExit("RG_JAVA_TEMPLATES");
        assertOrExit("RG_RESOURCE_VERSION");
        assertOrExit("RG_RESOURCE_DT");
        assertOrExit("RG_JAVA_TEMPLATES");
        List<String> paths = new LinkedList<>();
        paths.add(assertOrExit("RG_JAVA_OUTPUT"));
        paths.add(assertOrExit("RG_ANNO_OUTPUT"));
        paths.add(assertOrExit("RG_NS_OUTPUT"));
        paths.add(assertOrExit("RG_EQ_OUTPUT"));
        paths.forEach(All::assertDir);

        // Apache Jena 3.1 generates a NPE w/out this (2016-05-21)
        ARQ.init();
        Dataset dataset = TDBFactory.createDataset(tdbdata);
        All all = new All(dataset);
        all.generate();
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
            rlog.log(Level.INFO, "Setting log level: " + level);
            rlog.setLevel(Level.toLevel(level));
        }
    }
}
