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

import org.apache.jena.graph.Triple;
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.RDFNode;

import static org.apache.jena.query.ReadWrite.READ;

import java.util.ArrayList;
import static java.util.Arrays.asList;
import static java.util.Arrays.fill;
import java.util.Iterator;
import java.util.List;

class PagingIterator implements Iterator<QuerySolution>, AutoCloseable {
    private Dataset dataset;
    private String query;
    private QuerySolution[] solutions;
    private int offset = 0;
    private final static int limit = 1000;
    private int current;

    public PagingIterator(Dataset dataset, String query) {
        this.dataset = dataset;
        this.solutions = new QuerySolution[limit];
        query += "\nLIMIT " + limit;
        this.query = query;
        getNextBatch();
        resetCurrent();
    }

    @Override
    public boolean hasNext() {
        // if we've reached the end of the batch...
        if (current >= solutions.length) {
            // ... get another...
            getNextBatch();
            // ... and reset our position.
            resetCurrent();
        }
        if (solutions[current] != null) return true;
        return false;
    }

    @Override
    public QuerySolution next() {
        QuerySolution next = solutions[current];
        current += 1;
        return next;
    }

    @Override
    public void close() {
    }

    private String offsetQuery() {
        String next = query;
        next += "\nOFFSET " + offset;
        return next;
    }

    private void resetCurrent() { current = 0; }

    private void getNextBatch() {
        // null-out existing results
        fill(solutions, null);

        int i = 0;
        try (ReadTX tx = new ReadTX(dataset)) {
            String q = offsetQuery();
            QueryExecution qe = QueryExecutionFactory.create(q, dataset);
            ResultSet rs = qe.execSelect();
            while (rs.hasNext()) {
                QuerySolution next = rs.next();
                solutions[i] = next;
                i += 1;
            }
        }
        offset += limit;
    }

    /**
    public interface AllocatingIterator<E> extends Iterator<E>, Closeable {

    class Iter implements AllocatingIterator<SimpleKAMNode> {
            private boolean closed = false;

            @Override
            public boolean hasNext() {
                if (closed) throw new IllegalStateException("closed");
                try {
                    return nodeRS.next();
                } catch (SQLException e) {
                    e.printStackTrace();
                    close();
                    return false;
                }
            }

            @Override
            public SimpleKAMNode next() {
                if (closed) throw new IllegalStateException("closed");
                KamProtoNode kpn;
                try {
                    kpn = getKamProtoNode(nodeRS, paramRS);
                } catch (SQLException e) {
                    e.printStackTrace();
                    close();
                    return null;
                }
                int id = kpn.getId();
                FunctionEnum fx = kpn.getFunctionType();
                String lbl = kpn.getLabel();
                _KamNode node = new _KamNode(id, fx, lbl);
                return node;
            }

            @Override
            public void remove() {
                throw new UnsupportedOperationException();
            }

            @Override
            public void close() {
                closed = true;
                try {
                    nodeRS.close();
                    paramRS.close();
                } catch (SQLException e) {
                    // ignore it
                }
            }

            @Override
            public void finalize() {
                close();
            }

        }
        return new Iter();
            */

}
