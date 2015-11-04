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
import java.util.Iterator;
import java.util.List;

class ResultSetIterator implements Iterator<QuerySolution>, AutoCloseable {
    private Dataset dataset;
    private String query;
    private ResultSet resultSet;

    public ResultSetIterator(Dataset dataset, String query) {
        this.dataset = dataset;
        this.dataset.begin(READ);
        this.query = query;

        QueryExecution qe = QueryExecutionFactory.create(query, dataset);
        this.resultSet = qe.execSelect();
    }

    @Override
    public boolean hasNext() {
        return this.resultSet.hasNext();
    }

    @Override
    public QuerySolution next() {
        return this.resultSet.next();
    }

    @Override
    public void close() {
        this.dataset.end();
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
