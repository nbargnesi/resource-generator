package org.openbel.reggie.rdf.generate.namespaces;

import org.stringtemplate.v4.*;

import static java.lang.System.*;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * Created by nick on 11/5/15.
 */
public class STMain {

    static class ValuesBlock {
        List<String> values = new ArrayList<>();

        ValuesBlock() {
            values.add("Foo");
            values.add("Bar");
            values.add("Baz");
        }

        public List<String> getValues() {
            return values;
        }
    }

    static class Values implements Iterator<String> {

                private int current = 0;
                private int end = 2000000;

                @Override
                public boolean hasNext() {
                    if (current == end) return false;
                    return true;
                }

                @Override
                public String next() {
                    String ret = String.valueOf(currentTimeMillis());
                    current += 1;
                    return ret;
                }
    }

    public static void main(String... args) throws Exception {
        String templateDir = getenv("RG_JAVA_TEMPLATES");
        if (templateDir == null) {
            err.println("RG_JAVA_TEMPLATES is not set");
            exit(1);
        }
        STGroup group = new STGroupFile(templateDir + "/belns.stg");

        ST belns = group.getInstanceOf("belns");
        belns.add("nsblock", "namespace");
        belns.add("authblock", "author");
        belns.add("citblock", "citation");
        belns.add("procblock", "processing");
        out.println(belns.render());

        ST nsblock = group.getInstanceOf("namespace-block");
        nsblock.add("name", "By any other");
        out.println(nsblock.render());
    }

}
