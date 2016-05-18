package org.openbel.reggie.rdf;

import org.apache.commons.lang3.tuple.Triple;

/**
 * A T-triple.
 */
public class TTriple<T> extends Triple<T, T, T> {

    private T left;
    private T middle;
    private T right;

    /**
     * Gets the left element in this triple.
     *
     * @return {@code T}
     */
    @Override
    public T getLeft() {
        return left;
    }

    /**
     * Sets the left element in this triple.
     *
     * @param left {@code T}
     */
    public void setLeft(T left) {
        this.left = left;
    }

    /**
     * Gets the middle element in this triple.
     *
     * @return {@code T}
     */
    @Override
    public T getMiddle() {
        return middle;
    }

    /**
     * Sets the middle element in this triple.
     *
     * @param middle {@code T}
     */
    public void setMiddle(T middle) {
        this.middle = middle;
    }

    /**
     * Gets the right element in this triple.
     *
     * @return {@code T}
     */
    @Override
    public T getRight() {
        return right;
    }

    /**
     * Sets the right element in this triple.
     *
     * @param right {@code T}
     */
    public void setRight(T right) {
        this.right = right;
    }
}
