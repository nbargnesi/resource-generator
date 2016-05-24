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

import org.apache.log4j.Logger;
import org.stringtemplate.v4.ST;
import org.stringtemplate.v4.STGroupDir;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import static java.lang.System.*;
import static java.lang.String.format;

/**
 * BEL annotation template.
 */
public class AnnotationTemplate implements AutoCloseable {

    private final String uri;
    private final String version;
    private final String createdDateTime;
    private final File templateFile;
    private final String templateName;
    private final Logger log;
    private boolean ids = false;
    private File outputFile;
    private FileWriter writer;
    private boolean opened = false;

    /**
     * Create a annotation template associated with the indicated {@link File template file}.
     *
     * @param uri {@link String}
     * @param templateFile {@link File}
     */
    public AnnotationTemplate(String uri, File templateFile) {
        this.uri = uri;
        log = Logger.getRootLogger();
        if (!templateFile.canRead()) {
            final String fmt = "%s: can't read template";
            final String msg = format(fmt, templateFile.getAbsolutePath());
            throw new IllegalArgumentException(msg);
        }
        this.templateFile = templateFile;
        version = getenv("RG_RESOURCE_VERSION");
        createdDateTime = getenv("RG_RESOURCE_DT");
        File nsOutputDir = new File(getenv("RG_ANNO_OUTPUT"));
        String name = templateFile.getName();
        if (name.contains("-ids")) ids = true;
        String outputFileName = name.replace("-belanno.st", ".belanno");
        templateName = name.replace(".st", "");
        outputFile = new File(nsOutputDir, outputFileName);
        String absPath = outputFile.getAbsolutePath();

        if (outputFile.exists()) {
            log.info("Overwriting annotation: " + absPath);
        } else {
            log.info("Creating annotation: " + absPath);
        }

        if (ids) log.debug("Identifier-based annotation detected: " + absPath);
        else log.debug("Name-based annotation detected: " + absPath);
    }

    /**
     * Open the template in preparation of writing.
     */
    public void open() {
        try {
            writer = new FileWriter(outputFile);
        } catch (IOException ioex) {
            log.fatal("error opening annotation template output file", ioex);
            ioex.printStackTrace();
            exit(1);
        }
        opened = true;
    }

    /**
     * Write the annotation header to the template.
     */
    public void writeHeader() {
        STGroupDir group = new STGroupDir(templateFile.getParent());
        ST st = group.getInstanceOf(templateName);
        st.add("version", version);
        st.add("createdDateTime", createdDateTime);
        st.add("uri", uri);
        String hdr = st.render();
        try {
            writer.write(hdr);
        } catch (IOException ioex) {
            log.fatal("error writing annotation header", ioex);
            ioex.printStackTrace();
            exit(1);
        }
    }

    private String renderConcept(AnnotationConcept concept) {
        String label = concept.getPreferredLabel();
        String id = concept.getIdentifier();

        // return null if the concept is not complete
        if (label == null || id == null) return null;
        return label + "|" + id + "\n";
    }

    /**
     * Write a {@link AnnotationConcept annotation concept} to the template.
     *
     * @param concept {@link AnnotationConcept}
     */
    public void writeValue(AnnotationConcept concept) {
        String conceptstr = renderConcept(concept);
        if (conceptstr == null) return;
        try {
            writer.write(conceptstr);
        } catch (IOException ioex) {
            log.fatal("error writing annotation value", ioex);
            ioex.printStackTrace();
            exit(1);
        }
    }

    /**
     * Closes the template file.
     */
    @Override
    public void close() {
        if (!opened) return;
        try {
            writer.close();
        } catch (IOException ioex) {
            String path = outputFile.getAbsolutePath();
            log.fatal("error closing template " + path, ioex);
            ioex.printStackTrace();
            exit(1);
        }
    }
}
