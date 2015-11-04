#!/usr/bin/env python3
# coding: utf-8
'''
Executes an RDF extraction against the configured SPARQL endpoint.
'''
import os
import sys
import rdflib as rl
from functools import partial
from datetime import datetime as dt


def main():
    ###################################
    # BEGIN sanity checking environment
    url = os.getenv('RG_RDF_SPARQL_URL')
    if url is None:
        print('no RG_RDF_SPARQL_URL is set')
        sys.exit(1)
    if not url.endswith('/'):
        url += '/'
    # END sanity checking environment
    #################################

    g = rl.ConjunctiveGraph('SPARQLStore')
    url = url + 'query'
    g.open(url)

    # build namespaces
    NSs = {}
    NSs['belv'] = 'http://www.openbel.org/vocabulary/'
    NSs['dcterms'] = 'http://purl.org/dc/terms/'
    NSs['rdf'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    NSs['rdfs'] = 'http://www.w3.org/2000/01/rdf-schema#'
    NSs['skos'] = 'http://www.w3.org/2004/02/skos/core#'
    NSs['xsd'] = 'http://www.w3.org/2001/XMLSchema#'
    ns_query = 'select ?subject where { ?subject a belv:NamespaceConceptScheme}'
    namespaces = {}
    results = g.query(ns_query, initNs=NSs)
    for row in results:
        nsurl = str(row[0])
        q = 'select ?object where { <%s> belv:prefix ?object }'
        results = g.query(q % (nsurl))
        row = next(iter(results))
        literal = row[0]
        prefix = str(literal)
        # index namespace prefix to URL
        namespaces[prefix] = nsurl

    prefix_query = partial(g.query, initNs=NSs)
    values_query = 'select ?subject where { ?subject skos:inScheme <%s> }'
    value_query = 'select ?predicate ?object where { <%s> ?predicate ?object }'

    for nsurl in namespaces.values():
        q = values_query % (nsurl)
        namespace_values = [x for x in prefix_query(q)]
        total = len(namespace_values)
        print('Received %d results for %s.' % (total, nsurl))
        # for i, row in enumerate(namespace_values):
        #     if i % 100 == 0:
        #         print(i, 'of', total)
        #     value = str(row[0])
        #     q = value_query % (value)
        #     value_triples = [x for x in prefix_query(q)]


if __name__ == '__main__':
    main()
    sys.exit(0)
