package org.openbel.reggie.rdf;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.QuerySolution;

import java.util.Iterator;

/**
 * {@link QuerySolution} iterator.
 * <p>
 *     This class uses applies SPARQL {@code limit} and {@code offset} clauses
 *     to page through results until closed.
 * </p>
 */
public class QuerySolutions implements Iterable<QuerySolution>, AutoCloseable {

    //private ResultSetIterator iterator;
    private PagingIterator iterator;

    /**
     *
     * @param dataset
     * @param query
     */
    public QuerySolutions(Dataset dataset, String query) {
        iterator = new PagingIterator(dataset, query);
    }

    /**
     *
     */
    @Override
    public void close() {
        iterator.close();
    }

    /**
     *
     * @return
     */
    @Override
    public Iterator<QuerySolution> iterator() {
        return iterator;
    }
}
