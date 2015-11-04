package org.openbel.reggie.rdf;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.QuerySolution;

import java.util.Iterator;

/**
 * {@link QuerySolution} iterator.
 * Starts iterating the query solutions in a read transaction on construction,
 * and ends the transaction when closed.
 * <p>
 *     <code>
 *         try (QuerySolutions qs = new QuerySolutions(dataset, query)) {
 *             // read transaction begins
 *         }
 *         // read transaction ends
 *     </code>
 * </p>
 */
public class QuerySolutions implements Iterable<QuerySolution>, AutoCloseable {

    //private ResultSetIterator iterator;
    private PagingIterator iterator;

    public QuerySolutions(Dataset dataset, String query) {
        iterator = new PagingIterator(dataset, query);
    }

    @Override
    public void close() {
        iterator.close();
    }

    @Override
    public Iterator<QuerySolution> iterator() {
        return iterator;
    }
}
