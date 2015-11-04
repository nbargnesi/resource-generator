package org.openbel.reggie.rdf;

import org.apache.jena.query.Dataset;
import static org.apache.jena.query.ReadWrite.READ;

/**
 * Opens TDB {@link org.apache.jena.query.ReadWrite#READ READ} transactions on
 * construction and ends when it is closed.
 * <p>
 *     <code>
 *         try (ReadTX tx = new ReadTX(dataset)) {
 *             // read transaction begins
 *             ... query dataset
 *         }
 *         // read transaction ends
 *     </code>
 *
 * </p>
 */
public class ReadTX implements AutoCloseable {
    private Dataset dataset;

    /**
     * Create a read transaction for the provided dataset. The transaction
     * begins once constructed.
     *
     * @param ds {@link Dataset}
     */
    public ReadTX(Dataset ds) {
        this.dataset = ds;
        this.dataset.begin(READ);
    }

    /**
     * Ends the read transaction.
     */
    @Override
    public void close() {
        this.dataset.end();
    }
}
